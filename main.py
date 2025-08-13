from gamestate import GameState
from utils import get_choice

"""
Game conductor. Receives player input and prompts
the GameState to execute the appropriate actions.
"""

current_screen = "main_menu"
game_running = True

def main():
    global current_screen
    menu_options = {
        "main_menu": main_menu,
        "start_game": start_game,
    }

    while(game_running):
        menu_function = menu_options[current_screen]
        menu_function()
    

def main_menu():
    global current_screen, game_running
    choice = get_choice("Start game?", ["Yes", "No"])
    if choice == 0:
        current_screen = "start_game"
    else:
        game_running = False

def start_game():
    global current_screen
    
    game = GameState()

    game.start()

    current_screen = "main_menu"

if __name__ == "__main__":
    main()