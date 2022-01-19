import pandas as pd

def freezethawD(data):
  # Days where the maximum daily temperature > 0°C and the minimum daily temperature < 0°C. Number of occurrences per year.
  df = pd.read_csv(data)
  daycount = len(df)
  df = df[df["Max Temp (°C)"] * df["Min Temp (°C)"] < 0]
  df = df[["Max Temp (°C)", "Min Temp (°C)"]]
  count = len(df)
  peryear = float(count)/daycount * 365
  return peryear

def heatwaveD(data):
  # counts the number of rolling 3 day windows in which temp is >= 30. longer duration events counted multiple times
  df = pd.read_csv(data)  
  daycount = len(df)
  df = df[["Max Temp (°C)"]].rolling(3).min()
  df = df[df["Max Temp (°C)"] >= 30]
  count = len(df)
  peryear = float(count)/daycount * 365
  print(count, daycount, peryear)

def coldwaveD(data):
  # counts the number of rolling 3 day windows in which temp is <-15. longer duration events counted multiple times
  df = pd.read_csv(data)  
  daycount = len(df)
  df = df[["Min Temp (°C)"]].rolling(3).max()
  df = df[df["Min Temp (°C)"] <= -15]
  count = len(df)
  peryear = float(count)/daycount * 365
  print(count, daycount, peryear)

# more info: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.index.html 

def hightemperatureD(data):
  df = pd.read_csv(data)
  df = df[["Max Temp (°C)"]].mean().values[0]
  print(df)
  return df

def lowtemperatureD(data):
  df = pd.read_csv(data)
  df = df[["Min Temp (°C)"]].mean().values[0]
  print(df)
  return df

def veryhotdaysD(data):
  df = pd.read_csv(data)
  daycount = len(df)
  df = df[df["Max Temp (°C)"] >= 30]
  count = len(df)
  peryear = float(count)/daycount * 365
  print(count, daycount, peryear)
  return peryear


def verycolddaysD(data):
  df = pd.read_csv(data)
  daycount = len(df)
  df = df[df["Min Temp (°C)"] <= -30]
  count = len(df)
  peryear = float(count)/daycount * 365
  print(count, daycount, peryear)
  return peryear


def coolingdegreedaysD(data):
  df = pd.read_csv(data)  
  daycount = len(df)
  df = df[df["Mean Temp (°C)"] >= 18]
  count = len(df) # number of days >= 18
  aboveval = df[["Mean Temp (°C)"]].sum().values[0] - 18*count #number of degrees >=18 summed across the full dataset
  peryear = float(aboveval)/daycount * 365  # dividing by (number of days with data/365)
  print(aboveval, peryear)
  return peryear

def heatingdegreedaysD(data):
  df = pd.read_csv(data)  
  daycount = len(df)
  df = df[df["Mean Temp (°C)"] <= 18]
  count = len(df) # number of days <= 18
  aboveval = 18*count - df[["Mean Temp (°C)"]].sum().values[0] #number of degrees <=18 summed across the full dataset
  peryear = float(aboveval)/daycount * 365  # dividing by (number of days with data/365)
  print(aboveval, peryear)
  return peryear


def diurnaldeviationD(data):
  df = pd.read_csv(data)
  daycount = len(df)
  df = df[df["Max Temp (°C)"] - df["Min Temp (°C)"] > 25]  
  df = df[["Max Temp (°C)", "Min Temp (°C)"]]
  count = len(df)
  peryear = float(count)/daycount * 365
  print(count, daycount, peryear)
  print(df)
  return peryear


#def template(data):
###  df = pd.read_csv(data)
#  daycount = len(df)
#  #df = 
#  #  count = len(df)
#  peryear = float(count)/daycount * 365
#  print(count, daycount, peryear)
#  return peryear
