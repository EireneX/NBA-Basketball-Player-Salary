This README file introduces the program structure and functionality.

Project Structure
-----------------

## This folder contains the k-means clustering source code & data for part 3.1
-- Cluster/
   -- Kmean.R         # k-means source code in R
   -- avgdata.csv     # k-means source data in csv

## This folder contains the k-means clustering source codes & data for part 3.1
-- ETL/
  -- NBA_salary_analysis.db   # sqlite database
  -- avgdata.csv              # data generated from DB for k-means clustering

## This folder contains Linear Regression source code & data for part 3.2
-- Linear Regression/
  -- linear regression.r      # linear regression source code in R
  -- stats.csv                # data generated from DB for linear regression

## This folder contains Panel Data Analysis source code & data for part 3.3
-- Panel_Data_Analysis
  -- R_Analysis.Rproj               # R project for Panel Data Analysis
  -- salaries_stats.RData           # R data used in this analysis
  -- salary_panel_data_analysis.R   # R analysis script
  -- hausman_tests.txt              # results
  -- pos_PG_final.txt               # ...
  -- pos_SF_final.txt               # ...
  -- pos_SG_final.txt               # ...
  -- pos_C_final.txt                # ...
  -- pos_PF_final.txt               # ...
  -- Salary_vs_Postions.png
  -- Salary_vs_Seasons.png

## this README file
-- README.txt           

## This folder contains all the data crawled and parsed in Part 1
-- data/
  -- players/              # player html files
  -- player_stats/         # player statistics csv files
  -- teams/                # team html files
  -- team_stats/           # team statistics csv files
  -- player_profiles.csv   # all players' profile in 1 csv file
  -- team_profiles.csv     # all teams' profile in 1 csv file
  -- player_list.csv       # list of players
  -- team_list.csv         # list of teams
  -- stats_glossary.csv    # statistics glossary

## These Python scripts are used to perform ETL for database creation
-- etl_player_salary.py
-- etl_player_stats.py
-- etl_team_names.py
-- etl_team_profiles.py
-- etl_team_stats.py

# Python script to generate the glossary for statistics short names
-- glossary.py

# Python source codes for Web Scraping: 1) crawling 2) Parsing of Player & Team data
-- player_all_crawler.py    # crawl search results & parse all player page links
-- player_crawler.py        # crawl all player pages
-- player_profile_parser.py # parse all player profile information
-- player_stats_parser.py   # parse all player statistics information
-- team_all_crawler.py      # crawl all team results & parse all team page links
-- team_crawler.py          # crawl all team pages
-- team_profile_parser.py   # parse all team profile information
-- team_stats_parser.py     # parse all team statistics information
