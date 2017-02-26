# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup, Comment
# from urllib.request import urlopen
# python 2
from urllib2 import urlopen
import csv, re

def valid_filename(filename):
    return re.sub('[^\w\-_\. ]', '_', filename)

def norm_txt(txt):
    # return txt
    return re.sub('[\n,:▪]', '', txt).replace('\xa0', " ").strip()
    return re.sub(r'[^\w, ]', '', txt)

# read all team information
with open("data/team_list.csv", "r+") as f:
    reader = csv.reader(f)
    teams = {row[0]: row[1] for row in reader if "team_href" not in row}


def regex_match(pattern, text_compare):
    try:
        return re.findall(pattern, text_compare)[0].strip()
    except IndexError:
        return ""

profile_keys = ["team_name", "location", "team_names", "seasons", "seasons_start", "seasons_end", "record", "playoff_appearances",
                 "championships"]
# python 3
# with open("data/team_profiles.csv", "w+", newline="") as f:
# python 2
with open("data/team_profiles.csv", "wb") as f:
    writer = csv.writer(f, delimiter=",")
    writer.writerow(profile_keys)

    # start parsing team information one by one
    for team_name, team_href in teams.items():

        r = open("data/teams/"+team_name+".html", "rb+").read()
        # python 3
        # soup = BeautifulSoup(r, "lxml")
        # python 2
        soup = BeautifulSoup(r, "html.parser")
        profile_dict = {}

        # Regex patterns for team info

        LOCATION_PATTERN = u'Location:([\s,A-Za-z]*)Team Name'
        TEAMNAMES_PATTERN = u'Team Names?:(.*)Season'
        SEASONS_PATTERN = u'Seasons?:[\s]*([0-9]*).*;'
        SEASONS_START_PATTERN = u'Seasons?:.*;([\s0-9-]*)to'
        SEASONS_END_PATTERN = u'Seasons?:.*to([\s0-9-]*)Record'
        RECORD_PATTERN = u'Records?:(.*)Playoff Appearance'
        PLAYOFF_PATTERN = u'Playoff Appearances?:([\s0-9]*).*Championship'
        CHAMPIONSHIPS_PATTERN = u'Championships?:([\s0-9]*).*More Team Info'

        profile_html = soup.find("div", id="info").find("div", id="meta").find("div", {"class":None})

        team_infotext = " ".join(profile_html.text.split('\n'))

        location = regex_match(LOCATION_PATTERN, team_infotext)
        team_names = regex_match(TEAMNAMES_PATTERN, team_infotext)
        seasons = regex_match(SEASONS_PATTERN, team_infotext)
        seasons_start = regex_match(SEASONS_START_PATTERN, team_infotext)
        seasons_end = regex_match(SEASONS_END_PATTERN, team_infotext)
        record = regex_match(RECORD_PATTERN, team_infotext).split("(")[0]
        playoff_appearances = regex_match(PLAYOFF_PATTERN, team_infotext)
        championships = regex_match(CHAMPIONSHIPS_PATTERN, team_infotext)

        for k in profile_keys:
            print(k, ":", eval(k))

        writer.writerow([eval(k) for k in profile_keys])


