"""Loads current game and stores it as global."""

CUR_GAME = {
    "sport": "football",
    "team": "texas"
}


def load_cur_game():
    """
    Load the current game.

    Ex:
    CUR_GAME = {
        "sport": "football",
        "team": "texas"
    }
    """
    global CUR_GAME
    CUR_GAME = {
        "sport": "football",
        "team": "texas"
    }


def update_cur_game(new_game):
    """
    Update the current game.

    Ex param:
    {
        "sport": "football",
        "team": "texas"
    }
    """
    global CUR_GAME
    CUR_GAME = new_game
