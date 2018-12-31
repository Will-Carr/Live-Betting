"""REST API for getting odds."""
import json
import requests
import flask
import live_betting
from live_betting.model import CUR_GAME


@live_betting.app.route('/api/v1/odds/', methods=["GET"])
def get_odds():
    """GET the desired sport and team, then return the odds.

    Return:
    {
      "odds": [
        {
            "type": "spread", (spread, moneyline, total)
            "period": "Match", (Match, 1st Quarter, etc)
            "teams": [
                {
                    "team": "michigan",
                    "val": "-6.5"
                },
                {
                    "team": "florida",
                    "val": "+6.5"
                }
            ]
        },
        ...
      ]
    }
    """

    sport = CUR_GAME['sport']
    team = CUR_GAME['team']

    # The Bovada API
    url = "https://www.bovada.lv/services/sports/event/v2/events/A/description/" + sport

    r = requests.get(url)
    all_odds = r.json()

    found = False

    competitors = []

    # The request comes back as an array of different leagues.
    # So for football, it'll be split into NFL, CFB, CFL
    for odds_set in all_odds:
        if found:
            break

        # Each league then has all the games in an array
        for game in odds_set["events"]:
            if found:
                break

            # Loop through the competitors to match the wanted team
            for competitor in game["competitors"]:
                if team in competitor["name"].lower():

                    competitors = [c["name"] for c in game["competitors"]]

                    all_odds = game["displayGroups"]

                    found = True
                    break

    if not found:
        return flask.jsonify(**{})

    # all_odds is now an array of groups of odds. We only care about the normal
    # odds, so that's [0]
    normal_odds = all_odds[0]

    context = {"odds": []}

    for odds_type in normal_odds["markets"]:

        new_odd = {}

        if odds_type["description"] == "Point Spread":

            new_odd["type"] = "spread"
            new_odd["period"] = odds_type["period"]["description"]
            new_odd["teams"] = []

            for outcome in odds_type["outcomes"]:

                if float(outcome["price"]["handicap"]) > 0:
                    outcome["price"]["handicap"] = "+" + outcome["price"]["handicap"]

                # Normalize the team names
                if outcome["description"] not in competitors:
                    outcome["description"] = competitors[odds_type["outcomes"].index(outcome)]

                new_odd["teams"].append({
                    "team": outcome["description"],
                    "val": outcome["price"]["handicap"] + " (" + outcome["price"]["american"] + ")"
                })

            context["odds"].append(new_odd)

        elif odds_type["description"] == "Moneyline":

            new_odd["type"] = "moneyline"
            new_odd["period"] = odds_type["period"]["description"]
            new_odd["teams"] = []

            for outcome in odds_type["outcomes"]:

                # Normalize the team names
                if outcome["description"] not in competitors:
                    outcome["description"] = competitors[odds_type["outcomes"].index(outcome)]

                new_odd["teams"].append({
                    "team": outcome["description"],
                    "val": outcome["price"]["american"]
                })

            context["odds"].append(new_odd)

        elif odds_type["description"] == "Total":

            new_odd["type"] = "total"
            new_odd["period"] = odds_type["period"]["description"]
            new_odd["teams"] = []

            i = 0
            for outcome in odds_type["outcomes"]:

                # Normalize the team names
                if outcome["description"] not in competitors:
                    outcome["description"] = competitors[odds_type["outcomes"].index(outcome)]

                ou = "O " if i == 0 else "U "

                new_odd["teams"].append({
                    "team": outcome["description"],
                    "val": ou + outcome["price"]["handicap"] + " (" + outcome["price"]["american"] + ")"
                })

                i += 1

            context["odds"].append(new_odd)

    return flask.jsonify(**context)
