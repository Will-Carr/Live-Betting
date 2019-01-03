"""REST API for updating the game."""
import json
import requests
import flask
import live_betting
from live_betting.model import CUR_GAME


@live_betting.app.route('/api/v1/update/', methods=["POST"])
def update_game():
    """Receive the update message from GroupMe or other POST.

    Input:
    {
      ...
      "text": "!football michigan"
      ...
    }
    """

    message = flask.request.get_json()["text"]

    if len(message) > 0 and message[0] == "!":

        message = message[1:]
        message = message.strip()
        message = message.lower()

        if message == "help":
            response = """
The command:
![SPORT] [TEAM]

SPORT is, you know, the sport you're looking for. The ones that are supported are:
football, basketball, hockey, soccer

TEAM is one of the teams playing in the game. For college, only use the school's name, but pros can use either the city/state or the team name. Idk, Bovada's fucky like that.

Examples:
!Football Michigan
!Football Browns
!Basketball New York Knicks
            """

            post_json = {
                "bot_id": "d3835727b9e146241672ef5119",
                "text": response
            }

            requests.post("https://api.groupme.com/v3/bots/post", json=post_json)

        else:
            sport, team = message.split(" ", 1)

            CUR_GAME["sport"] = sport
            CUR_GAME["team"] = team


    return flask.jsonify(**{})
