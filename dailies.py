# trying to collect all daily data from ECCC's tables into one mega table, per site ID
# site = https://dd.weather.gc.ca/climate/observations/daily/csv/ON/
# specific url example = https://dd.weather.gc.ca/climate/observations/daily/csv/ON/climate_daily_ON_6041109_1944-03_P1D.csv

import pandas as pd
from siteIDdb import findprov
import requests
from bs4 import BeautifulSoup
from fetchdata import fetchECCC


def downloadlist(siteID, yr1, yr2):
  # builds a list of file names to downbload from ECCC's daily climate data, using yr1,yr2 as an *inclusive* range of years to include
  prov = findprov(siteID)
  for yr in range(yr1, yr2+1):
    for i in range(12): #months
      fil = "climate_daily_" + prov + "_" + str(siteID) + "_" + str(yr) + "-" + str(i+1).zfill(2) + "_P1D.csv"
      yield fil

#need to add an error message if there's any missing days



def collectalldailies(siteID, limit=-1, method = 1):
  foldername = "https://dd.weather.gc.ca/climate/observations/daily/csv/" + findprov(
    siteID) + "/"  # string of location of all the files
  filenameprefix = "https://dd.weather.gc.ca/climate/observations/daily/csv/" + findprov(siteID) + "/climate_daily_" + findprov(siteID) + "_" + str(siteID)  #only want files that start with this

  if method == 1: 
    # opening the folder to list out the files
    folder = requests.get(foldername, timeout=360)
    soup = BeautifulSoup(folder.text, 'html.parser')
  
    #fetching the data into a csv-ish list, which writes to file later (currently in main)
    years = range(1981, 2011) #unclear if assigning it here vs main makes more sense
    header = []
    data = []
    for link in soup.find_all('a'):
      href = link.get("href")
      #if len(href)>30 and href.endswith(".csv"): year = int(href[25:29])
      #print(year, year in years)
      if siteID in href and href.endswith(".csv") and int(href[25:29]) in years: 
        print("fetching "+href)
        try:
          d = fetchECCC(foldername + href)
        except requests.exceptions.HTTPError:
          print("Could not fetch :" + href)
          continue
        if header == []: header = d[0]
        data += d[1:]
    data.insert(0,header)      
    return data


  if method == 2:
    header = []
    data = []
    errors = []
    for item in downloadlist(siteID, 1981, 2021):
      print("fetching: " + item)
      try:
        d = fetchECCC(foldername + item)
      except requests.exceptions.HTTPError as e:
        print(e)
        errors.append(e)
        continue
      if header == []: header = d[0]
      data += d[1:]
    data.insert(0,header)      
    return data
  print("finished collecting")

  #dailydata = pd.read_csv(siteIDurl)
  #return sites
