"""Loads current game and stores it as global."""

import time

CUR_GAME = {}
LAST_FOUND = 0.0

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
        "sport": "basketball",
        "team": "ruifvbgrui"
    }

    global LAST_FOUND
    LAST_FOUND = 0.0


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

    global LAST_FOUND
    LAST_FOUND = time.time()

def update_last_time():
    """
    Update LAST_FOUND.
    """
    global LAST_FOUND
    LAST_FOUND = time.time()
