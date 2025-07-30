from party import Party
from hero import Knight
from encounter import TrainingDummy
from gamestate import GameState
import time

def main():
    # Select heroes and boss
    party = Party()
    encounter = TrainingDummy()

    # Create game state
    party.add_member(Knight())
    game = GameState(party, encounter)

    # Start game loop
    game_over = False

    auto_advance = False
    timeout = 2.0

    while not game_over:
        take_turn(game, party, encounter)
        end_turn(game, party, encounter)

        auto_advance, timeout = wait_for_next_turn(auto_advance, timeout)

    # Display result
    print(f"The winner is: {game.get_winner}")

def take_turn(game_state, party, encounter):
    party.take_turn(game_state)
    encounter.take_turn(game_state)

def end_turn(game_state, party, encounter):
    party.end_turn(game_state)
    encounter.end_turn(game_state)

    #advance game state by 1 turn

def wait_for_next_turn(auto_advance, timeout):
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

def is_battle_over(party, encounter):
    pass

if __name__ == "__main__":
    main()