import time
from bs4 import BeautifulSoup, Comment
from urllib.request import urlopen
import json, os.path, csv, re

def valid_filename(filename):
    return re.sub('[^\w\-_\. ]', '_', filename)

def parse_player_common(player_no, player_id, tables):
    pass

def parse_player_stats(player_no, player_id):
    for stats_id, table in tables_stats.items():
        print("Saving player "+player_id+"'stats: "+stats_id)
        thead = table.find_all("thead")[0]
        folder_path = "data/player_stats/"+player_no+"_"+player_id+"/"

        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)

        with open(folder_path+valid_filename(player_no+"_"+player_id+"_"+stats_id+".csv"), "w+", newline="") as f:
            writer = csv.writer(f, delimiter=",")
            # write header
            writer.writerow([th.text for th in thead.find_all("tr")[-1].find_all("th")])
            # write stats
            tbody = table.find_all("tbody")[0]
            for tr in tbody.find_all("tr"):
                writer.writerow([ele.text for ele in tr.find_all(["th", "td"])])

        # write stats summary
        with open(folder_path+valid_filename(player_no+"_"+ player_id+"_"+stats_id+"_summary.csv"), "w+", newline="") as f:
            writer = csv.writer(f, delimiter=",")
            # write header
            writer.writerow([th.text for th in thead.find_all("tr")[-1].find_all("th")])
            # write stats summary
            tfoot = table.find_all("tfoot")
            if len(tfoot) >0 : tfoot = tfoot[0]
            else: continue
            for tr in tfoot.find_all("tr"):
                if tr.get("class") is not None and 'blank_table' in tr.get("class"):
                    continue
                writer.writerow([ele.text for ele in tr.find_all(["th", "td"])])

def parse_player_leaderboard(player_no, player_id):
    for table in tables_leaderboard:
        leaderboard_type = table.find_all("caption")[0].text
        print("Saving player " + player_id + "'s leaderboard stats: " + leaderboard_type)
        folder_path = "data/player_stats/" + player_no + "_" + player_id + "/"

        with open(folder_path+valid_filename(player_no+"_"+player_id+"_"+leaderboard_type+".csv"), "w+", newline="") as f:
            writer = csv.writer(f, delimiter=",")
            # write header
            writer.writerow([leaderboard_type])
            # write stats
            for tr in table.find_all("tr"):
                writer.writerow([" ".join([ele.text for ele in tr.find_all("td")])])

def parse_player_salary(player_no, player_id):
    for stats_id, table in tables_salaries.items():
        if "salar" not in stats_id:
            continue
        print("Saving player "+player_id+"'salary stats: "+stats_id)
        thead = table.find_all("thead")[0]
        folder_path = "data/player_stats/"+player_no+"_"+player_id+"/"

        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)

        with open(folder_path+valid_filename(player_no+"_"+player_id+"_"+stats_id+".csv"), "w+", newline="") as f:
            writer = csv.writer(f, delimiter=",")
            # write header
            writer.writerow([th.text for th in thead.find_all("tr")[-1].find_all("th")])
            # write stats
            tbody = table.find_all("tbody")[0]
            for tr in tbody.find_all("tr"):
                writer.writerow([ele.text for ele in tr.find_all(["th", "td"])])

        # write stats summary
        with open(folder_path+valid_filename(player_no+"_"+ player_id+"_"+stats_id+"_summary.csv"), "w+", newline="") as f:
            writer = csv.writer(f, delimiter=",")
            # write header
            writer.writerow([th.text for th in thead.find_all("tr")[-1].find_all("th")])
            # write stats summary
            tfoot = table.find_all("tfoot")
            if len(tfoot) >0 : tfoot = tfoot[0]
            else: continue
            for tr in tfoot.find_all("tr"):
                if tr.get("class") is not None and 'blank_table' in tr.get("class"):
                    continue
                writer.writerow([ele.text for ele in tr.find_all(["th", "td"])])


# read all player information
with open("data/player_list.json", "r+") as f:
    players = json.load(f)

full_digits = len(str(len(players)))

def zero_pad(s, digit = full_digits):
    while len(s) < digit:
        s = "0" + s
    return s

# start parsing player information one by one
for index, player in enumerate(players):

    tables_stats = {}
    tables_leaderboard = []
    tables_salaries = {}

    player_id = player["id"]
    player_no = zero_pad(str(index+1))
    r = open("data/players/"+player_no+"_"+player_id+".html", "rb+").read()
    soup = BeautifulSoup(r, "lxml")

    tables_all = []

    # Extract all tables in non-comments
    tables = soup.find_all("table")
    tables_all = tables_all + tables

    # Extract all tables in comments
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    for c in comments:
        soup_comment = BeautifulSoup(c, 'lxml')
        tables = soup_comment.find_all('table')
        tables_all = tables_all + tables

    # table_ids are in 3 categories:
    # 1) stats
    # 2) leaderboard related (table_id = None)
    # 3) Salary, Contract Salary information

    for table in tables_all:
        id = table.get("id")
        if id is None:
            tables_leaderboard.append(table)
        elif id == "all_salaries" or "contract" in id:
            tables_salaries[id] = table
        else:
            tables_stats[id] = table

    # Parse player stats data:
    # Output: playerNum_playerId_statsID.csv
    # col1, col2, col3, ...


    print(">>> Parsing game stats for player: "+player_id)
    parse_player_stats(player_no, player_id)
    print()

    print(">>> Parsing leadership stats for player: " + player_id)
    parse_player_leaderboard(player_no, player_id)
    print()

    print(">>> Parsing leadership stats for player: " + player_id)
    parse_player_salary(player_no, player_id)
    print()
