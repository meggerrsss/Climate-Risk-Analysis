# trying to collect all daily data from ECCC's tables into one mega table, per site ID
# site = https://dd.weather.gc.ca/climate/observations/daily/csv/ON/
# specific url example = https://dd.weather.gc.ca/climate/observations/daily/csv/ON/climate_daily_ON_6041109_1944-03_P1D.csv

from siteIDdb import findprov
import requests
from bs4 import BeautifulSoup
from fetchdata import fetchECCC
from openconfig import openconfig


def downloadlist(yr1, yr2):
  # builds a list of file names to downbload from ECCC's daily climate data, using yr1,yr2 as an *inclusive* range of years to include
  prov = findprov(siteid)
  for yr in range(yr1, yr2+1):
    for i in range(12): #months
      fil = "climate_daily_" + prov + "_" + str(siteID) + "_" + str(yr) + "-" + str(i+1).zfill(2) + "_P1D.csv"
      yield fil

#need to add an error message if there's any missing days



def collectalldailies(siteid, years = [1981, 2010], limit=-1):
  openconfig()
  foldername = "https://dd.weather.gc.ca/climate/observations/daily/csv/" + findprov(
    siteid) + "/"  # string of location of all the files
  filenameprefix = "https://dd.weather.gc.ca/climate/observations/daily/csv/" + findprov(siteid) + "/climate_daily_" + findprov(siteid) + "_" + str(siteid)  #only want files that start with this

  if scrapemethod == 1: 
    # opening the folder to list out the files, slow
    folder = requests.get(foldername, timeout=360)
    soup = BeautifulSoup(folder.text, 'html.parser')
  
    #fetching the data into a csv-ish list, which writes to file later (later as in, in main)
    header = []
    data = []
    errors = []
    for link in soup.find_all('a'):
      href = link.get("href")
      if siteid in href and href.endswith(".csv") and int(href[25:29]) in years: 
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


  if scrapemethod == 2:
    # using the year range and siteid, create full paths from scratch and only get those, recommended, fast
    header = []
    data = []
    errors = []
    for item in downloadlist(years[0], years[1]):
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
