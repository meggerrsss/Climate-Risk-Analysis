import requests
import csv
from collections import defaultdict


def fetchECCC(urlname):
  # inputs the url name (ECCC link or local like 'example.csv')
  with requests.Session() as s:
    download = s.get(urlname)
    download.raise_for_status()
    decoded = download.content.decode("ISO-8859-1")
    reader = csv.reader(decoded.splitlines())
  return list(reader)