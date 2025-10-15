import requests
import csv

# scrapes climate normals page if it exists, given a specific siteID as defined in config 
def fetchECCC(urlname):
  # inputs the url name (ECCC link or local like 'example.csv')
  with requests.Session() as s:
    download = s.get(urlname)
    download.raise_for_status()
    decoded = download.content.decode("ISO-8859-1")
    reader = csv.reader(decoded.splitlines())
  return list(reader)