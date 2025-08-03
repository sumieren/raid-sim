from encounter import Encounter
from party import Party

from jobs.registry import JOB_REGISTRY

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

        party.add_member(JOB_REGISTRY["Knight"](self.rng))
        party.add_member(JOB_REGISTRY["Archer"](self.rng))
        party.add_member(JOB_REGISTRY["Wizard"](self.rng))
        party.add_member(JOB_REGISTRY["Knight"](self.rng))

        encounter = Encounter(self.rng, party, boss)

        encounter.start()
