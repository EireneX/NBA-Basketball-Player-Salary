import time
from bs4 import BeautifulSoup
from urllib.request import urlopen
import json, os, csv


base_url = "http://www.basketball-reference.com"
u = "http://www.basketball-reference.com/teams/"
cnt = 5000
player_list = []

r = urlopen(u).read()
soup = BeautifulSoup(r, "lxml")
tbody = soup.find("table", id="teams_active").find("tbody")
with open("data/team_list.csv", "w+", newline="") as f:
    writer = csv.writer(f, delimiter=",")
    writer.writerow(["team_name", "team_href"])
    for a in tbody.find_all("a"):
        team_href = a.get("href")
        team_name = a.text
        writer.writerow([team_name, base_url+team_href])
