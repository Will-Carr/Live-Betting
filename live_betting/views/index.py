"""
Live_Betting index (main) view.

URLs include:
/
"""
import json
import requests
import flask
import live_betting


@live_betting.app.route('/', methods=['GET'])
def show_index():
    """Display / route."""

    # # Our API
    # url = "http://localhost:6969/api/v1/odds/"
    #
    # r = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(CUR_GAME))
    # all_odds = r.json()
    #
    # print(json.dumps(all_odds, indent=4))
    # context = all_odds

    return flask.render_template("index.html")
