"""REST API for getting game stats from ESPN."""
import re
from bs4 import BeautifulSoup
import lxml
import json
import requests
import live_betting


def live_game(sport, team):

    from live_betting.model import CUR_STAT, update_stat

    if sport == "football":
        new_sport = "nfl"
        stat = CUR_STAT
        if stat == "passing":
            update_stat("rushing")
        elif stat == "rushing":
            update_stat("receiving")
        elif stat == "receiving":
            update_stat("passing")
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

    if stat == "passing":
        the_stat = soup.find(id="gamepackage-passing")
    elif stat == "rushing":
        the_stat = soup.find(id="gamepackage-rushing")
    elif stat == "receiving":
        the_stat = soup.find(id="gamepackage-receiving")

    try:
        for div in the_stat.find_all("span", {'class':'abbr'}):
            div.decompose()

        all = the_stat.prettify()
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
