# trying to collect all daily data from ECCC's tables into one mega table, per site ID
# site = https://dd.weather.gc.ca/climate/observations/daily/csv/ON/
# specific url example = https://dd.weather.gc.ca/climate/observations/daily/csv/ON/climate_daily_ON_6041109_1944-03_P1D.csv

import pandas as pd
from siteIDdb import findprov
import requests

def collectalldailies(siteID):
  foldername = "https://dd.weather.gc.ca/climate/observations/daily/csv/" + findprov(siteID)+"/" # string of location of all the files
  filenameprefix = "https://dd.weather.gc.ca/climate/observations/daily/csv/"+ findprov(siteID) + "/climate_daily_" + findprov(siteID) + "_" + str(siteID) #only want files that start with this 

   # opening the folder to list out the files
  folder = requests.get(foldername, timeout=10)
  folder = folder.text.split('\n')[8:-4]  # head/food stuff eliminated

  #slicing each string scraped from the list of files to get all of their names
  for f in range(len(folder)):
    folder[f] = folder[f][49:-71]  # this will need to be better written for finding the a href characters lol

  print(folder[0])

  # apparently better to grow a list then convert to frame than it is to grow a frame?
  data = []
  for filename in folder:
    if filename[0:84] == filenameprefix:
      with os.scandir(filename) as d:
        data = data.append(d)
 
  print(data)   

  #dailydata = pd.read_csv(siteIDurl)
  #return sites 