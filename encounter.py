import time

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
            print(f"Turn #{self._turn_count}")
            self.take_turn(self.party, self.boss)
            self.end_turn(self.party, self.boss)

            # Interim check if game is over, so we don't need to wait for next turn.
            if self.is_fight_over():
                break
            
            auto_advance, timeout = self.wait_for_next_turn(auto_advance, timeout)

            self._turn_count += 1

        # Display result
        print("You win!")

    def take_turn(self, party, encounter):
        party.take_turn(self)
        encounter.take_turn(self)

    def end_turn(self, party, encounter):
        party.end_turn(self)
        encounter.end_turn(self)

        #advance game state by 1 turn

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
            return False, timeout
        
    def is_fight_over(self):
        if self.boss.hp <= 0:
            print(f"{self.boss.name} was defeated!\n")
            return True
        return False
    
    def handle_skill_effects(self, effect, targets):
        # f"{skill.name} deals {damage} damage to {targets.name}!"
        pass