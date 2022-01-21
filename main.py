import csv
from from_normals import climatetable
import reports
from siteIDdb import findprov
from dailies import collectalldailies
from fetchdata import fetchECCC
from graphdaily import runplot

def main(siteid, scrapedailies = False, climatenormals = True, rplot = False):
  # importing from web https://dd.weather.gc.ca/climate/observations/
  #siteid = '6016527' #ottawa --- requesting list of datafiles is too slow to run
  #siteid = '8300060' #pei 
    
  print("siteid: ", siteid)
  province = findprov(siteid)
  print("province: ", province)
  normalsurl = "https://dd.weather.gc.ca/climate/observations/normals/csv/1981-2010/" + province + "/climate_normals_" + province + "_" + siteid + "_1981-2010.csv"

  normalsreader = fetchECCC(normalsurl)

  #scrapedailies = True 
  years = [1981, 2010]
  print("scrape daily data? ", scrapedailies)
  if scrapedailies:
    # build filename based off siteID
  # this section imports all daily data from ECCC at a specific site ID into a saved file, currently very slow for non-PEI siteIDs
    dailydata = collectalldailies(siteid, years = years, method=2)
    with open("temporarydailydata.csv", 'w') as f:
      csvwriter = csv.writer(f)
      for line in dailydata:
        csvwriter.writerow(line)
    print("file written")
  if rplot: 
    if not scrapedailies: print("plotting without downloading fresh...")
    runplot()
    


  if climatenormals:
    #data entirely from the climate normals summaries
    print("scraping from climate normals pages...")
    chunked_reader = climatetable(normalsreader)
    reports.final_report(chunked_reader, 'temporarydailydata.csv')

if __name__ == "__main__":
  # ARGUMENTS REMINDER 
  # siteid, scrapedailies = False, climatenormals = True, rplot = False

  # PEI can scrape data but not use the climate normals (yet)
  main('8300300', False, True, False)

  #main('6016527', True, False, False)

  # if rerunning from data that already exists
  #main('8300300', False, False, True)

  # OTT can use the climate normals but not scrape data (timeout error)
  #main('6016527', False, True, False)
  # change line 40 from str to csv for csv output demo

  #main('2101300', True, False, False)
