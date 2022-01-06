import csv
from collections import defaultdict
import requests


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
  # 365 - Days with precipitation (year)
  # Number of days with less than 0.2 mm of rain (Dry Day)
  for row in report['Days with Precipitation']:
    if row[0] == ">= 0.2 mm":
      return 365 - float(row[-2])
  raise ValueError

def annualsnowdepth(report):
  # Annual Snow Depth (year)
  # Extreme mean annual snow depth; cm (January – December) per year
  #for row in report['Precipitation']:
  #  if row[0] == "Average Snow Depth (cm)":
  #    return float(row[-2])
  monthweights = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
  for row in report['Precipitation']:
    if row[0] == "Average Snow Depth (cm)":
      weighted = [int(row[x+1]) * monthweights[x] for x in range(12)]
      return sum(weighted)/float(sum(monthweights))
  raise ValueError
  #i'm uncertain that averaging 12 whole numbers really has enough significant digits to get two decimal points out of it but i guess it's better than just pulling the year value. 
  # reverse the commented lines if we just want the year value returned instead
  # also change monthweights to [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31] for weighted days

def averagewintersnowdepth(report):
  # Average Oct-Apr Snow Depth (year)
  # Extreme mean seasonal snow depth (Oct – April) per year
  for row in report['Precipitation']:
    if row[0] == "Average Snow Depth (cm)":
      octapr = row[1:5]+row[10:13]
      avg = sum([float(x) for x in octapr])
      return avg/7
  raise ValueError


def hightemperature(report):
  # High Temperature (Max)
  # Maximum temperature °C (high) recorded in a 24-hour period ending in the morning of the next day per year.
  for row in report['Temperature']:
    if row[0] == "Daily Maximum (°C)":
      return float(row[-2])
  raise ValueError


def lowtemperature(report):
  # Low Temperature (Min)
  # Minimum temperature °C (low) is for a period of the same length but begins in the evening of the previous day per year.
  for row in report['Temperature']:
    if row[0] == "Daily Minimum (°C)":
      return float(row[-2])
  raise ValueError


def veryhotdays(report):
  # Very Hot Days
  # Number of days with temperatures >30°C per year.  
  for row in report['Days with Maximum Temperature']:
    if row[0] == "> 30 °C":
      return float(row[-2])
  raise ValueError


def verycolddays(report):
  # Very Cold Days
  # Number of days with temperatures <-30°C per year.  
  for row in report['Days with Minimum Temperature']:
    if row[0] == "< - 30 °C":
      return float(row[-2])
  raise ValueError


def coolingdegreedays(report):
  # Cooling Degree Days (CDD)
  # CDD are equal to the number of degrees Celsius a given day’s mean temperature is above 18 °C per year.
  for row in report['Degree Days']:
    if row[0] == 'Above 18 °C':
      return float(row[-2])
  raise ValueError


def heatingdegreedays(report):
  # Cooling Degree Days (CDD)
  # CDD are equal to the number of degrees Celsius a given day’s mean temperature is above 18 °C per year.
  for row in report['Degree Days']:
    if row[0] == 'Below 18 °C':
      return float(row[-2])
  raise ValueError


def annualprecipitation(report):
  # Total Annual Precipitation
  # Total amount of precipititation in mm per year. 
  for row in report['Precipitation']:
    if row[0] == 'Precipitation (mm)':
      return float(row[-2])
  raise ValueError


def springprecipitation(report):
  # Total Spring Precipitation
  # Total amount of precipititation in mm per spring (Mar, Apr, May). 
  for row in report['Precipitation']:
    if row[0] == 'Precipitation (mm)':
      return float(row[3])+float(row[4])+float(row[5])
  raise ValueError


def summerprecipitation(report):
  # Total Summer Precipitation
  # Total amount of precipititation in mm per summer (Jun, Jul, Aug). 
  for row in report['Precipitation']:
    if row[0] == 'Precipitation (mm)':
      return float(row[6])+float(row[7])+float(row[8])
  raise ValueError
  

def fallprecipitation(report):
  # Total Fall Precipitation
  # Total amount of precipititation in mm per fall (Sep, Oct, Nov). 
  for row in report['Precipitation']:
    if row[0] == 'Precipitation (mm)':
      return float(row[9])+float(row[10])+float(row[11])
  raise ValueError
  

def winterprecipitation(report):
  # Total Winter Precipitation
  # Total amount of all precipititation types in mm per winter (Dec, Jan, Feb). 
  for row in report['Precipitation']:
    if row[0] == 'Precipitation (mm)':
      return float(row[12])+float(row[1])+float(row[2])
  raise ValueError
  

def extremesnowfalldays(report):
  # Extreme Snowfall Totals
  # Days per year with conditions (>25 cm).
  for row in report['Days With Snowfall']:
    if row[0] == '>= 25 cm':
      return float(row[-2])
  raise ValueError
  

def annualsnowfalltotal(report):
  # Extreme Snowfall Total
  # Annual snowfall total; cm (January – December) per year.
  for row in report['Precipitation']:
    if row[0] == 'Snowfall (cm)':
      return float(row[-2])
  raise ValueError
  

def strongwinddays(report):
  # Strong Winds
  # Maximum Annual instantaneous wind gust (days having wind gusts >63 km/h per year). Baseline (1994 – 2009) from regional analysis.
  for row in report['Wind']:
    if row[0] == 'Days with Winds >= 63 km/h':
      return float(row[-2])
  raise ValueError




