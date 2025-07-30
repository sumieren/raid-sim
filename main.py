from party import Party
from hero import Knight
from encounter import Encounter
from gamestate import GameState
import time

def main():
    # Select heroes and boss
    party = Party()
    encounter = Encounter("Training Dummy")

    # Create game state
    party.add_member(Knight())
    game = GameState(party, encounter)

    # Start game loop
    game_over = False

    auto_advance = False
    timeout = 2

    while not game_over:
        take_turn(game, party, encounter)
        end_turn(game, party, encounter)

        auto_advance, timeout = wait_for_next_turn(auto_advance, timeout)

    # Display result

def take_turn(game_state, party, encounter):
    party.take_turn(game_state)
    encounter.take_turn(game_state)

def end_turn(game_state, party, encounter):
    party.end_turn(game_state)
    encounter.end_turn(game_state)

    #advance game state by 1 turn

def wait_for_next_turn(auto_advance, timeout):
    time.sleep(timeout)

    return auto_advance, timeout

def is_battle_over(party, encounter):
    pass

if __name__ == "__main__":
    main()