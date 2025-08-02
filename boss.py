class Boss:
    def __init__(self, hp, rng):
        self.name = ""
        self.rng = rng

        self._hp = hp
        self._cur_hp = self._hp

    def take_turn(self, game_state):
        pass

    def end_turn(self, game_state):
        pass

    def take_damage(self, damage):
        self._cur_hp -= damage

        if self._cur_hp < 0:
            self._cur_hp = 0

    @property
    def hp(self):
        return self._cur_hp
    
    @property
    def max_hp(self):
        return self._hp
    
class TrainingDummy(Boss):
    def __init__(self, rng):
        super().__init__(hp=100, rng=rng)
        self.name = "Training Dummy"