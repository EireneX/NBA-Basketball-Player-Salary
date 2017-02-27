import time
from bs4 import BeautifulSoup, Comment
from urllib.request import urlopen
import json, os.path, csv, re

def valid_filename(filename):
    return re.sub('[^\w\-_\. ]', '_', filename)

def norm_txt(txt):
    # return txt
    return re.sub('[\n,:▪]', '', txt).replace('\xa0', " ").strip()
    return re.sub(r'[^\w, ]', '', txt)

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
    player_id = player["id"]
    player_no = zero_pad(str(index+1))
    r = open("data/players/"+player_no+"_"+player_id+".html", "rb+").read()
    soup = BeautifulSoup(r, "lxml")

    profile_dict = {}

    profile_html = soup.find("div", id="info")
    profile_img = profile_html.find("img").get("src")
    profile = profile_html.find("div", {"itemtype": "http://schema.org/Person"})
    name = profile.find("h1")
    full_name = profile.find("p")

    profile_dict.update({"name": name.text, "full_name": full_name.find("strong").text.replace("\n","")})

    # print(profile_dict)

    nick_name = full_name.find_next_sibling("p")

    for p in nick_name.find_next_siblings("p"):
        attr = p.find("strong")
        if attr is None:
            for span in p.find_all("span"):
                profile_dict[norm_txt(span.get("itemprop"))] = norm_txt(span.text)
            profile_dict["height_weight"] = norm_txt(span.next_sibling)
            continue
        if "Position" in attr.text:
            profile_dict[norm_txt(attr.text)] = norm_txt(attr.next_sibling)
        else:
            profile_dict[norm_txt(attr.text)] = norm_txt(" ".join(item if isinstance(item,str) else item.text for item in attr.find_next_siblings()))
        print(profile_dict)

    # print(profile_dict)



    # print(">>> Parsing game stats for player: "+player_id)

    print()

    # if index > 0:
    #     break
    break