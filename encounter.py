import time
from log import log_damage
from party import Party, Stat

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
            self.end_turn(self.party, self.boss)

            #test zone for effects
            self.party.gain_stat(Stat.TENACITY, 1, in_encounter=True)

            self.print_ui()
            for msg in turn_log:
                print(msg)

            # Interim check if game is over, so we don't need to wait for next turn.
            if self.is_fight_over():
                break

            auto_advance, timeout = self.wait_for_next_turn(auto_advance, timeout)
            

        # Display result
        print("You win!")

    def take_turn(self, party, encounter):
        party_actions, log = party.take_turn(self)
        for action in party_actions:
            log.extend(self.handle_action(action))
        encounter.take_turn(self)

        return log

    def end_turn(self, party, encounter):
        party.end_turn(self)
        encounter.end_turn(self)

        self._turn_count += 1

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

        for member in self.party.members:
            print(f"{member.name}: {member.hp}/{member.max_hp}", end=" ")

        spacer = " " * 30
        print(f"{spacer}{self.boss.name} {self.boss_hp_bar()} {self.boss.hp}/{self.boss.max_hp}")

    def boss_hp_bar(self):
        return f"|███████████|"

    def handle_action(self, data):
        match (data["type"]):
            # Receives type == damage, amount of base damage, user object, targets list and skill object
            case "damage":
                targets = data["targets"]
                final_damage = data["damage"] + (self.party.power * Party.POWER_SCALING)

                is_crit = self.party.inspiration_check(data["user"].crit_chance)
                if is_crit:
                    final_damage *= 3

                # Accuracy is one of the rare chances not affected by Inspiration, because it's generally at 100% and can get lowered by mechanics.
                # These mechanics would have no point if any amount of inspiration mitigated it.
                is_miss = data["user"].accuracy < self.rng.random()
                if is_miss:
                    final_damage = 0

                final_damage = round(final_damage)

                for target in targets:
                    target.take_damage(final_damage)

                return log_damage(data["skill"], final_damage, data["targets"], is_crit, is_miss)