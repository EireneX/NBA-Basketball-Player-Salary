from bs4 import BeautifulSoup, Comment
# from urllib.request import urlopen
# python 2
from urllib2 import urlopen
import os.path, csv, re

def valid_filename(filename):
    return re.sub('[^\w\-_\. ]', '_', filename)


def norm_txt(txt):
    # removing non-ascii
    return re.sub(r'[^\x00-\x7F]+',' ', txt)


def parse_team_stats(team_name):
    for stats_id, table in tables_stats.items():
        print("Saving team "+team_name+"'stats: "+stats_id)
        thead = table.find_all("thead")[0]
        folder_path = "data/team_stats/"

        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)

        # python 3
        # with open(folder_path+valid_filename(team_name+".csv"), "w+", newline="") as f:
        # python 2
        with open(folder_path + valid_filename(team_name + ".csv"), "wb") as f:
            writer = csv.writer(f, delimiter=",")
            # write header
            writer.writerow([norm_txt(th.text) for th in thead.find_all("tr")[-1].find_all("th")])
            # write stats
            tbody = table.find_all("tbody")[0]
            for tr in tbody.find_all("tr"):
                writer.writerow([norm_txt(ele.text) for ele in tr.find_all(["th", "td"])])


# read all team information
with open("data/team_list.csv", "r+") as f:
    reader = csv.reader(f)
    teams = {row[0]: row[1] for row in reader if "team_href" not in row}


# start parsing player information one by one
for team_name, team_href in teams.items():

    tables_stats = {}

    r = open("data/teams/"+team_name+".html", "rb+").read()
    # python 3
    # soup = BeautifulSoup(r, "lxml")
    # python 2
    soup = BeautifulSoup(r, "html.parser")
    tables_all = []

    # Extract all tables in non-comments
    table = soup.find("div", id="content").find("table")
    tables_all.append(table)

    for table in tables_all:
        tables_stats[table.get("id")] = table

    print(">>> Parsing stats for team: "+team_name)
    parse_team_stats(team_name)
    print()
