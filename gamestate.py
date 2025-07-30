class GameState:
    def __init__(self, party, encounter):
        self._party = party
        self._encounter = encounter

        self.turn_count = 0
        self.winner = ""

    def get_encounter(self):
        return self._encounter