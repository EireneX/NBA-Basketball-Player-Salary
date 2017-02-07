import time
from bs4 import BeautifulSoup
from urllib.request import urlopen
import json, os, csv

def html_parser(html):
    tables = html.find_all("table")
    if (len(tables) > 0):
        table = html.find_all("table")[0]
        player_list = [{"id": td.get("data-append-csv"),
                        "name": td.get("csk"),
                        "name-display": td.text,
                        "href": base_url + td.find("a").get("href")}
                       for td in table.find_all("td", {"data-stat": "player"})]
        return player_list
    else:
        return None


base_url = "http://www.basketball-reference.com"
u = "http://www.basketball-reference.com/play-index/" \
    "psl_finder.cgi?request=1&match=combined&type=totals&per_minute_base=36&per_poss_base=100&lg_id=NBA&is_playoffs=N" \
    "&year_min=2006&year_max=2015&franch_id=&season_start=1&season_end=-1&age_min=0&age_max=99&shoot_hand=&height_min=0" \
    "&height_max=99&birth_country_is=Y&birth_country=&birth_state=&college_id=&draft_year=&is_active=&debut_yr_aba_start=" \
    "&debut_yr_aba_end=&debut_yr_nba_start=&debut_yr_nba_end=&is_hof=&is_as=&as_comp=gt&as_val=&award=&pos_is_g=Y&pos_is_gf=Y" \
    "&pos_is_f=Y&pos_is_fg=Y&pos_is_fc=Y&pos_is_c=Y&pos_is_cf=Y&qual=&c1stat=&c1comp=&c1val=&c2stat=&c2comp=&c2val=&c3stat=&c3comp=" \
    "&c3val=&c4stat=&c4comp=&c4val=&c5stat=&c5comp=&c6mult=1.0&c6stat=&order_by=ws&order_by_asc"
cnt = 5000
player_list = []

for i in range(0, cnt, 100):
    print (">>> Going to read player No.: " + str(i+1) + " to No. " + str(i+101) + " at url: " )
    url_100player = u + "&offset=" + str(i)
    print(url_100player)
    r = urlopen(url_100player).read()
    soup = BeautifulSoup(r, "lxml")
    player100 = html_parser(soup)

    if player100 is None:
        print(">>> END OF THE LIST")
        break
    else:
        print(">>> " + str(i + len(player100)) + " players information are found. Saving results web page...")
        player_list = player_list + player100
        with open("data/player_results" + str(i + len(player100)) + ".html", "wb+") as f:
            f.write(r)

    # time.sleep(0.1)

print("Last 3 players are:")
print(player_list[::-1][:3][::-1])

print("Writing results to player_list.json")
with open("data/player_list.json", "w+") as f:
    json.dump(player_list, f)

print("Writing results to player_list.csv")
with open("data/player_list.csv", "w+", newline='') as f:
    writer = csv.writer(f, delimiter=",")
    writer.writerow(["id", "name", "name-display", "href"])
    for p in player_list:
        writer.writerow([p["id"], p["name"], p["name-display"], p["href"]])

print("DONE!")
