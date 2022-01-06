import csv
from meghan import climatetable, fetchECCC
import reports
from siteIDdb import findprov

def main():
  # importing from web https://dd.weather.gc.ca/climate/observations/
  siteid = '6016527'
  province = findprov(siteid)
  url = "https://dd.weather.gc.ca/climate/observations/normals/csv/1981-2010/" + province + "/climate_normals_" + province + "_" + siteid + "_1981-2010.csv"
  #url = 'example3.csv'

  reader = fetchECCC(url)

  chunked_reader = climatetable(reader)
  reports.final_report(chunked_reader)

if __name__ == "__main__":
  main()