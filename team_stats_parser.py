import time
from bs4 import BeautifulSoup, Comment
from urllib.request import urlopen
import json, os.path, csv, re

def valid_filename(filename):
    return re.sub('[^\w\-_\. ]', '_', filename)

def parse_team_stats(team_name):
    for stats_id, table in tables_stats.items():
        print("Saving team "+team_name+"'stats: "+stats_id)
        thead = table.find_all("thead")[0]
        folder_path = "data/team_stats/"

        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)

        with open(folder_path+valid_filename(team_name+".csv"), "w+", newline="") as f:
            writer = csv.writer(f, delimiter=",")
            # write header
            writer.writerow([th.text for th in thead.find_all("tr")[-1].find_all("th")])
            # write stats
            tbody = table.find_all("tbody")[0]
            for tr in tbody.find_all("tr"):
                writer.writerow([ele.text for ele in tr.find_all(["th", "td"])])


# read all team information
with open("data/team_list.csv", "r+") as f:
    reader = csv.reader(f)
    teams = {row[0]: row[1] for row in reader if "team_href" not in row}


# start parsing player information one by one
for team_name, team_href in teams.items():

    tables_stats = {}

    r = open("data/teams/"+team_name+".html", "rb+").read()
    soup = BeautifulSoup(r, "lxml")

    tables_all = []

    # Extract all tables in non-comments
    table = soup.find("div", id="content").find("table")
    tables_all.append(table)

    # # Extract all tables in comments
    # comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    # for c in comments:
    #     soup_comment = BeautifulSoup(c, 'lxml')
    #     table = soup_comment.find('table')
    #     tables_all.append(table)

    for table in tables_all:
        tables_stats[table.get("id")] = table

    print(">>> Parsing stats for team: "+team_name)
    parse_team_stats(team_name)
    print()
