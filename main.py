from gamestate import GameState

"""
Game conductor. Receives player input and prompts
the GameState to execute the appropriate actions.
"""

def main():
    game = GameState()

    game.start()

if __name__ == "__main__":
    main()