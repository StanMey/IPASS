from selenium import webdriver
from bs4 import BeautifulSoup
import time

test_url = "https://www.premierleague.com/results?co=1&se=79&cl=-1"


def get_match_id(url):
    """"""
    driver = webdriver.Firefox()
    driver.get(url)

    # the waiting time between a new scroll try
    SCROLL_PAUSE_TIME = 3

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        # check if maximum scroll height is found
        if new_height == last_height:
            break
        last_height = new_height

    time.sleep(2)
    html = driver.page_source
    soup = BeautifulSoup(html, features="html.parser")

    matches_list = []
    games = soup.findAll("div", {"class": "fixture postMatch"})
    for game in games:
        matches_list.append(game.attrs['data-matchid'])

    # close the applet and return all the match id's
    driver.close()
    return matches_list
