import requests, csv 
import pandas as pd

siteIDurl = 'https://dd.weather.gc.ca/climate/observations/climate_station_list.csv'

def fetch(urlname):
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


def findprov(siteID):
  db = fetch(siteIDurl)
  db['Climate ID'] = db['Climate ID'].map(str) #ensuring entire climate ID colum is a str
  spot = db.loc[db['Climate ID'] == siteID]
  short = shortenprovince(spot['Province'].values[0])
  return short
      


  
