from skill import Skill
from gamestate import GameState

class Hero:
    def __init__(self):
        self._hp = 0
        self._mp = 0

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
    def __init__(self):
        super().__init__()
        self.name = "Knight"

    def take_turn(self, game_state):
        skill = Skill("Disciplined Slash", 0, self.disciplined_slash)
        skill.cast(self, game_state.encounter)

    def disciplined_slash(self, skill, user, target):
        target.take_damage(1)
        return f"{skill.name} deals 1 damage to {target.name}!"