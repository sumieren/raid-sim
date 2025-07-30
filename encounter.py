class Encounter:
    def __init__(self, party, encounter):
        self._party = party
        self._encounter = encounter

        self._turn_count = 0

    def is_fight_over(self):
        if self.encounter.hp <= 0:
            print(f"{self.encounter.name} was defeated!\n")
            self._winner = self.party.members
            return True
        return False

    @property
    def party(self):
        return self._party

    @property
    def encounter(self):
        return self._encounter