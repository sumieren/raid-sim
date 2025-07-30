from encounter import Encounter
from party import Party
from hero import Knight
from boss import TrainingDummy
import random

class GameState:
    """
    Holds all game logic and is responsible for executing
    actions chosen by the player.
    """

    def __init__(self, rng_seed=None):
        self.rng = random.Random(rng_seed)

    def start(self):
        # Select heroes and boss
        party = Party(self.rng)
        boss = TrainingDummy(self.rng)

        party.add_member(Knight(self.rng))

        encounter = Encounter(party, boss)

        encounter.start()
