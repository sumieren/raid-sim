from skill import Skill
from skills.skills import disciplined_slash
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
        #raise NotImplementedError("Subclasses must implement this method!")
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
        return disciplined_slash.cast(self, game_state.boss)
    
class Archer(Hero):
    def __init__(self, rng):
        super().__init__(rng)
        self.name = "Archer"

    def take_turn(self, game_state):
        return super().take_turn(game_state)
    
class Wizard(Hero):
    def __init__(self, rng):
        super().__init__(rng)
        self.name = "Wizard"

    def take_turn(self, game_state):
        return super().take_turn(game_state)
    
class Priest(Hero):
    def __init__(self, rng):
        super().__init__(rng)
        self.name = "Priest"

    def take_turn(self, game_state):
        return super().take_turn(game_state)