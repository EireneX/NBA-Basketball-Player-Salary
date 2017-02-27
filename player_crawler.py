import time
# python 3
# from urllib.request import urlopen
# python 2
from urllib2 import urlopen
import json

with open("data/player_list.json", "r+") as f:
    players = json.load(f)

full_digits = len(str(len(players)))
def zero_pad(s, digit = full_digits):
    while len(s) < digit:
        s = "0" + s
    return s

for index, player in enumerate(players):
    u = player["href"]
    player_no = zero_pad(str(index+1))
    print("Crawling data for player " + player_no + "_" + player["name-display"] + " at url:")
    print(u)

    r = urlopen(u).read()

    with open("data/players/" + player_no + "_" + player["id"] + ".html", "wb+") as f:
        f.write(r)

    time.sleep(1)

