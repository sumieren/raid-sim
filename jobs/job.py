from skill import Skill
import random

from .registry import register_job

class Job:
    def __init__(self, hp, mp, rng):
        self.tier = 1

        self._hp = hp
        self._mp = mp

        self._cur_hp = self._hp
        self._cur_mp = self._mp

        self.str = 0
        self.dex = 0
        self.int = 0
        self.vit = 0
        self.mnd = 0

        self.skills = []

        self.rng = rng

    def take_turn(self, game_state):
        #raise NotImplementedError("Subclasses must implement this method!")
        return (None, None)

    def end_turn(self, game_state):
        # manage buffs and debuffs
        # tick down cooldowns by 1 turn
        for skill in self.skills:
            skill.pass_turn()

    @property
    def hp(self):
        return self._cur_hp
    
    @property
    def max_hp(self):
        return self._hp
    
    def mp(self):
        return self._mp
    
from skills.skills import disciplined_slash
@register_job
class Archer(Job):
    def __init__(self, rng):
        super().__init__(hp=10, mp=10, rng=rng)
        self.name = "Archer"

        self.skills = [disciplined_slash()]

    def take_turn(self, game_state):
        return self.skills[0].cast(self, game_state.boss)
    
from skills.skills import fireball
@register_job
class Wizard(Job):
    def __init__(self, rng):
        super().__init__(hp=10, mp=10, rng=rng)
        self.name = "Wizard"

        self.skills = [fireball()]

    def take_turn(self, game_state):
        if self.skills[0].current_cooldown == 0:
            return self.skills[0].cast(self, game_state.boss)
        else:
            return (None, None)
    
@register_job
class Priest(Job):
    def __init__(self, rng):
        super().__init__(hp=10, mp=10, rng=rng)
        self.name = "Priest"

    def take_turn(self, game_state):
        return super().take_turn(game_state)