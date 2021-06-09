import pandas as pd 
from datetime import datetime as dt 
# pybaseball package
from pybaseball import statcast
from pybaseball import statcast_pitcher
from pybaseball import playerid_lookup
from pybaseball.plotting import plot_stadium
from pybaseball.plotting import spraychart
from pybaseball.lahman import pitching
from pybaseball import schedule_and_record
from pybaseball import pitching_stats_range
from pybaseball.teamid_lookup import team_ids
from pybaseball.lahman import teams
from pybaseball.statcast_pitcher import statcast_pitcher_expected_stats 

# baseball-scraper package
from baseball_scraper import espn

# Data: Statcast 
# Overview: https://www.mlb.com/glossary/statcast 
# Package to pull data:
    # https://pypi.org/project/pybaseball/
# Other Packages considered: 
    # https://pypi.org/project/baseball-scraper/
    # https://pypi.org/project/vigorish/
# Useful source to compare packages:
    # https://snyk.io/advisor/python
    


############## Statcast data ##############
data = statcast(start_dt='2021-04-01', end_dt='2021-04-02', team='SEA')
data.loc[data.game_date == '2021-04-01',:]
data.head()

############## Team Crosswalk #############
team_cross = teams()
team_cross = team_ids()

############# Player Crosswalk ############
player = playerid_lookup('Sheffield', 'Justus')

############## Date Range #################
dt_lst = pd.date_range(start='2021-04-01', end='2021-05-31', freq='D')
dt_range = []
for i in dt_lst:
  dt_range.append(i.strftime('%Y-%m-%d'))


############### Pitcher Profile ##############
# Game by Game
# TODO remove data.GS filter if want to look at all pitchers ; for now just looking at starters
table_lst = []
for x in dt_range:
    data  = pitching_stats_range(start_dt=x, end_dt=x)
    data = data.loc[data.GS == 1,:]
    table_lst.append(data)

pitching = pd.concat(table_lst)


# Probable pitchers for upcoming games
# TODO build out a future frame and do incremental loads based on dynamic date ranges 
fut_pitchers = espn.ProbableStartersScraper(dt(2021,6,2), dt(2021,6,2)).scrape()
fut_pitchers[['First','Last']] = fut_pitchers.Name.str.split(expand=True)
# TODO match to home team - down sampling to mariners for time being to get main up and running
fut_pitchers = fut_pitchers.loc[fut_pitchers.Name.str.contains('Flexen'),:]



# Season stats ~ averages
# Get Pitcher profile per starter 
# TODO figure out how to impliment functions instead of all these loops
# def player_lookup(first, last):
#    foo = x.split(" ",2)
#     player = playerid_lookup(last, first)
#     return player_lookup

table_lst = []
for x in fut_pitchers.Name:
    data  = pitching_stats_range(start_dt=x, end_dt=x)
    table_lst.append(data)

tmp = pd.concat(table_lst)



# Main Table 
table_lst = []
for x in [2021]:
    data = schedule_and_record(season=x, team='SEA')
    data.loc[:,'year'] = x
    table_lst.append(data)

main_sea = pd.concat(table_lst)


