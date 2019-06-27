# import libraries
import urllib.request as req
from bs4 import BeautifulSoup
import time

# import other files
import csv_operations as dc
import pl_selenium_crawler as plsc


# the url for searching for a match
PRE_URL = "https://www.premierleague.com/match/"
# the url for searching for all the match id's for a specific season
results_url = "https://www.premierleague.com/results?co=1&se=27&cl=-1"


def gathering_match_info(page_url):
    """Gets all the needed info from a match from the website:
    e.g. 'https://www.premierleague.com/match/38640' and writes it into a dictionary"""

    # parsing the page
    web_page = req.urlopen(page_url)
    soup = BeautifulSoup(web_page, features="html.parser")

    match_info = {}

    # retrieving the teams and their formations from the site
    formations_container = soup.findAll("div", {"class": "position"})
    is_home_team = True
    for div in formations_container:
        text = div.text.strip().split(" ")

        if is_home_team:
            # if it is the first team i.o.w the home team
            match_info['home_team'] = text[0].replace('\n', '')
            for i in range(1, len(text) - 1):
                if text[i] != '':
                    match_info['home_team'] += " {0}".format(text[i].replace('\n', ''))
                else:
                    break
            # match_info['home_team'] = " ".join(text[:len(text) - 1])
            match_info['home_formation'] = text[-1]
            is_home_team = False
        else:
            # it's the second team
            match_info['away_team'] = text[0].replace('\n', '')
            for i in range(1, len(text) - 1):
                if text[i] != '':
                    match_info['away_team'] += " {0}".format(text[i].replace('\n', ''))
                else:
                    break
            match_info['away_formation'] = text[-1]

    # retrieving the game score
    score_container = soup.find("div", {"class": "score fullTime"})
    game_score = score_container.text.strip().split("-")
    match_info['home_score'] = game_score[0]
    match_info['away_score'] = game_score[1]

    # retrieving the matchdate
    game_date = soup.title.text.split(", ")[-1].split(" | ")
    match_info['season'] = game_date[0]
    match_info['league'] = game_date[1]

    # return the dictionary with all the information
    print(match_info)
    return match_info


# main
if __name__ == '__main__':
    # get a list of all the id's
    matches_list = plsc.get_matches_id_list(results_url)

    #
    matches_info_list = []
    count = 0
    for match in matches_list:
        matches_info_list.append(gathering_match_info(PRE_URL + match))
        time.sleep(1)
        print(count)
        count += 1

    # write all the matches into a csv file
    season_date = "PL_season_{0}.csv".format(matches_info_list[0]['season'].replace('/', '-'))
    dc.match_data_to_csv(matches_info_list, season_date)
