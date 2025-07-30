class Boss:
    def __init__(self):
        self.name = ""
        self._hp = 0

    def take_turn(self, game_state):
        pass

    def end_turn(self, game_state):
        pass

    def take_damage(self, damage):
        self._hp -= damage

    @property
    def hp(self):
        return self._hp
    
class TrainingDummy(Boss):
    def __init__(self):
        self.name = "Training Dummy"
        self._hp = 10