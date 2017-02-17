import sqlite3
import csv
import glob

# connect to database
connection = sqlite3.connect('ETL/NBA_salary_analysis.db')

# set up constants
team_profiles = "team_profiles"
col_names_raw = ['team_name', 'location','team_names' ,'seasons','playoff_appearances','championships']
col_types = ['text','text','text','int','int','int']
col_names = ['"' + col_names_raw[i] +'"' for i in range(0,len(col_names_raw))]
print col_names

# create table : only need to create once
temp_list = []
for i in range(0, len(col_names)):
    temp_list.append(col_names[i] + ' ' + col_types[i])
print temp_list
query = '''create table {0} ({1}, PRIMARY KEY (team_name))'''
query = query.format(team_profiles, ','.join(temp_list))
print query
connection.execute(query)

# get paths & file names
file_paths = glob.glob("./data/team_profiles.csv")
print len(file_paths)

# loop through all files & insert stats into team_stats table
for i in range(0, len(file_paths)):
    with open(file_paths[i], 'r') as f:
        reader = csv.reader(f)
        header = reader.next()
        indexes = [header.index(col_name) for col_name in col_names_raw]
        query = 'insert into {0}({1}) values ({2})'
        query = query.format(team_profiles, ','.join(col_names), ','.join('?' * len(col_names)))
        for row in reader:
            lastCell = "N.A."
            to_insert = [row[index] for index in indexes]
            connection.execute(query, to_insert)

# commit changes and close connection
connection.commit()
connection.close()
