from encounter import Encounter
from party import Party

from jobs import job
from jobs import knight

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

        party.add_member(knight.Knight(self.rng))
        party.add_member(job.Archer(self.rng))
        party.add_member(job.Wizard(self.rng))
        party.add_member(job.Priest(self.rng))

        encounter = Encounter(self.rng, party, boss)

        encounter.start()
