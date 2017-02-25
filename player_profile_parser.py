# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup, Comment
# python 3
# from urllib.request import urlopen
# python 2
from urllib2 import urlopen
import json, csv, re
from io import open

def norm_txt(txt):
    # removing non-ascii
    return re.sub(r'[^\x00-\x7F]+',' ', txt)

# read all player information
with open("data/player_list.json", "r+") as f:
    players = json.load(f)

full_digits = len(str(len(players)))

def zero_pad(s, digit = full_digits):
    while len(s) < digit:
        s = "0" + s
    return s

def regex_match(pattern, text_compare):
    try:
        return re.findall(pattern, text_compare)[0].strip()
    except IndexError:
        return ""

profile_keys = ["player_id", "positions", "height", "weight", "shoots", "team", "birthday", "birthyear",
                 "birth_place", "debut_date", "experience"]

# python 3
# with open("data/player_profiles.csv", "w+", newline="") as f:
with open("data/player_profiles.csv", "wb") as f:
    writer = csv.writer(f, delimiter=",")
    writer.writerow([k for k in profile_keys])

    # start parsing player information one by one
    for index, player in enumerate(players):
        player_id = player["id"]
        player_no = zero_pad(str(index+1))
        r = open("data/players/"+player_no+"_"+player_id+".html", "rb+").read()
        # python 3
        # soup = BeautifulSoup(r, "lxml")
        # python 2
        soup = BeautifulSoup(r, "html.parser")

        profile_dict = {}

        # Regex patterns for player info
        POSN_PATTERN = u'Position:(.*?)\u25aa'
        HEIGHT_PATTERN = u'([0-9]-[0-9]{1,2})'
        WEIGHT_PATTERN = u'([0-9]{2,3})lb'
        SHOOTS_PATTERN = u'Shoots: ([\s,A-Za-z]*)'
        TEAM_PATTERN = u'Team:(.*?)Born'
        DEBUT_PATTERN = u'NBA Debut:(.*?\d{4})'
        EXPERIENCE_PATTERN = u'Experience:([\s0-9]*)'

        profile_html = soup.find("div", {"itemtype": "http://schema.org/Person"})

        player_infotext = " ".join(profile_html.text.split('\n'))

        positions = regex_match(POSN_PATTERN, player_infotext).split(" and ")
        height = regex_match(HEIGHT_PATTERN, player_infotext)
        weight = regex_match(WEIGHT_PATTERN, player_infotext)
        shoots = regex_match(SHOOTS_PATTERN, player_infotext)
        team = regex_match(TEAM_PATTERN, player_infotext)
        birthday = profile_html.find("a", href=re.compile(r'birthdays')).text.strip()
        birthyear = profile_html.find("a", href=re.compile(r'birthyears')).text.strip()
        birth_place = norm_txt(profile_html.find("span", itemprop='birthPlace').text.replace("in", "").strip())
        debut_date = regex_match(DEBUT_PATTERN, player_infotext)
        experience = regex_match(EXPERIENCE_PATTERN, player_infotext)

        print(positions, height, weight, shoots, team, birthday, birthyear, birth_place, debut_date, experience)

        writer.writerow([eval(k) for k in profile_keys])

