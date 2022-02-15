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
  print(range(yr1, yr2))
  for yr in range(yr1, yr2+1):
    for i in range(12): #months
      fil = "climate_daily_" + prov + "_" + str(siteID) + "_" + str(yr) + "-" + str(i+1).zfill(2) + "_P1D.csv"
      yield fil

#need to add an error message if there's any missing days



def collectalldailies(siteID, years = [1981, 2010], limit=-1, method = 2, verbose = True):
  foldername = "https://dd.weather.gc.ca/climate/observations/daily/csv/" + findprov(
    siteID) + "/"  # string of location of all the files
  filenameprefix = "https://dd.weather.gc.ca/climate/observations/daily/csv/" + findprov(siteID) + "/climate_daily_" + findprov(siteID) + "_" + str(siteID)  #only want files that start with this

  if method == 1: 
    # opening the folder to list out the files, slow
    folder = requests.get(foldername, timeout=360)
    soup = BeautifulSoup(folder.text, 'html.parser')
  
    #fetching the data into a csv-ish list, which writes to file later (currently in main)
    years = range(1981, 2011) #unclear if assigning it here vs main makes more sense
    header = []
    data = []
    errors = []
    for link in soup.find_all('a'):
      href = link.get("href")
      #if len(href)>30 and href.endswith(".csv"): year = int(href[25:29])
      #print(year, year in years)
      if siteID in href and href.endswith(".csv") and int(href[25:29]) in years: 
        if verbose: print("fetching "+href)
        try:
          d = fetchECCC(foldername + href)
        except requests.exceptions.HTTPError:
          t = "Could not fetch :" + href
          if verbose: print(t)
          errors.append(t)
          continue
        if header == []: header = d[0]
        data += d[1:]
    data.insert(0,header)   
    with open('errorreport.txt', 'a') as f:
      for err in errors:
        f.write(str(err)+'\n')    
    return data


  if method == 2:
    header = []
    data = []
    errors = []
    print(years)
    for item in downloadlist(siteID, years[0], years[1]):
      if verbose: print("fetching: " + item)
      try:
        d = fetchECCC(foldername + item)
      except requests.exceptions.HTTPError as e:
        if verbose: print(e)
        errors.append(e)
        continue
      if header == []: header = d[0]
      data += d[1:]
    data.insert(0,header)  
    with open('errorreport.txt', 'a') as f:
      for err in errors:
        f.write(str(err)+'\n')    
    return data
  
  
  if verbose: print("finished collecting")

  #dailydata = pd.read_csv(siteIDurl)
  #return sites
