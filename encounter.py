class Encounter:
    def __init__(self):
        self.name = ""
        self._hp = 0

    def take_turn(self, game_state):
        pass

    def end_turn(self, game_state):
        pass

    def take_damage(self, damage):
        self._hp -= damage
        if self.hp == 0:
            print("Enemy defeated!")

    @property
    def hp(self):
        return self._hp
    
class TrainingDummy(Encounter):
    def __init__(self):
        self.name = "Training Dummy"
        self._hp = 10