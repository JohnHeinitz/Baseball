import pandas as pd 
from pybaseball import statcast



# Data: Statcast 
# Overview: https://www.mlb.com/glossary/statcast 
# Package to pull data:
    # https://pypi.org/project/pybaseball/
# Other Packages considered: 
    # https://pypi.org/project/baseball-scraper/
    # https://pypi.org/project/vigorish/
# Useful source to compare packages:
    # https://snyk.io/advisor/python
    

data = statcast(start_dt='2017-06-24', end_dt='2017-06-24')

