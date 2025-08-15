from .registry import register_job
from party import Party

class Job:
    def __init__(self, hp, mp, rng):
        self._hp = hp
        self._cur_hp = self._hp

        self.speed = 0

        self.crit_chance = 0.05
        self.accuracy = 1.0
        self.block_chance = 0.0
        self.dodge_chance = 0.0
        self.gauge_boost = 0

        self.skills = []

        self.rng = rng

    def take_turn(self, game_state):
        raise NotImplementedError("Subclasses must implement this method!")

    def end_turn(self, game_state):
        # manage buffs and debuffs
        for skill in self.skills:
            skill.pass_turn()

    def gauge_status(self):
        return "test"

    def take_damage(self, game_state, damage, dodgeable=True):
        is_dodge = game_state.party.inspiration_check(self.dodge_chance + (game_state.party.focus * Party.FOCUS_DODGE_CHANCE)) if dodgeable else False
        if is_dodge:
            return "dodge"
        else:
            is_block = game_state.party.inspiration_check(self.block_chance + (game_state.party.tenacity * Party.TENACITY_BLOCK_CHANCE))
            if is_block:
                damage *= (1 - Party.TENACITY_BLOCK_AMOUNT)

            self._cur_hp -= round(damage)

            if self._cur_hp < 0:
                self._cur_hp = 0

            if is_block:
                return "block"
        
        return None

    def gain_max_hp(self, amount, in_encounter=False):
        self._hp += amount
        if not in_encounter:
            self._cur_hp = self._hp

    def get_healed(self, amount):
        self._cur_hp = round(min(self._cur_hp + amount, self._hp))

    @property
    def hp(self):
        return self._cur_hp
    
    @property
    def max_hp(self):
        return self._hp
    
from skills.skills import disciplined_slash
@register_job
class Archer(Job):
    def __init__(self, rng):
        super().__init__(hp=10, mp=10, rng=rng)
        self.name = "Archer"

        self.speed = 7

        self.skills = [disciplined_slash()]

    def take_turn(self, game_state):
        return self.skills[0].cast(self, game_state.boss)
    
from skills.skills import fireball
@register_job
class Wizard(Job):
    def __init__(self, rng):
        super().__init__(hp=10, mp=10, rng=rng)
        self.name = "Wizard"

        self.speed = 4

        self.skills = [fireball()]

    def take_turn(self, game_state):
        if self.skills[0].current_cooldown == 0:
            return self.skills[0].cast(self, game_state.boss)
        else:
            return (None, ["Wizard was unable to act."])
    
from skills.skills import cure
@register_job
class Priest(Job):
    def __init__(self, rng):
        super().__init__(hp=10, mp=10, rng=rng)
        self.name = "Priest"

        self.speed = 4

        self.skills = [cure()]

    def take_turn(self, game_state):
        target_list = []

        for member in game_state.party.members:
            if member.hp < 4:
                target_list.append(member)

        if not target_list:
            target_list = game_state.party.members
        target = game_state.rng.choice(target_list)

        return self.skills[0].cast(self, target)