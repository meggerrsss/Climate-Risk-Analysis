import requests, csv 
import pandas as pd

siteIDurl = 'https://dd.weather.gc.ca/climate/observations/climate_station_list.csv'

def fetch(urlname, typ=1):
  # inputs the url name (ECCC link or local like 'example.csv')
  # typ = 1 is just lists, typ = 2 is me experimenting with pandas 
  if typ==1: 
    with requests.Session() as s:
      download = s.get(urlname)
      decoded = download.content.decode("ISO-8859-1")
      reader = csv.reader(decoded.splitlines())
    return list(reader)
  elif typ==2:
    sites = pd.read_csv(siteIDurl)
    return sites 
    

def shortenprovince(prov):
  if prov == "ALBERTA": return "AB"
  elif prov == "BRITISH COLUMBIA": return "BC"
  elif prov == "NEWFOUNDLAND": return "NL"
  elif prov == "SASKATCHEWAN": return "SK"
  elif prov == "QUEBEC": return "QC"
  elif prov == "NOVA SCOTIA": return "NS"
  elif prov == "ONTARIO": return "ON"
  elif prov == "NEW BRUNSWICK": return "NB"
  elif prov == "YUKON TERRITORY": return "YT"
  elif prov == "NORTHWEST TERRITORIES": return "NT"
  elif prov == "PRINCE EDWARD ISLAND": return "PE"
  elif prov == "NUNAVUT": return "NU"
  elif prov == "MANITOBA": return "MB"
  else: return ValueError 


def findprov(siteID, typ=2):
  db = fetch(siteIDurl)
  for row in db:
    if row[5] == siteID:
      return shortenprovince(row[1])
      


  
