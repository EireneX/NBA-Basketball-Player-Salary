import time
# from urllib.request import urlopen
# python 2
from urllib2 import urlopen
import csv


with open("data/team_list.csv", "r+") as f:
    reader = csv.reader(f)
    teams = {row[0]: row[1] for row in reader if "team_href" not in row}

for name, href in teams.items():
    print("Crawling data for team " + name + " at url:")
    print(href)

    r = urlopen(href).read()

    with open("data/teams/" + name + ".html", "wb+") as f:
        f.write(r)

    time.sleep(1)
