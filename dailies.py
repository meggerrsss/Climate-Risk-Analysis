# trying to collect all daily data from ECCC's tables into one mega table, per site ID
# site = https://dd.weather.gc.ca/climate/observations/daily/csv/ON/
# specific url example = https://dd.weather.gc.ca/climate/observations/daily/csv/ON/climate_daily_ON_6041109_1944-03_P1D.csv

import pandas as pd
from siteIDdb import findprov
import requests
from bs4 import BeautifulSoup
from fetchdata import fetchECCC


def collectalldailies(siteID, limit=-1):
  foldername = "https://dd.weather.gc.ca/climate/observations/daily/csv/" + findprov(
    siteID) + "/"  # string of location of all the files
  filenameprefix = "https://dd.weather.gc.ca/climate/observations/daily/csv/" + findprov(siteID) + "/climate_daily_" + findprov(siteID) + "_" + str(siteID)  #only want files that start with this

  # opening the folder to list out the files
  folder = requests.get(foldername, timeout=360)
  soup = BeautifulSoup(folder.text, 'html.parser')
  
  #fetching the data into a csv-ish list, which writes to file later (currently in main)
  header = []
  data = []
  for link in soup.find_all('a'):
    href = link.get("href")
    if siteID in href and href.endswith(".csv"): 
      print("fetching "+href)
      d = fetchECCC(foldername + href)
      print(d[1:])
      if header == []: header = d[0]
      data += d[1:]
  data.insert(0,header)      
  return data
  print("finished collecting")

  #dailydata = pd.read_csv(siteIDurl)
  #return sites
