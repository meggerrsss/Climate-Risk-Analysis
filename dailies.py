# trying to collect all daily data from ECCC's tables into one mega table, per site ID
# site = https://dd.weather.gc.ca/climate/observations/daily/csv/ON/
# specific url example = https://dd.weather.gc.ca/climate/observations/daily/csv/ON/climate_daily_ON_6041109_1944-03_P1D.csv

import pandas as pd
from siteIDdb import findprov
import requests
from bs4 import BeautifulSoup


def collectalldailies(siteID, limit=-1):
  foldername = "https://dd.weather.gc.ca/climate/observations/daily/csv/" + findprov(siteID)+"/" # string of location of all the files
  filenameprefix = "https://dd.weather.gc.ca/climate/observations/daily/csv/"+ findprov(siteID) + "/climate_daily_" + findprov(siteID) + "_" + str(siteID) #only want files that start with this 

   # opening the folder to list out the files
  folder = requests.get(foldername, timeout=30)
  soup = BeautifulSoup(folder.text, 'html.parser')
  

  #some testing for name filtering
  intermediate = soup.find_all('a')
  print(intermediate.get('href'))
  #print(soup.find_all('a'))


  #for a in soup.findall(a):
  #requests.get(href)
  
  # apparently better to grow a list then convert to frame than it is to grow a frame?
  #data = []
  #for line in soup.find_all(a):
  #  filename = line.get('a href')
  #  if foldername+filename[0:84] == filenameprefix:
  #    with os.scandir(filename) as d:
  #     data = data.append(d)
  #     time.sleep(0.5)
  #     print(data)   

  #dailydata = pd.read_csv(siteIDurl)
  #return sites 