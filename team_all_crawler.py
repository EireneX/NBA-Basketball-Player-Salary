from bs4 import BeautifulSoup
# python 3
# from urllib.request import urlopen
# python 2
from urllib2 import urlopen
import csv


base_url = "http://www.basketball-reference.com"
u = "http://www.basketball-reference.com/teams/"

r = urlopen(u).read()
# python 3
# soup = BeautifulSoup(r, "lxml")
# python 2
soup = BeautifulSoup(r, "html.parser")
tbody = soup.find("table", id="teams_active").find("tbody")

print("Writing to team names & team urls to team_list.csv...")
# python 3
# with open("data/team_list.csv", "w+", newline="") as f:
with open("data/team_list.csv", "wb") as f:
    writer = csv.writer(f, delimiter=",")
    writer.writerow(["team_name", "team_href"])
    for a in tbody.find_all("a"):
        team_href = a.get("href")
        team_name = a.text
        print("Found team "+team_name+" at "+base_url+team_href)
        writer.writerow([team_name, base_url+team_href])
