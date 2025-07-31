class Party:
    def __init__(self, rng, size=4):
        self.rng = rng
        self.size = size
        self.members = []

    def add_member(self, hero):
        self.members.append(hero)

    def take_turn(self, game_state):
        selected_actions = []
        log = []

        for hero in self.members:
            action, msg = hero.take_turn(game_state)
            if action:
                selected_actions.append(action)
            if msg:
                log.extend(msg)

        return selected_actions, log

    def end_turn(self, game_state):
        # call end turn on heroes
        pass