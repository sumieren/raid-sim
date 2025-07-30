from encounter import Encounter
from party import Party
from hero import Knight
from boss import TrainingDummy

class GameState:
    def __init__(self):
        pass

    def start(self):
        # Select heroes and boss
        party = Party()
        boss = TrainingDummy()

        party.add_member(Knight())

        encounter = Encounter(party, boss)

        encounter.start()
