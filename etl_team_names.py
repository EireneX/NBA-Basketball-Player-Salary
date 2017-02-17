import sqlite3
import csv
import glob

# connect to database
connection = sqlite3.connect('ETL/NBA_salary_analysis.db')

# set up constants
team_names = "team_names"
col_names_raw = ['key', 'name']
col_types = ['text','text']
col_names = ['"' + col_names_raw[i] +'"' for i in range(0,len(col_names_raw))]
print col_names

# create table : only need to create once
temp_list = []
for i in range(0, len(col_names)):
    temp_list.append(col_names[i] + ' ' + col_types[i])
print temp_list
query = '''create table {0} ({1}, PRIMARY KEY (key))'''
query = query.format(team_names, ','.join(temp_list))
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
        team_names_index = header.index('team_names')
        team_name_index = header.index('team_name')
        query = 'insert into {0}({1}) values ({2})'
        query = query.format(team_names, ','.join(col_names), ','.join('?' * len(col_names)))
        for row in reader:
            for name in row[team_names_index].split(','):
                to_insert = [name.lstrip()] + [row[team_name_index]]
                connection.execute(query, to_insert)

# commit changes and close connection
connection.commit()
connection.close()
