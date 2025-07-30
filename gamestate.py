class GameState:
    def __init__(self, party, encounter):
        self._party = party
        self._encounter = encounter

        self._turn_count = 0
        self._winner = ""

    def get_encounter(self):
        return self._encounter
    
    def get_winner(self):
        return self.winner