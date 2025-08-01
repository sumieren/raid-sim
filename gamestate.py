from encounter import Encounter
from party import Party
import hero
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

        party.add_member(hero.Knight(self.rng))
        party.add_member(hero.Archer(self.rng))
        party.add_member(hero.Wizard(self.rng))
        party.add_member(hero.Priest(self.rng))

        encounter = Encounter(self.rng, party, boss)

        encounter.start()
