class GameState:
    def __init__(self, party, encounter):
        self.party = party
        self.encounter = encounter

        self.turn_count = 0
        self.winner = ""
