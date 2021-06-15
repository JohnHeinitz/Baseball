import pandas as pd 
from datetime import datetime as dt 
from datetime import timedelta
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


# set export path
path = r'C:\Users\JH\Documents\git\Baseball\Statcast\DataFiles'

# Create date range for function calls
dt_lst = pd.date_range(start='2021-04-01', end='2021-06-12', freq='D')
dt_range = []
for i in dt_lst:
  dt_range.append(i.strftime('%Y-%m-%d'))


# Statcast data
game_data = statcast(start_dt='2021-04-01', end_dt='2021-06-12', team='SEA')

# Team Crosswalk
team_history = teams()
team_fact    = team_ids()

# Pitching profile 
# Adjust data.GS == 1 to go beyond starting pitchers
table_lst = []
for x in dt_range:
    data  = pitching_stats_range(start_dt=x, end_dt=x)
    data = data.loc[data.GS == 1,:]
    table_lst.append(data)

pitching_history = pd.concat(table_lst)


# Pitcher fact 
table_lst = []
for x in pitching_history.Name:
    First, Last = x.split(sep=" ", maxsplit=1)
    foo = playerid_lookup(Last, First)
    table_lst.append(foo)

player_fact = pd.concat(table_lst)


# Future pitchers
# TODO build out a future frame and do incremental loads based on dynamic date ranges dt.today()
fut_pitchers = espn.ProbableStartersScraper(dt.today() + timedelta(1), dt.today() + timedelta(1)).scrape()


# Exports
game_data       .to_excel(path+'\\game_data.xlsx')
team_history    .to_excel(path+'\\team_history.xlsx')
team_fact       .to_excel(path+'\\team_fact.xlsx')
pitching_history.to_excel(path+'\\pitching_history.xlsx')
player_fact     .to_excel(path+'\\player_fact.xlsx')
fut_pitchers    .to_excel(path+'\\fut_pitchers.xlsx')




 


# TODO determine flow of frames above and build out a 'main' frame
# Get Pitcher profile per expected starter 
## table_lst = []
## for x in fut_pitchers.Name:
##     data  = pitching_stats_range(start_dt=x, end_dt=x)
##     table_lst.append(data)
## 
## tmp = pd.concat(table_lst)
## 
## 
## # Main Table 
## table_lst = []
## for x in [2021]:
##     data = schedule_and_record(season=x, team='SEA')
##     data.loc[:,'year'] = x
##     table_lst.append(data)
## 
## main_sea = pd.concat(table_lst)


