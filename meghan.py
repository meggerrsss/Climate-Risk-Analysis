# packages
import csv
from collections import defaultdict
from pprint import pprint
import requests

# importing from url or example

# importing from web
siteid = 6016527
province = 'unknown'

def finddata(siteidv, province='unknown'):
  if siteidv == 'example':
    data = 'example.csv'
  elif siteidv == 'example2':
    data = 'example2.csv'
  elif siteidv == 'example3':
    data = 'example3.csv'
  elif province == 'unknown':
    data = 'unknown'
  return data
#sites = pd.read_csv("https://dd.weather.gc.ca/climate/observations/climate_station_list.csv")
#sites.head()

#url = "https://dd.weather.gc.ca/climate/observations/normals/csv/1981-2010/ON/climate_normals_ON_6016527_1981-2010.csv"
url = 'example.csv'

def fetchECCC(urlname):
  # inputs the url name (ECCC link or local like 'example.csv')
  # returns a list of list of strings for every line and cell in the original csv 
  with requests.Session() as s:
    download = s.get(urlname)
    decoded = download.content.decode("ISO-8859-1")
    reader = csv.reader(decoded.splitlines())
  return list(reader)

print (fetchECCC('example.csv'))