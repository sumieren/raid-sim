import time
import math
from log import log_damage, log_heal, log_boss_damage
from party import Party, Stat
from boss import BossState

class Encounter:
    """
    Individual boss fight. Receives data from gamestate
    and executes the boss fight. Returns rewards.
    """

    def __init__(self, rng, party, boss):
        self.rng = rng
        self.party = party
        self.boss = boss

        self._turn_count = 1
        

    def start(self):
        # Start game loop
        auto_advance = False
        timeout = 2.0

        while not self.is_fight_over():
            turn_log = []
            turn_log.extend(self.take_turn(self.party, self.boss))

            self.print_ui()
            for msg in turn_log:
                print(msg)

            self.end_turn(self.party, self.boss)



            # Interim check if game is over, so we don't need to wait for next turn.
            if self.is_fight_over():
                break

            auto_advance, timeout = self.wait_for_next_turn(auto_advance, timeout)

            self._turn_count += 1 

        # Display result
        print("You win!")

    def take_turn(self, party, boss):
        log = []

        party_actions = party.take_turn(self)
        for action, message in party_actions:
            if message:
                log.extend(message)
            if action:
                print(action)
                log.extend(self.handle_action(action))

        boss_actions = boss.take_turn(self)
        for action, message in boss_actions:   
            if message:
                log.extend(message)
            if action:
                print(action)
                log.extend(self.handle_boss_action(action))

        return log

    def end_turn(self, party, boss):
        party.end_turn(self)
        boss.end_turn(self)


    def wait_for_next_turn(self, auto_advance, timeout):
        """ 
        Delays the game until the player presses Enter.
        Player can type 'auto' followed by a float to automatically
        advance the gamestate until it ends. Returns the options to
        'save' the chosen mode and timeout.

        Args:
            auto_advance (bool): Whether to auto advance game state or not.
            timeout (float): Amount of seconds to delay between each auto turn.
        """

        if auto_advance:
            time.sleep(timeout)
            # Empty line for clarity
            print()
            return auto_advance, timeout
        else:
            prompt = input("\nPress Enter for next turn, or type 'auto <seconds>' for auto-advance: ").strip().lower()

            if prompt.startswith("auto"):
                parts = prompt.split()

                if len(parts) > 1:
                    try:
                        timeout = float(parts[1])
                    except:
                        print("Invalid timeout entered, using default value.")
                    print(f"Starting auto mode with timeout {timeout} seconds.")

                # Empty line for clarity
                print()
                return True, timeout
            
            # Empty line for clarity
            print()
            print()
            return False, timeout
        
    def is_fight_over(self):
        if self.boss.hp <= 0:
            print(f"{self.boss.name} was defeated!\n")
            return True
        return False
    
    def print_ui(self):
        print(f"Turn #{self._turn_count}")

        members_per_line = 2
        num_members = len(self.party.members)
        lines = []

        # For each 2 party members, generate a line with their name, HP and gauge stats
        for i in range (0, num_members, members_per_line):
            left = " ".join(f"{member.name}: {member.hp}/{member.max_hp} [{member.gauge_status()}]"
                        for member in self.party.members[i:i+members_per_line])
            lines.append(left)

        spacer = " " * 30

        # For the first 2 lines: boss name, HP bar
        for index, line in enumerate(lines):
            right = ""
            if index == 0:
                right = self.boss.name + "    " + self.draw_gauge(self.boss.hp, self.boss.max_hp, label="[HP]")
            elif index == 1:
                right = (len(self.boss.name) * " ") + "    " + self.draw_gauge(self.boss.stagger, self.boss.stun_threshold, label="[ST]")
            print(f"{line}{spacer}{right}")

        print()
    
    def draw_gauge(self, current, max_value, bar_length=10, label=""):
        # Get hp ratio and round to find how many are filled and which are partially filled.
        # Then loop over all bars to see how far filled or empty they should be
        ratio = max(0, min(1, current / max_value))
        filled = int(ratio * bar_length)
        partial_fill = ratio * bar_length - filled
        chars = "█▓▒░-"
        dither = ""
        for i in range(bar_length):
            if i < filled:
                dither += chars[0]     # Solid fill
            elif i == filled and partial_fill > 0:
                # Pick character according to fraction (optional: finer granularity if you want)
                if partial_fill > 0.7:
                    dither += chars[1] # Heavy dither
                elif partial_fill > 0.35:
                    dither += chars[2] # Mid dither
                else:
                    dither += chars[3] # Light dither
            else:
                dither += chars[-1]    # Empty
        return f"{label}|{dither}| {current}/{max_value}"

    def handle_action(self, data):
        crit_multiplier = 3
        match (data["type"]):
            # Receives type == damage, amount of base damage, user object, targets list and skill object
            case "damage":
                log = []

                targets = data["targets"]
                final_damage = data["damage"] + (self.party.power * Party.POWER_SCALING)

                is_crit = self.party.inspiration_check(data["user"].crit_chance + (self.party.focus * Party.FOCUS_CRIT_CHANCE))
                if is_crit:
                    final_damage *= crit_multiplier

                # Accuracy is one of the rare chances not affected by Inspiration, because it's generally at 100% and can get lowered by mechanics.
                # These mechanics would have no point if any amount of inspiration mitigated it.
                is_miss = (data["user"].accuracy + (self.party.focus * Party.FOCUS_ACCURACY)) < self.rng.random()
                if is_miss:
                    final_damage = 0

                if self.boss.state == BossState.CHARGING and self.boss.next_action:
                    interrupt_chance = self.party.adaptability * Party.ADAPT_INTERRUPT
                    if self.party.inspiration_check(interrupt_chance):
                        self.boss.trigger_interrupt()

                # Regular damage slowly builds stagger.
                damage_stagger_ratio = 0.01
                final_stagger = (final_damage * damage_stagger_ratio) * (1 + (self.party.adaptability * Party.ADAPT_STAGGER_BOOST))

                final_damage = round(final_damage)
                final_stagger = math.ceil(final_stagger)
                for target in targets:
                    target.take_damage(final_damage)
                    target.take_stagger(final_stagger)
                    log.extend(log_damage(data["skill"], final_damage, [target], is_crit, is_miss))

                return log
            
            # Receives type == heal, amount of base healing, user object, targets list and skill object
            case "heal":
                log = []

                targets = data["targets"]
                final_heal = data["amount"] + (self.party.power * Party.POWER_SCALING)

                is_crit = self.party.inspiration_check(data["user"].crit_chance + (self.party.focus * Party.FOCUS_CRIT_CHANCE))
                if is_crit:
                    final_heal *= crit_multiplier

                final_heal = round(final_heal)
                for target in targets:
                    target.get_healed(final_heal)
                    log.extend(log_heal(data["skill"], final_heal, [target], is_crit))

                return log

                
            
    def handle_boss_action(self, data):
        match (data["type"]):
            # Receives type == damage, attack name, user, damage, targets whether it is dodgeable
            case "damage":
                log = []
                targets = data["targets"]
                damage = data["damage"]

                damage = round(damage)
                for target in targets:
                    response = target.take_damage(self, damage, data["dodgeable"])
                    if response == "dodge":
                        log.extend(log_boss_damage(data["attack_name"], damage, [target], is_dodge=True))
                    elif response == "block":
                        log.extend(log_boss_damage(data["attack_name"], damage, [target], is_block=True))
                    else:
                        log.extend(log_boss_damage(data["attack_name"], damage, [target]))

                return log

                
