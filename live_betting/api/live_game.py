"""REST API for getting game stats from ESPN."""
import re
from bs4 import BeautifulSoup
import lxml
import json
import requests
import live_betting


def live_game(sport, team):

    if sport == "football":
        new_sport = "nfl"
    # else if sport == "hockey":
    #     new_sport = "nhl"
    # else if sport == "football":
    #     new_sport = "nfl"
    else:
        new_sport = sport

    gameId = find_game_id(new_sport, team)

    url = "http://www.espn.com/" + new_sport + "/boxscore?gameId=" + gameId

    espn_html = requests.get(url).text
    soup = BeautifulSoup(espn_html, 'lxml')

    passing = soup.find(id="gamepackage-passing")
    rushing = soup.find(id="gamepackage-rushing")
    receiving = soup.find(id="gamepackage-receiving")

    try:
        for div in passing.find_all("span", {'class':'abbr'}):
            div.decompose()
        for div in rushing.find_all("span", {'class':'abbr'}):
            div.decompose()
        for div in receiving.find_all("span", {'class':'abbr'}):
            div.decompose()
        # passing.span["abbr"].decompose()
        # rushing.span["abbr"].decompose()
        # receiving.span["abbr"].decompose()
        print(passing)
        all = "<div>" + passing.prettify() + rushing.prettify() + receiving.prettify() + "</div>"
    except:
        all = "<div></div>"

    return all

def find_game_id(sport, team):

    gameId = "0"

    all_games = requests.get("http://www.espn.com/" + sport + "/bottomline/scores").text
    all_games = all_games.lower()

    i = 1
    while True:

        team_index = all_games.find("left" + str(i))
        if team_index == -1:
            break

        amp_index = all_games.find("&", team_index)

        # "left1=" = 6
        team_string = all_games[team_index + 6 : amp_index]

        if team in team_string:
            game_id_index = all_games.find("gameid", amp_index)
            amp2_index = all_games.find("&", game_id_index)

            # "gameId=" = 7
            gameId = all_games[game_id_index + 7 : amp2_index]
            break

        i += 1

    return gameId
