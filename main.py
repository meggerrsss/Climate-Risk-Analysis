import csv
from meghan import climatetable
import reports
from siteIDdb import findprov
from dailies import collectalldailies
from fetchdata import fetchECCC
#import graphdaily

def main():
  # importing from web https://dd.weather.gc.ca/climate/observations/
  #siteid = '6016527' #ottawa --- requesting list of datafiles is too slow to run
  siteid = '8300060' #pei 
  province = findprov(siteid)
  url = "https://dd.weather.gc.ca/climate/observations/normals/csv/1981-2010/" + province + "/climate_normals_" + province + "_" + siteid + "_1981-2010.csv"

  reader = fetchECCC(url)

  # this section imports all daily data at a specific site ID into a saved file
  dailydata = collectalldailies(siteid)
  with open("temporarydailydata.csv", 'w') as f:
    csvwriter = csv.writer(f)
    for line in dailydata:
      csvwriter.writerow(line)

  chunked_reader = climatetable(reader)
  reports.final_report(chunked_reader)

if __name__ == "__main__":
  main()