import pandas as pd

warningthres = 0.1
verbose = False

def freezethawD(df):
  # Days where the maximum daily temperature > 0°C and the minimum daily temperature < 1°C. Number of occurrences per year.
  daycount = len(df)
  df = df[["Max Temp (°C)", "Min Temp (°C)"]].dropna()
  df["Max Temp (°C)"] = pd.to_numeric(df["Max Temp (°C)"])
  df["Min Temp (°C)"] = pd.to_numeric(df["Min Temp (°C)"])
  cleaneddaycount = len(df)
  missing = 1- cleaneddaycount/float(daycount)
  if missing > warningthres and verbose: print("warning, {:.2f}% of data in specified year range is missing/unusable.".format(missing*100))
  if verbose: print("daycount = ", daycount, "; cleaned daycount = ", cleaneddaycount)
  df = df[df["Max Temp (°C)"] > 0]
  df = df[df["Min Temp (°C)"] < -1]
  count = len(df)
  peryear = float(count)/cleaneddaycount * 365
  return peryear

def heatwaveD(df): # * needs cleaning check
  # counts the number of rolling 3 day windows in which temp is >= 30. longer duration events listed once
  df = df[["Max Temp (°C)"]].dropna()
  daycount = len(df) # after cleaning
  df = df[["Max Temp (°C)"]].dropna().rolling(3).min()
  df = df[df["Max Temp (°C)"] >= 30]
  eventdates = df.index.array
  consec = 0 # number of times a rolling 3 day window starts one day apart
  for event in range(len(eventdates)-1):
    if abs(eventdates[event]-eventdates[event+1]) == 1:
      consec += 1
  count = len(df) # number of rolling 3 day windows
  discrete = count-consec  # number of discrete events with at least 1 day off
  peryear = float(discrete)/daycount * 365
  return peryear

def coldwaveD(df): # * needs cleaning check
  # counts the number of rolling 3 day windows in which temp is <= -15. longer duration events listed once
  df = df[["Min Temp (°C)"]].dropna()
  daycount = len(df)
  df = df[["Min Temp (°C)"]].dropna().rolling(3).max()
  df = df[df["Min Temp (°C)"] <= -15]
  eventdates = df.index.array
  consec = 0
  for event in range(len(eventdates)-1):
    if abs(eventdates[event]-eventdates[event+1]) == 1:
      consec += 1
  count = len(df)
  discrete = count-consec
  peryear = float(discrete)/daycount * 365
  return peryear

# more info: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.index.html 

def hightemperatureD(df): 
  df = df[["Max Temp (°C)"]].dropna().mean().values[0]
  return df

def lowtemperatureD(df):
  df = df[["Min Temp (°C)"]].dropna().mean().values[0]
  return df

def veryhotdaysD(df):
  df = df[["Max Temp (°C)"]].dropna()
  daycount = len(df)
  df = df[df["Max Temp (°C)"] > 30].dropna()
  count = len(df)
  peryear = float(count)/daycount * 365
  #if verbose: print(count, daycount, peryear)
  return peryear

  
def veryveryhotdaysD(df):
  df = df[["Max Temp (°C)"]].dropna()
  daycount = len(df)
  df = df[df["Max Temp (°C)"] > 32].dropna()
  count = len(df)
  peryear = float(count)/daycount * 365
  #if verbose: print(count, daycount, peryear)
  return peryear

  
def extremelyhotdaysD(df):
  df = df[["Max Temp (°C)"]].dropna()
  daycount = len(df)
  df = df[df["Max Temp (°C)"] > 34].dropna()
  count = len(df)
  peryear = float(count)/daycount * 365
  #if verbose: print(count, daycount, peryear
  return peryear




def verycolddaysD(df):
  df = df[["Min Temp (°C)"]].dropna()
  daycount = len(df)
  df = df[df["Min Temp (°C)"] < -30].dropna()
  count = len(df)
  peryear = float(count)/daycount * 365
  #if verbose: print(count, daycount, peryear)
  return peryear

  
def veryverycolddaysD(df):
  df = df[["Min Temp (°C)"]].dropna()
  daycount = len(df)
  df = df[df["Min Temp (°C)"] < -32].dropna()
  count = len(df)
  peryear = float(count)/daycount * 365
  #if verbose: print(count, daycount, peryear)
  return peryear

  
def extremelycolddaysD(df):
  df = df[["Min Temp (°C)"]].dropna()
  daycount = len(df)
  df = df[df["Min Temp (°C)"] < -34].dropna()
  count = len(df)
  peryear = float(count)/daycount * 365
  #if verbose: print(count, daycount, peryear
  return peryear



def coolingdegreedaysD(df): # * needs cleaning check
  daycount = len(df)
  df = df[df["Mean Temp (°C)"] > 18].dropna()
  count = len(df) # number of days >= 18
  aboveval = df[["Mean Temp (°C)"]].sum().values[0] - 18*count #number of degrees >=18 summed across the full dataset
  peryear = float(aboveval)/daycount * 365  # dividing by (number of days with data/365)
  if verbose: print(aboveval, peryear)
  return peryear

def heatingdegreedaysD(df):  # * needs cleaning check
  daycount = len(df)
  df = df[df["Mean Temp (°C)"] < 18].dropna()
  count = len(df) # number of days <= 18
  aboveval = 18*count - df[["Mean Temp (°C)"]].sum().values[0] #number of degrees <=18 summed across the full dataset
  peryear = float(aboveval)/daycount * 365  # dividing by (number of days with data/365)
  if verbose: print(aboveval, peryear)
  return peryear


