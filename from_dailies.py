import pandas as pd

def freezethawD(df):
  # Days where the maximum daily temperature > 0°C and the minimum daily temperature < 0°C. Number of occurrences per year.
  daycount = len(df)
  df = df[["Max Temp (°C)", "Min Temp (°C)"]]
  print(df)
  df = df[df["Max Temp (°C)"] > 0]
  print(df)
  df = df[df["Min Temp (°C)"] < -1]
  print(df)
  #df = df[df["Max Temp (°C)"] * df["Min Temp (°C)"] < 0] it wasn't this option lol
  count = len(df)
  peryear = float(count)/daycount * 365
  print(count)
  exit()
  return peryear

def heatwaveD(df):
  # counts the number of rolling 3 day windows in which temp is >= 30. longer duration events counted multiple times
  daycount = len(df)
  df = df[["Max Temp (°C)"]].rolling(3).min()
  df = df[df["Max Temp (°C)"] > 30]
  eventdates = df.index.array
  consec = 0 # number of times a rolling 3 day window starts one day apart
  for event in range(len(eventdates)-1):
    if abs(eventdates[event]-eventdates[event+1]) == 1:
      consec += 1
  count = len(df) # number of rolling 3 day windows
  discrete = count-consec  # number of discrete events with at least 1 day off
  peryear = float(discrete)/daycount * 365
  return peryear

def coldwaveD(df):
  # counts the number of rolling 3 day windows in which temp is <-15. longer duration events counted multiple times
  daycount = len(df)
  df = df[["Min Temp (°C)"]].rolling(3).max()
  df = df[df["Min Temp (°C)"] < -15]
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
  df = df[["Max Temp (°C)"]].mean().values[0]
  #print(df)
  return df

def lowtemperatureD(df):
  df = df[["Min Temp (°C)"]].mean().values[0]
  #print(df)
  return df

def veryhotdaysD(df):
  daycount = len(df)
  df = df[df["Max Temp (°C)"] > 30]
  count = len(df)
  peryear = float(count)/daycount * 365
  #print(count, daycount, peryear)
  return peryear


def verycolddaysD(df):
  daycount = len(df)
  df = df[df["Min Temp (°C)"] < -30]
  count = len(df)
  peryear = float(count)/daycount * 365
  #print(count, daycount, peryear)
  return peryear


def coolingdegreedaysD(df):
  daycount = len(df)
  df = df[df["Mean Temp (°C)"] > 18]
  count = len(df) # number of days >= 18
  aboveval = df[["Mean Temp (°C)"]].sum().values[0] - 18*count #number of degrees >=18 summed across the full dataset
  peryear = float(aboveval)/daycount * 365  # dividing by (number of days with data/365)
  #print(aboveval, peryear)
  return peryear

def heatingdegreedaysD(df):
  daycount = len(df)
  df = df[df["Mean Temp (°C)"] < 18]
  count = len(df) # number of days <= 18
  aboveval = 18*count - df[["Mean Temp (°C)"]].sum().values[0] #number of degrees <=18 summed across the full dataset
  peryear = float(aboveval)/daycount * 365  # dividing by (number of days with data/365)
  #print(aboveval, peryear)
  return peryear


def diurnaldeviationD(df):
  daycount = len(df)
  df = df[df["Max Temp (°C)"] - df["Min Temp (°C)"] > 25]  
  df = df[["Max Temp (°C)", "Min Temp (°C)"]]
  count = len(df)
  peryear = float(count)/daycount * 365
  #print(df)
  return peryear


def annualprecipitationD(df):
  daycount = len(df)
  df = df[["Total Precip (mm)"]]
  total = df.sum().values[0]
  peryear = float(total)/daycount * 365
  print(total, daycount, peryear)
  #print(df)
  return peryear


def seasonalpretipD(df):
  daycount = len(df)
  df = df[["Month", "Total Precip (mm)"]]
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


def annualsnowdepthD(df):
  df = df[["Snow on Grnd (cm)"]]
  df = df.mean().values[0]
  #print(df)
  return df

def averagewintersnowdepthD(df): #october to april
  df = df[["Month", "Snow on Grnd (cm)"]]
  df = df[(df.Month >= 10) | (df.Month <= 4 )]
  df = df.mean().values[0]
  #print(df)
  return df

def extremesnowfalldaysD(df):
  df = df[["Total Snow (cm)"]]
  df = df[df["Total Snow (cm)"] >= 25]
  #print(df)
  #print(len(df))
  return len(df)

def annualsnowfalltotalD(df):
  daycount = len(df)
  df = df[["Total Snow (cm)"]]
  total = df.sum().values[0]
  peryear = float(total)/daycount * 365
  #print(total, daycount, peryear)
  #print(df)
  return peryear


def drydaysD(df):
  daycount = len(df)
  df = df[["Total Precip (mm)"]]
  df = df[df["Total Precip (mm)"] < 0.2]
  count = len(df)
  peryear = float(count)/daycount * 365
  #print(count, daycount, peryear)
  return peryear
  

def strongwinddaysD(df):
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
    



#def template(data):
###  df = pd.read_csv(data)
#  daycount = len(df)
#  #df = 
#  #  count = len(df)
#  peryear = float(count)/daycount * 365
#  print(count, daycount, peryear)
#  return peryear
