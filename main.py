import requests
import pandas as pd

siteid = 1016940
province = "BC"
# siteid can be found here: https://dd.weather.gc.ca/climate/observations/
# alternatively, print siteid as table 
sites = pd.read_csv("https://dd.weather.gc.ca/climate/observations/climate_station_list.csv")
sites.head()
#print(sites)

siteurl = "https://dd.weather.gc.ca/climate/observations/normals/csv/1981-2010/"+province+"/climate_normals_"+province+"_"+str(siteid)+"_1981-2010.csv"
print(siteurl)

df = pd.read_csv("siteurl")
print(df)
#attempting to save as DataFrame but too much space, trying as regular text file first

