from log import log_bonus_action

class Party:
    POWER_SCALING = 1.0           # Amount of increased damage/healing/etc 1 point of Power gives
    TENACITY_TO_HP = 10           # Amount of max HP gained per point of tenacity
    TENACITY_BLOCK_CHANCE = 0.05  # Percentage to trigger tenacity damage reduction per point of tenacity
    TENACITY_BLOCK_AMOUNT = 0.3   # Percent of damage blocked by a tenacity block (Currently does not scale with tenacity check if this works in playtests)
    # todo: tenacity debuff effects

    SYNERGY_PROC_CHANCE = 0.005   # Bonus turn chance per point of synergy

    INSPIRATION_BOOST = 0.1       # Percentage by which all chance-based effects are increased per point of inspiration

    def __init__(self, rng, size=4):
        self.rng = rng
        self.size = size
        self.members = []

        # Party-wide stats, primary progression next to job advancements.
        self.power = 0              # Governs damage and healing output
        self.tenacity = 1000000           # Governs damage taken, chance to take less damage, debuff duration
        self.alacrity = 0           # Governs gauge and a chance to reduce cd
        self.synergy = 0            # Governs buffs and a chance to give another teammate another action
        self.focus = 0              # Governs crit, accuracy, dodges
        self.adaptability = 0       # Governs stun rate, provides chance to interrupt boss casts
        self.inspiration = 0        # Governs all random chance (skills and stats)

    def add_member(self, hero):
        self.members.append(hero)

    def take_turn(self, game_state):
        selected_actions = []
        log = []

        for hero in sorted(self.members, key=lambda h: h.speed, reverse=True):
            action, msg = hero.take_turn(game_state)
            if not action:
                continue

            selected_actions.append(action)

            if msg:
                log.extend(msg)

            if action:
                inspired_hero, message = self.check_synergy_proc(hero, [m for m in self.members if m is not hero])
                if inspired_hero:
                    log.extend(message)
                    a, m = inspired_hero.take_turn(game_state)

                    if a:
                        selected_actions.append(a)
                    if m:
                        log.extend(m)

        return selected_actions, log

    def end_turn(self, game_state):
        for hero in self.members:
            hero.end_turn(game_state)

    def check_synergy_proc(self, procced_from, eligible_members):
        is_proc = self.inspiration_check(self.SYNERGY_PROC_CHANCE)
        chosen_member = self.rng.choice(eligible_members)

        if is_proc:
            return chosen_member, log_bonus_action(procced_from, chosen_member)
        else:
            return None, None
        
    def inspiration_check(self, base_chance):
        """
        Returns True if a chance-based effect succeeds, factoring in party-wide inspiration.
        - base_chance is the base probability (0.0–1.0).
        - party.inspiration boosts the base chance.
        """
        true_chance = base_chance * (1 + (self.inspiration * Party.INSPIRATION_BOOST))
        return self.rng.random() < min(true_chance, 1.0)