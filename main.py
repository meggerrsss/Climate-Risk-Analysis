import csv
from from_normals import climatetable
import reports
from siteIDdb import findprov
from fetchdailies import collectalldailies
from fetchdata import fetchECCC
from graphdaily import runplot
import pandas as pd
import tomli

def main():
  # importing from web https://dd.weather.gc.ca/climate/observations/ 

  # importing from config file, call arguments like 
  with open("config.toml", "rb") as f:
    config = tomli.load(f)

  # converting each line in config.toml to its own variable name
  for sett in config.keys():
    #exec("{0} = {1}".format(sett,config[sett]))
    globals()[sett] = config[sett] 

  if verbose: print(config)

  # downloading data 
  if verbose: print("siteid: ", siteid)
  province = findprov(siteid)
  if verbose: print("province: ", province)

  # importing from EC's climate normals system 
  if scrapenormals: 
    normalsurl = "https://dd.weather.gc.ca/climate/observations/normals/csv/1981-2010/" + province + "/climate_normals_" + province + "_" + siteid + "_1981-2010.csv"
    try: normalsreader = fetchECCC(normalsurl)
    except: pass # ############# create an error message to store ############

  if verbose: print("scrape daily data? ", scrapedailies)
  if scrapedailies:
    #yearrange = [int(x) for x in years[1:-1].split(", ")] # converting to integers
    # build filename based off siteID
    # this section imports all daily data from ECCC at a specific site ID into a saved file
    dailydata = collectalldailies(config)
    with open("temporarydailydata.csv", 'w') as f:
      csvwriter = csv.writer(f)
      for line in dailydata:
        csvwriter.writerow(line)
    if verbose: print("dailies data imported and file written")
  if rplot: 
    if verbose and not scrapedailies: print("plotting without downloading fresh...")
    runplot()
    

  if scrapenormals: 
    #data entirely from the climate normals summaries
    print("scraping from climate normals pages...")
    normalsdata = climatetable(normalsreader)
    dailiesdataframe = pd.read_csv('temporarydailydata.csv')
    reports.final_report(normalsdata, dailiesdataframe, config=config)

if __name__ == "__main__":
  # ARGUMENTS REMINDER 
  # siteid, scrapedailies = False, rplot = False

  #main('7016294', True, False)
  #main('23026HN', True, False)
  main()
  #main('6016527', True, False)

  # if rerunning from data that already exists
  #main('8300300', False, True)

  # OTT can use the climate normals but not scrape data (timeout error)
  #main('6016527', False, False)
  # change line 40 from str to csv for csv output demo

  #main('2101300', True, False)



#notes about what to do add to config file
# site id
# toggle for each parameter 
# "error threshold" for missing data >x% (10 is default)
# verbose mode?
# year range


