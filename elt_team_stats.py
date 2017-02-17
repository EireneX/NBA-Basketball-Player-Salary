import sqlite3
import csv
import glob

# connect to database
connection = sqlite3.connect('ETL/NBA_salary_analysis.db')

# set up constants
team_stats = "team_stats"
season_column_name = "Season"
col_names_raw = ['team_name', 'Season' ,'Team','W','L','W/L%','Finish','SRS','Pace','Rel_Pace','ORtg','Rel_ORtg','DRtg','Rel_DRtg','Playoffs','Coaches','Top WS']
col_types = ['text','int','text','int', 'int','real','int','real','real','real','real','real','real','real','text', 'text','text']
col_names = ['"' + col_names_raw[i] +'"' for i in range(0,len(col_names_raw))]
print col_names

# create table : only need to create once
temp_list = []
for i in range(0, len(col_names)):
    temp_list.append(col_names[i] + ' ' + col_types[i])
print temp_list
query = '''create table {0} ({1}, PRIMARY KEY (team_name, Season))'''
query = query.format(team_stats, ','.join(temp_list))
print query
connection.execute(query)

# get paths & file names
file_paths = glob.glob("./data/team_stats/*.csv")
print len(file_paths)

# loop through all files & insert stats into team_stats table
for i in range(0, len(file_paths)):
    with open(file_paths[i], 'r') as f:
        team_name = str(file_paths[i].split('/')[-1].split('.')[0])
        print "inserting stats for " + team_name
        reader = csv.reader(f)
        header = reader.next()
        indexes = [header.index(col_name) for col_name in col_names_raw[2:16]]
        season_col_index = header.index(season_column_name)
        query = 'insert into {0}({1}) values ({2})'
        query = query.format(team_stats, ','.join(col_names), ','.join('?' * len(col_names)))
        for row in reader:
            season = int(row[season_col_index].split('-')[0])
            if 2005 <= season <= 2014:
                # lastCell = str(row[-1]).encode('utf8')
                lastCell = "N.A."
                to_insert = [team_name] + [season] + [row[index] for index in indexes] + [lastCell]
                connection.execute(query, to_insert)

# commit changes and close connection
connection.commit()
connection.close()
