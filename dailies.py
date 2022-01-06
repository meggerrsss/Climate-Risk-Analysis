#trying to collect all daily data from ECCC's tables into one mega table, per site ID
# site = https://dd.weather.gc.ca/climate/observations/daily/csv/ON/
# specific url example = https://dd.weather.gc.ca/climate/observations/daily/csv/ON/climate_daily_ON_6041109_1944-03_P1D.csv

import pandas as pd
from siteIDdb import findprov

def collectalldailies(siteID):
  folder = "https://dd.weather.gc.ca/climate/observations/daily/csv/"+ findprov(siteID)+"/"
  filenamefilter = "https://dd.weather.gc.ca/climate/observations/daily/csv/"+ findprov(siteID)+"/climate_daily_"+ findprov(siteID)+"_"+str(siteID)
  print(folder, filenamefilter)
  d = []
  for filename in folder:
    print(filename)
    if filename[0:84] == filenamefilter:
      return filename

  dailydata = pd.read_csv(siteIDurl)
  return sites 