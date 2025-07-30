from skill import Skill
import random

class Hero:
    def __init__(self, rng):
        self._hp = 0
        self._mp = 0

        self.str = 0
        self.dex = 0
        self.int = 0
        self.vit = 0
        self.mnd = 0

        self.rng = rng

    def take_turn(self, game_state):
        pass

    def end_turn(self, game_state):
        # manage buffs and debuffs
        # tick down cooldowns by 1 turn
        pass

    @property
    def hp(self):
        return self._hp
    
    def mp(self):
        return self._mp

class Knight(Hero):
    def __init__(self, rng):
        super().__init__(rng)
        self.name = "Knight"

    def take_turn(self, game_state):
        skill = Skill("Disciplined Slash", 0, self.disciplined_slash)
        skill.cast(self, game_state.boss)

    def disciplined_slash(self, skill, user, target):
        damage = self.rng.randint(2,4)
        target.take_damage(damage)
        return f"{skill.name} deals {damage} damage to {target.name}!"