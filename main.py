##########################################################################################
# processing ECCC's climate normals data output into readable/callable chunks
# data can be found here : https://dd.weather.gc.ca/climate
# Meghan Green, 12/14/2021
##########################################################################################

import requests
import pandas as pd
import pprint 

siteid = 1016940
province = "BC"
# siteid can be found here: https://dd.weather.gc.ca/climate/observations/
sites = pd.read_csv("https://dd.weather.gc.ca/climate/observations/climate_station_list.csv")
sites.head()
# alternatively, print siteid as table with print(sites)

siteurl = "https://dd.weather.gc.ca/climate/observations/normals/csv/1981-2010/"+province+"/climate_normals_"+province+"_"+str(siteid)+"_1981-2010.csv"

#playing around with the example file to avoid pinging ECCC too much
f = open("example.csv")
contents = f.read()
f.close()
lontents = contents.split('\n')
#print(lontents[3:5])

#converting this mess to usable dataframes
title = lontents[0].strip()

filename = "example.csv"

###### IMPORTING DATAFRAMES #######
# frame subset based on data shown here: https://climate.weather.gc.ca/climate_normals/results_1981_2010_e.html?searchType=stnName&txtStationName=Victoria&searchMethod=contains&txtCentralLatMin=0&txtCentralLatSec=0&txtCentralLongMin=0&txtCentralLongSec=0&stnID=118&dispBack=0
metadata = pd.read_csv(filename, skiprows=[i for i in range(0,3)], skipfooter = 99, engine='python').transpose()
temperature = pd.read_csv(filename, skiprows=[i for i in range(0,13)], skipfooter = 82, engine='python').drop(labels=0, axis=0)
precipitation = pd.read_csv(filename, skiprows=[i for i in list(range(0,13)) + list(range(14,23))], skipfooter = 67, engine='python').drop(labels=0, axis=0)
daysmaxtemp = pd.read_csv(filename, skiprows=[i for i in list(range(0,13)) + list(range(14,38))], skipfooter = 60, engine='python').drop(labels=0, axis=0)
daysmintemp = pd.read_csv(filename, skiprows=[i for i in list(range(0,13)) + list(range(14,45))], skipfooter = 52, engine='python').drop(labels=0, axis=0)
dayswithrainfall = pd.read_csv(filename, skiprows=[i for i in list(range(0,13)) + list(range(14,53))], skipfooter = 47, engine='python').drop(labels=0, axis=0)
dayswithsnowfall = pd.read_csv(filename, skiprows=[i for i in list(range(0,13)) + list(range(14,58))], skipfooter = 42, engine='python').drop(labels=0, axis=0)
dayswithprecipitataion = pd.read_csv(filename, skiprows=[i for i in list(range(0,13)) + list(range(14,63))], skipfooter = 37, engine='python').drop(labels=0, axis=0)
dayswithsnowdepth = pd.read_csv(filename, skiprows=[i for i in list(range(0,13)) + list(range(14,68))], skipfooter = 32, engine='python').drop(labels=0, axis=0)
degreedays = pd.read_csv(filename, skiprows=[i for i in list(range(0,13)) + list(range(14,73))], skipfooter = 20, engine='python').drop(labels=0, axis=0)
evaporation = pd.read_csv(filename, skiprows=[i for i in list(range(0,13)) + list(range(14,85))], skipfooter = 18, engine='python').drop(labels=0, axis=0)
brightsunshine = pd.read_csv(filename, skiprows=[i for i in list(range(0,13)) + list(range(14,87))], skipfooter = 11, engine='python').drop(labels=0, axis=0)

print(brightsunshine)





#notes
# data not having every table is absolutely going to break this, as it's broken up by line numbers and named appropriately. 
# could possibly move the temperatures to one data frame then teased out to the chunks & keep months as heading
# need an example of a spot that doesn't have all data to test that out later, once everything from this is imported
