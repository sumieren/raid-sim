class Party:
    def __init__(self, rng, size=4):
        self.rng = rng
        self.size = size
        self.members = []

    def add_member(self, hero):
        self.members.append(hero)

    def take_turn(self, game_state):
        selected_actions = []

        for hero in self.members:
            selected_actions.append(hero.take_turn(game_state))

        return selected_actions

    def end_turn(self, game_state):
        # call end turn on heroes
        pass