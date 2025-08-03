class Party:
    POWER_SCALING = 1.0      # Amount of increased damage/healing/etc 1 point of Power gives.

    def __init__(self, rng, size=4):
        self.rng = rng
        self.size = size
        self.members = []

        # Party-wide stats, primary progression next to job advancements.
        self.power = 0          # Governs damage and healing output
        self.tenacity = 0       # Governs damage taken, chance to take less damage, debuff duration
        self.alacrity = 0       # Governs gauge and a chance to reduce cd
        self.synergy = 0        # Governs buffs and a chance to give another teammate another action
        self.focus = 0          # Governs crit, accuracy, dodges
        self.adaptability = 0   # Governs stun rate, provides chance to interrupt boss casts
        self.inspiration = 0    # Governs all random chance (skills and stats)

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
        for hero in self.members:
            hero.end_turn(game_state)