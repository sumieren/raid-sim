from log import log_bonus_action
from enum import Enum, auto

class Stat(Enum):
    POWER = auto()
    TENACITY = auto()
    ALACRITY = auto()
    SYNERGY = auto()
    FOCUS = auto()
    ADAPTABILITY = auto()
    INSPIRATION = auto()

class Party:
    POWER_SCALING = 1.0           # Amount of increased damage/healing/etc 1 point of Power gives
    TENACITY_TO_HP = 10           # Amount of max HP gained per point of tenacity
    TENACITY_BLOCK_CHANCE = 0.05  # Percentage to trigger tenacity damage reduction per point of tenacity
    TENACITY_BLOCK_AMOUNT = 0.3   # Percent of damage blocked by a tenacity block (Currently does not scale with tenacity check if this works in playtests)
    # todo: tenacity debuff effects
    # todo: synergy buff effects
    SYNERGY_PROC_CHANCE = 0.005   # Bonus turn chance per point of synergy
    FOCUS_CRIT_CHANCE = 0.05      # Amount of crit added per point in focus
    FOCUS_ACCURACY = 0.075        # Amount of accuracy per point in focus
    FOCUS_DODGE_CHANCE = 0.01     # Chance to dodge per point in focus

    INSPIRATION_BOOST = 0.1       # Percentage by which all chance-based effects are increased per point of inspiration

    def __init__(self, rng, size=4):
        self.rng = rng
        self.size = size
        self.members = []

        # Party-wide stats, primary progression next to job advancements.
        self.power = 0              # Governs damage and healing output
        self.tenacity = 0           # Governs max hp, chance to take less damage, debuff duration
        self.alacrity = 0           # Governs gauge and a chance to reduce cd
        self.synergy = 0            # Governs buffs and a chance to give another teammate another action
        self.focus = 0              # Governs crit, accuracy, dodges
        self.adaptability = 0       # Governs stun rate, provides chance to interrupt boss casts
        self.inspiration = 0        # Governs all random chance (skills and stats)

    def add_member(self, hero):
        self.members.append(hero)

    def take_turn(self, game_state):
        tuples = []

        for hero in sorted(self.members, key=lambda h: h.speed, reverse=True):
            action, msg = hero.take_turn(game_state)
            if not action:
                continue

            tuples.append((action, msg))

            inspired_hero, message = self.check_synergy_proc(hero, [m for m in self.members if m is not hero])
            if inspired_hero:
                tuples.append((None, message))
                a, m = inspired_hero.take_turn(game_state)

                if a and m:
                    tuples.append((a, m))

        return tuples

    def end_turn(self, game_state):
        for hero in self.members:
            hero.end_turn(game_state)

    def gain_stat(self, stat, amount, in_encounter=False):
        match (stat):
            case Stat.POWER:
                pass
            case Stat.TENACITY:
                if in_encounter:
                    print("The party gained Tenacity, but temporary buffs haven't been implemented yet.")
                else:
                    self.tenacity += amount

                # Gain max_hp
                for member in self.members:
                    member.gain_max_hp(amount, in_encounter)
            case Stat.ALACRITY:
                pass
            case Stat.SYNERGY:
                pass
            case Stat.FOCUS:
                pass
            case Stat.ADAPTABILITY:
                pass
            case Stat.INSPIRATION:
                pass
            case _:
                raise ValueError(f"Unknown stat: {stat}") 

    def check_synergy_proc(self, procced_from, eligible_members):
        is_proc = self.inspiration_check(self.SYNERGY_PROC_CHANCE * self.synergy)
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