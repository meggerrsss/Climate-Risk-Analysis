import requests
import pandas as pd

siteid = 6016527
# siteid can be found here: https://dd.weather.gc.ca/climate/observations/
# alternatively, print siteid as table 
sites = pd.from_csv(("https://dd.weather.gc.ca/climate/observations/climate_station_list.csv")
sites.head()


df = pd.from_csv("https://dd.weather.gc.ca/climate/observations/normals/csv/1981-2010/ON/climate_normals_ON_6016527_1981-2010.csv")
df.head()

