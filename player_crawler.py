import time
from bs4 import BeautifulSoup
from urllib.request import urlopen
import json, os, csv

# with open("data/player_list.csv", 'r+') as f:
#     players = list[csv.reader(f)]


with open("data/player_list.json", "r+") as f:
    players = json.load(f)

full_digits = len(str(len(players)))
def zero_pad(s, digit = full_digits):
    while len(s) < digit:
        s = "0" + s
    return s

for index, player in enumerate(players):
    if index < 404:
        continue
    u = player["href"]
    player_no = zero_pad(str(index+1))
    # u = "http://www.basketball-reference.com/players/j/jamesle01.html"
    print("Crawling data for player " + player_no + "_" + player["name-display"] + " at url:")
    print(u)

    r = urlopen(u).read()
    # soup = BeautifulSoup(r, "lxml")

    with open("data/players/" + player_no + "_" + player["id"] + ".html", "wb+") as f:
        f.write(r)

    # tables = soup.find_all("table")
    # for table in tables:

    time.sleep(1)
    # if index > 2:
    #     break
