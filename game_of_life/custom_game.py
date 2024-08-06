# Get user input for custom rules of the game - `game of life`.
# `B(born)number/S(survivor)two numbers`
# default: (B3/S23)


def custom_game():
    """Get user input for custom game."""
    game_legality: str = input("Enter the legality of the game (default: B3/S23): ")

    try:
        import game
    except:
        import game_of_life.game as game

    game.game_of_life(game_legality)


if __name__ == "__main__":
    custom_game()
