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
  return peryear
  #print(count, daycount, peryear)

def coldwaveD(data):
  # counts the number of rolling 3 day windows in which temp is <-15. longer duration events counted multiple times
  df = pd.read_csv(data)  
  daycount = len(df)
  df = df[["Min Temp (°C)"]].rolling(3).max()
  df = df[df["Min Temp (°C)"] <= -15]
  count = len(df)
  peryear = float(count)/daycount * 365
  return peryear
  #print(count, daycount, peryear)

# more info: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.index.html 

def hightemperatureD(data):
  df = pd.read_csv(data)
  df = df[["Max Temp (°C)"]].mean().values[0]
  #print(df)
  return df

def lowtemperatureD(data):
  df = pd.read_csv(data)
  df = df[["Min Temp (°C)"]].mean().values[0]
  #print(df)
  return df

def veryhotdaysD(data):
  df = pd.read_csv(data)
  daycount = len(df)
  df = df[df["Max Temp (°C)"] >= 30]
  count = len(df)
  peryear = float(count)/daycount * 365
  #print(count, daycount, peryear)
  return peryear


def verycolddaysD(data):
  df = pd.read_csv(data)
  daycount = len(df)
  df = df[df["Min Temp (°C)"] <= -30]
  count = len(df)
  peryear = float(count)/daycount * 365
  #print(count, daycount, peryear)
  return peryear


def coolingdegreedaysD(data):
  df = pd.read_csv(data)  
  daycount = len(df)
  df = df[df["Mean Temp (°C)"] >= 18]
  count = len(df) # number of days >= 18
  aboveval = df[["Mean Temp (°C)"]].sum().values[0] - 18*count #number of degrees >=18 summed across the full dataset
  peryear = float(aboveval)/daycount * 365  # dividing by (number of days with data/365)
  #print(aboveval, peryear)
  return peryear

def heatingdegreedaysD(data):
  df = pd.read_csv(data)  
  daycount = len(df)
  df = df[df["Mean Temp (°C)"] <= 18]
  count = len(df) # number of days <= 18
  aboveval = 18*count - df[["Mean Temp (°C)"]].sum().values[0] #number of degrees <=18 summed across the full dataset
  peryear = float(aboveval)/daycount * 365  # dividing by (number of days with data/365)
  #print(aboveval, peryear)
  return peryear


def diurnaldeviationD(data):
  df = pd.read_csv(data)
  daycount = len(df)
  df = df[df["Max Temp (°C)"] - df["Min Temp (°C)"] > 25]  
  df = df[["Max Temp (°C)", "Min Temp (°C)"]]
  count = len(df)
  peryear = float(count)/daycount * 365
  #print(df)
  return peryear


def annualprecipitationD(data):
  df = pd.read_csv(data)
  daycount = len(df)
  df = df[["Total Precip (mm)"]]
  total = df.sum().values[0]
  peryear = float(total)/daycount * 365
  print(total, daycount, peryear)
  #print(df)
  return peryear


def seasonalpretipD(data):
  df = pd.read_csv(data)
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


def annualsnowdepthD(data):
  df = pd.read_csv(data)
  df = df[["Snow on Grnd (cm)"]]
  df = df.mean().values[0]
  #print(df)
  return df

def averagewintersnowdepthD(data): #october to april
  df = pd.read_csv(data)
  df = df[["Month", "Snow on Grnd (cm)"]]
  df = df[(df.Month >= 10) | (df.Month <= 4 )]
  df = df.mean().values[0]
  #print(df)
  return df

def extremesnowfalldaysD(data):
  df = pd.read_csv(data)
  df = df[["Total Snow (cm)"]]
  df = df[df["Total Snow (cm)"] > 25]
  #print(df)
  #print(len(df))
  return len(df)

def annualsnowfalltotalD(data):
  df = pd.read_csv(data)
  daycount = len(df)
  df = df[["Total Snow (cm)"]]
  total = df.sum().values[0]
  peryear = float(total)/daycount * 365
  #print(total, daycount, peryear)
  #print(df)
  return peryear


def drydaysD(data):
  df = pd.read_csv(data)
  daycount = len(df)
  df = df[["Total Precip (mm)"]]
  df = df[df["Total Precip (mm)"] < 0.2]
  count = len(df)
  peryear = float(count)/daycount * 365
  #print(count, daycount, peryear)
  return peryear
  

def strongwinddaysD(data):
  df = pd.read_csv(data)
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
