"""REST API for getting game stats from ESPN."""
import re
from bs4 import BeautifulSoup
import lxml
import json
import requests
import live_betting


def live_game(sport, team):

    from live_betting.model import CUR_STAT, update_stat

    stat = ""
    new_sports = []

    team = team.replace(" ", "%20")
    print(team)

    if sport == "football":
        new_sports = ["nfl", "college-football"]
        stat = CUR_STAT
        if stat == "passing":
            update_stat("rushing")
        elif stat == "rushing":
            update_stat("receiving")
        else:
            update_stat("passing")
    elif sport == "basketball":
        new_sports = ["nba", "mens-college-basketball"]
        stat = CUR_STAT
        if stat == "home":
            update_stat("away")
        else:
            update_stat("home")
    # elif sport == "football":
    #     new_sport = "nfl"
    else:
        new_sport = [sport]

    gameId, new_sport = find_game_id(new_sports, team)
    print(gameId, new_sport)

    url = "http://www.espn.com/" + new_sport + "/boxscore?gameId=" + gameId

    espn_html = requests.get(url).text
    soup = BeautifulSoup(espn_html, 'lxml')

    # Football
    if stat == "passing":
        the_stat = soup.find(id="gamepackage-passing")
    elif stat == "rushing":
        the_stat = soup.find(id="gamepackage-rushing")
    elif stat == "receiving":
        the_stat = soup.find(id="gamepackage-receiving")

    # Basketball
    elif stat == "away":
        the_stat = soup.find(class_="gamepackage-away-wrap")
    elif stat == "home":
        the_stat = soup.find(class_="gamepackage-home-wrap")

    try:
        for div in the_stat.find_all("span", {'class':'abbr'}):
            div.decompose()

        all = the_stat.prettify()
    except:
        all = "<div></div>"

    return all

def find_game_id(sports, team):

    gameId = "0"
    found = False
    ret_sport = ""

    # Ex- basketball could give 'nba' or 'mens-college-basketball'
    for sport in sports:
        all_games = requests.get("http://www.espn.com/" + sport + "/bottomline/scores").text
        all_games = all_games.lower()

        ret_sport = sport

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
                found = True
                break

            i += 1

        if found:
            break

    return gameId, ret_sport
