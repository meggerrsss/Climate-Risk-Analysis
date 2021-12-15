#############
# processing ECCC's climate normals data output into readable/callable chunks
# data can be found here : https://dd.weather.gc.ca/climate


import requests
import pandas as pd
import pprint 

siteid = 1016940
province = "BC"
# siteid can be found here: https://dd.weather.gc.ca/climate/observations/
# alternatively, print siteid as table 
sites = pd.read_csv("https://dd.weather.gc.ca/climate/observations/climate_station_list.csv")
sites.head()
#print(sites)

siteurl = "https://dd.weather.gc.ca/climate/observations/normals/csv/1981-2010/"+province+"/climate_normals_"+province+"_"+str(siteid)+"_1981-2010.csv"
#print(siteurl)

#playing around with the example file to avoid pinging ECCC too much
f = open("example.csv")
contents = f.read()
f.close()
lontents = contents.split('\n')
#print(lontents[3:5])

#converting this mess to usable dataframes
title = lontents[0].strip()
#metadata = pd.DataFrame([sub.split(",") for sub in lontents[3:5]])
#print(metadata)

metadata = pd.read_csv("example.csv", skiprows=[i for i in range(0,3)], skipfooter = 99, engine='python').transpose()
temperature = pd.read_csv("example.csv", skiprows=[i for i in range(0,13)], skipfooter = 82, engine='python')

print(temperature)


#df = pd.read_csv("siteurl")
#print(df)
#attempting to save as DataFrame but too much space, trying as regular text file first

