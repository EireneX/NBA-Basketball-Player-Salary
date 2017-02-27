import sqlite3
import csv
import os
import re

# if more than one team in one season, use TOT stats
# create player_stats table based on per 36 min data
# composite primary keys: player_id & season(stored as int using the first year)

# connect to database
connection = sqlite3.connect('ETL/NBA_salary_analysis.db')

# set up constants
player_stats = "player_stats"
season_column_name = "Season"
col_names_raw = ["player_id","Season", "Pos","G",'GS','MP','FG','FGA','FG%','3P','3PA','3P%','2P','2PA','2P%','FT','FTA','FT%','ORB','DRB','TRB','AST','STL','BLK','TOV','PF','PTS']
col_types = ['text', 'int', "text",'real','real','real','real','real','real','real','real','real','real','real','real','real','real','real','real','real','real','real','real','real','real','real','real']
col_names = ['"' + col_names_raw[i] +'"' for i in range(0,len(col_names_raw))]
print col_names

# create table : only need to create once
temp_list = []
for i in range(0, len(col_names)):
    temp_list.append(col_names[i] + ' ' + col_types[i])
print temp_list
query = '''create table {0} ({1}, PRIMARY KEY (player_id, Season))'''
query = query.format(player_stats, ','.join(temp_list))
print query
connection.execute(query)

# get paths & file names of all per 36 min csv files
STATS_FILE_PATTERN = r'[0-9]{4}_([a-z]+[0-9]+)_per_minute[^a-z]{1}csv'
file_paths = []
file_names = []
for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        matchObject = re.match(STATS_FILE_PATTERN, name)
        if matchObject is not None:
            file_names.append(name)
            file_paths.append(os.path.join(root, name))
print len(file_paths)

# loop through all files & insert stats into player_stats table
for i in range(0, len(file_paths)):
    with open(file_paths[i], 'r') as f:
        player_id = re.match(STATS_FILE_PATTERN, file_names[i]).group(1)
        print "inserting stats for " + player_id
        reader = csv.reader(f)
        header = reader.next()
        indexes = [header.index(col_name) for col_name in col_names_raw[2:]]
        season_col_index = header.index(season_column_name)
        query = 'insert into {0}({1}) values ({2})'
        query = query.format(player_stats, ','.join(col_names), ','.join('?' * len(col_names)))
        season_list = []
        for row in reader:
            season = int(row[season_col_index].split('-')[0])
            if season not in season_list and 2005 <= season <= 2014: # only insert TOT stats if multiple teams in one season
                season_list.append(season)
                to_insert = [player_id] + [season] + [row[index] for index in indexes]
                connection.execute(query, to_insert)

# commit changes and close connection
connection.commit()
connection.close()