def diurnalamplitudeD(df): 
  #number of days the max-min temp >=25
  df = df[["Max Temp (°C)", "Min Temp (°C)"]].dropna()
  daycount = len(df)
  df = df[df["Max Temp (°C)"] - df["Min Temp (°C)"] >= 25].dropna() 
  df = df[["Max Temp (°C)", "Min Temp (°C)"]]
  count = len(df)
  peryear = float(count)/daycount * 365
  return peryear


def annualprecipitationD(df): # * needs cleaning check
  daycount = len(df)
  df = df[["Total Precip (mm)"]].dropna()
  total = df.sum().values[0]
  peryear = float(total)/daycount * 365
  print(total, daycount, peryear)
  #print(df)
  return peryear


# commented out to help with the generalization in reports/config
def seasonalprecipitationD(df): # * needs cleaning check
  daycount = len(df)
  df = df[["Month", "Total Precip (mm)"]].dropna()
  spring = df[(df['Month'] >= 3) & (df['Month'] <= 5)]
  summer = df[(df['Month'] >= 6) & (df['Month'] <= 8)]
  autumn = df[(df['Month'] >= 9) & (df['Month'] <= 11)]
  winter = df[(df.Month == 12) | (df.Month <= 2 )]
  #print(spring)
  #seasoncounts = [len(spring), len(summer), len(autumn), len(winter)]
  seasontotals = [spring.sum().values[0], summer.sum().values[0], autumn.sum().values[0], winter.sum().values[0]]
  peryeartotals = [i/float(daycount) for i in seasontotals]
  #print(peryeartotals)
  return peryeartotals #spr, sum, aut, win


# wrappers to make my life eaiser with the function vs functionD requirement 
def springprecipitationD(df): 
  return seasonalprecipitationD(df)[0] 
def summerprecipitationD(df): 
  return seasonalprecipitationD(df)[1] 
def fallprecipitationD(df): 
  return seasonalprecipitationD(df)[2] 
def winterprecipitationD(df): 
  return seasonalprecipitationD(df)[3] 


def annualsnowdepthD(df):
  df = df[["Snow on Grnd (cm)"]].dropna()
  df = df.mean().values[0]
  #print(df)
  return df

def averagewintersnowdepthD(df): #october to april  # * needs cleaning check
  df = df[["Month", "Snow on Grnd (cm)"]].dropna()
  df = df[(df.Month >= 10) | (df.Month <= 4 )]
  df = df.mean().values[0]
  #print(df)
  return df

def extremesnowfalldaysD(df):
  df = df[["Total Snow (cm)"]].dropna()
  df = df[df["Total Snow (cm)"] >= 25]
  #print(df)
  #print(len(df))
  return len(df)

def annualsnowfalltotalD(df): # * needs cleaning check
  daycount = len(df)
  df = df[["Total Snow (cm)"]].dropna()
  total = df.sum().values[0]
  peryear = float(total)/daycount * 365
  #print(total, daycount, peryear)
  #print(df)
  return peryear


def drydaysD(df): # * needs cleaning check
  daycount = len(df)
  df = df[["Total Precip (mm)"]].dropna()
  df = df[df["Total Precip (mm)"] < 0.2]
  count = len(df)
  peryear = float(count)/daycount * 365
  #print(count, daycount, peryear)
  return peryear
  

def strongwinddaysD(df): # * needs cleaning check
  daycount = len(df)
  df = df[["Spd of Max Gust (km/h)"]].dropna()
  df = df[df["Spd of Max Gust (km/h)"].apply(lambda x: x.isnumeric())]
  df["Spd of Max Gust (km/h)"] = pd.to_numeric(df["Spd of Max Gust (km/h)"])
  df = df[df["Spd of Max Gust (km/h)"] >= 63]
  #print(df)
  count = len(df)
  peryear = float(count)/daycount * 365
  #print(count, daycount, peryear)
  return peryear



def warmestmaximumD(df): 
  #option 1: max temp across whole dataset
  #df1 = df[["Max Temp (°C)"]].dropna().max().values[0]
  #options 2: annual max temps, then average 
  df = df[['Year', 'Max Temp (°C)']].groupby(['Year']).max()
  df = df[["Max Temp (°C)"]].dropna().mean().values[0]
  return df


def coldestminimumD(df): # straight to option 2, see warmestmax
  df = df[['Year', 'Min Temp (°C)']].groupby(['Year']).min()
  df = df[["Min Temp (°C)"]].dropna().mean().values[0]
  return df
  

def meantemperaturesD(df): 
  # average of the daily max and the daily min temperatures
  df = df[["Max Temp (°C)", "Min Temp (°C)"]].dropna()
  df = df[["Max Temp (°C)", "Min Temp (°C)"]].dropna().mean()
  df = df.mean()
  return df


def longestheatwaveD(df):
  #longest stretch of time across the entire duration that temps reach >=30
  df = df[["Max Temp (°C)"]].dropna()
  df = df[df["Max Temp (°C)"] >= 30]
  print(df)
  eventdates = df.index.array
  consec = 1
  print(eventdates)
  for event in range(len(eventdates)-1):
    if eventdates[event] == eventdates[event-1]+1:
      consec += 1
    else: # eventdates[event] > eventdates[event-1]+1:
      consec = 1
  print(consec)
  

  

# to do from nathan's additional parameters list
  # longest spell of >30 
  # average length of heat waves
  # date of first fall frost
  # date of last spring frost
  # frost days
  # frost free season
  # icing days
  # mild winter days
  # winter days
  #wet days
  # freezing degree days
  # heavy precipitation 
  # - >10mm, >20mm, 3 day max, 5 day max, single day max
  










#def template(data): # * needs cleaning check
###  df = pd.read_csv(data)
#  daycount = len(df)
#  #df = 
#  #  count = len(df)
#  peryear = float(count)/daycount * 365
#  print(count, daycount, peryear)
#  return peryear
