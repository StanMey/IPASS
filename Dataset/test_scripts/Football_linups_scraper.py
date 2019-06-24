# https://www.football-lineups.com/tourn/Eredivisie_2017-2018/Fixture/
# import libraries
import urllib.request
import random
import re
from bs4 import BeautifulSoup

# url to the site
url = "https://www.football-lineups.com/match/264326/"
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
request = urllib.request.Request(url, headers={'User-Agent': user_agent})
response = urllib.request.urlopen(request)
html = response.read()

# showing the title
soup = BeautifulSoup(html, features="html.parser")
print(soup.title)

# searching for the lineups
match_teams = "23"
print(match_teams)

for tag in soup.find_all('a', re.compile("/tactic/")):
    print(tag)

# searching for the club names
# club_names = soup.
