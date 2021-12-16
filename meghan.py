import csv
from collections import defaultdict
from pprint import pprint
import requests


# importing from web
siteid = 6016527
province = 'ON'
#url = "https://dd.weather.gc.ca/climate/observations/normals/csv/1981-2010/" + province + "/climate_normals_" + province + "_" + siteid + "_1981-2010.csv"
url = 'example.csv'

with open(url) as f:
    reader = list(csv.reader(f))


def fetchECCC(urlname):
  # inputs the url name (ECCC link or local like 'example.csv')
  with requests.Session() as s:
    download = s.get(urlname)
    decoded = download.content.decode("ISO-8859-1")
    reader = csv.reader(decoded.splitlines())
  return list(reader)


def climatetable(csvlist):
  # csvlist = output from list(csv.reader(file)):
  # returns a list of list of strings for every line and cell in the original csv 
  outp = defaultdict(list)
  table = '' # "staging area"/"table"/"workspsace" whatever
  for row in csvlist:
    if len(row) == 0: # if row is empty, skip
      continue
    elif len(row) == 1: # if row only has the title of a section, name section that
      table = row[0]
    else: # if row is not a title, add it to the last section
      outp[table].append(row)
  return outp 


#results out of the report 

def drydays(report):
  for row in report['Days with Precipitation']:
    if row[0] == ">= 0.2 mm":
      return 365 - float(row[-2])
  raise ValueError

chunked_report = climatetable(reader)

print(drydays(chunked_report))