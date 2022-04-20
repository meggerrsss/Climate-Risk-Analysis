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
  return peryear

  
def veryveryhotdaysD(df):
  df = df[["Max Temp (°C)"]].dropna()
  daycount = len(df)
  df = df[df["Max Temp (°C)"] > 32].dropna()
  count = len(df)
  peryear = float(count)/daycount * 365
  return peryear

  
def extremelyhotdaysD(df):
  df = df[["Max Temp (°C)"]].dropna()
  daycount = len(df)
  df = df[df["Max Temp (°C)"] > 34].dropna()
  count = len(df)
  peryear = float(count)/daycount * 365
  return peryear




def verycolddaysD(df):
  df = df[["Min Temp (°C)"]].dropna()
  daycount = len(df)
  df = df[df["Min Temp (°C)"] < -30].dropna()
  count = len(df)
  peryear = float(count)/daycount * 365
  return peryear

  
def veryverycolddaysD(df):
  df = df[["Min Temp (°C)"]].dropna()
  daycount = len(df)
  df = df[df["Min Temp (°C)"] < -32].dropna()
  count = len(df)
  peryear = float(count)/daycount * 365
  return peryear

  
def extremelycolddaysD(df):
  df = df[["Min Temp (°C)"]].dropna()
  daycount = len(df)
  df = df[df["Min Temp (°C)"] < -34].dropna()
  count = len(df)
  peryear = float(count)/daycount * 365
  return peryear

  
def frostdaysD(df):
  df = df[["Min Temp (°C)"]].dropna()
  daycount = len(df)
  df = df[df["Min Temp (°C)"] <= 0].dropna()
  count = len(df)
  peryear = float(count)/daycount * 365
  return peryear

  
def mildwinterdaysD(df):
  df = df[["Min Temp (°C)"]].dropna()
  daycount = len(df)
  df = df[df["Min Temp (°C)"] <= -5].dropna()
  count = len(df)
  peryear = float(count)/daycount * 365
  return peryear

  
def winterdaysD(df):
  df = df[["Min Temp (°C)"]].dropna()
  daycount = len(df)
  df = df[df["Min Temp (°C)"] <= -15].dropna()
  count = len(df)
  peryear = float(count)/daycount * 365
  return peryear

  
def icingdaysD(df):
  df = df[["Max Temp (°C)"]].dropna()
  daycount = len(df)
  df = df[df["Max Temp (°C)"] <= 0].dropna()
  count = len(df)
  peryear = float(count)/daycount * 365
  #if verbose: print(count, daycount, peryear
  return peryear



def coolingdegreedaysD(df): #
  df = df[["Mean Temp (°C)"]].dropna()
  daycount = len(df)
  df = df[df["Mean Temp (°C)"] > 18].dropna()
  count = len(df) # number of days >= 18
  aboveval = df[["Mean Temp (°C)"]].sum().values[0] - 18*count #number of degrees >=18 summed across the full dataset
  peryear = float(aboveval)/daycount * 365  # dividing by (number of days with data/365)
  if verbose: print(aboveval, peryear)
  return peryear

def heatingdegreedaysD(df):    
  df = df[["Mean Temp (°C)"]].dropna()
  daycount = len(df)
  df = df[df["Mean Temp (°C)"] < 18].dropna()
  count = len(df) # number of days <= 18
  aboveval = 18*count - df[["Mean Temp (°C)"]].sum().values[0] #number of degrees <=18 summed across the full dataset
  peryear = float(aboveval)/daycount * 365  # dividing by (number of days with data/365)
  if verbose: print(aboveval, peryear)
  return peryear

  
def freezingdegreedaysD(df):    
  df = df[["Mean Temp (°C)"]].dropna()
  daycount = len(df)
  df = df[df["Mean Temp (°C)"] < 0].dropna()
  #count = len(df) # number of days < 0
  aboveval = - df[["Mean Temp (°C)"]].sum().values[0] #number of degrees  summed across the full dataset
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


def annualprecipitationD(df): 
  df = df[["Total Precip (mm)"]].dropna()
  daycount = len(df)
  total = df.sum().values[0]
  peryear = float(total)/daycount * 365
  return peryear

  
def springprecipitationD(df): 
  df = df[["Month", "Total Precip (mm)"]].dropna()
  daycount = len(df)
  df = df[(df['Month'] >= 3) & (df['Month'] <= 5)]
  total = df.sum().values[1]
  peryear = float(total)/daycount * 365
  return peryear

  
def summerprecipitationD(df): 
  df = df[["Month", "Total Precip (mm)"]].dropna()
  daycount = len(df)
  df = df[(df['Month'] >= 6) & (df['Month'] <= 8)]
  total = df.sum().values[1]
  peryear = float(total)/daycount * 365
  return peryear

  
def fallprecipitationD(df): 
  df = df[["Month", "Total Precip (mm)"]].dropna()
  daycount = len(df)
  df = df[(df['Month'] >= 9) & (df['Month'] <= 11)]
  total = df.sum().values[1]
  peryear = float(total)/daycount * 365
  return peryear

  
def winterprecipitationD(df): 
  df = df[["Month", "Total Precip (mm)"]].dropna()
  daycount = len(df)
  df = df[(df.Month == 12) | (df.Month <= 2 )]
  total = df.sum().values[1]
  peryear = float(total)/daycount * 365
  return peryear


def annualtemperatureD(df): 
  df = df[["Mean Temp (°C)"]].dropna()
  df = df.mean().values[0]
  return df


def springtemperatureD(df): 
  df = df[['Month', "Mean Temp (°C)"]].dropna()
  df = df[(df['Month'] >= 3) & (df['Month'] <= 5)]
  df = df.mean().values[1]
  return df


def summertemperatureD(df): 
  df = df[['Month', "Mean Temp (°C)"]].dropna()
  df = df[(df['Month'] >= 6) & (df['Month'] <= 8)]
  df = df.mean().values[1]
  return df


def falltemperatureD(df): 
  df = df[['Month', "Mean Temp (°C)"]].dropna()
  df = df[(df['Month'] >= 9) & (df['Month'] <= 11)]
  df = df.mean().values[1]
  return df


def wintertemperatureD(df): 
  df = df[['Month', "Mean Temp (°C)"]].dropna()
  df = df[(df.Month == 12) | (df.Month <= 2 )]
  df = df.mean().values[1]
  return df


def annualsnowdepthD(df):
  df = df[["Snow on Grnd (cm)"]].dropna()
  df = df.mean().values[0]
  #print(df)
  return df


def averagewintersnowdepthD(df): #october to april  # * needs cleaning check
  df = df[["Month", "Snow on Grnd (cm)"]].dropna()
  df = df[(df.Month >= 10) | (df.Month <= 4 )]
  df = df.mean().values[1]
  #print(df)
  return df


def extremesnowfalldaysD(df):
  df = df[["Total Snow (cm)"]].dropna()
  daycount = len(df)
  df = df[df["Total Snow (cm)"] >= 25]
  return len(df)/float(daycount) * 365


def annualsnowfalltotalD(df): 
  df = df[["Total Snow (cm)"]].dropna()
  daycount = len(df)
  total = df.sum().values[0]
  peryear = float(total)/daycount * 365
  return peryear




def drydaysD(df): 
  df = df[["Total Precip (mm)"]].dropna()
  daycount = len(df)
  df = df[df["Total Precip (mm)"] < 0.2]
  count = len(df)
  peryear = float(count)/daycount * 365
  #print(count, daycount, peryear)
  return peryear

  
def wetdaysD(df): 
  df = df[["Total Precip (mm)"]].dropna()
  daycount = len(df)
  df = df[df["Total Precip (mm)"] >= 0.2]
  count = len(df)
  peryear = float(count)/daycount * 365
  #print(count, daycount, peryear)
  return peryear
  

def strongwinddaysD(df):
  df = df[['Year',"Spd of Max Gust (km/h)"]].dropna()
  daycount = len(df)  
  df = df[df["Spd of Max Gust (km/h)"].apply(lambda x: x.isnumeric())]
  newdaycount = len(df)
  df["Spd of Max Gust (km/h)"] = pd.to_numeric(df["Spd of Max Gust (km/h)"])
  df = df[df["Spd of Max Gust (km/h)"] > 63]
  df = df[['Year', "Spd of Max Gust (km/h)"]].groupby(['Year']).count()
  df = df.mean()
  return df.values[0]
  

def strongerwinddaysD(df):
  df = df[['Year',"Spd of Max Gust (km/h)"]].dropna()
  daycount = len(df)  
  df = df[df["Spd of Max Gust (km/h)"].apply(lambda x: x.isnumeric())]
  newdaycount = len(df)
  df["Spd of Max Gust (km/h)"] = pd.to_numeric(df["Spd of Max Gust (km/h)"])
  df = df[df["Spd of Max Gust (km/h)"] > 90]
  df = df[['Year', "Spd of Max Gust (km/h)"]].groupby(['Year']).count()
  df = df.mean()
  return df.values[0]
 



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




#pd.set_option('max_columns', None)
def longestheatwaveD(df):
  #longest stretch of time across the entire duration that temps reach >=30
  # strategy implemented from https://joshdevlin.com/blog/calculate-streaks-in-pandas/ 
  df = df[["Year", "Max Temp (°C)"]].dropna()
  # creating a column where heatwave conditions are satisfied 
  df['hot'] = df["Max Temp (°C)"] >= 30
  # column that says "does the streak start over" -- includes both "heatwave" streak and "not a heatwave" streaks for now
  df['streakstart'] = df.hot.ne(df.hot.shift())
  # a new column that is True if this is the start of a heatwave streak, not just any streak
  df['heatstart'] = df.hot & df.streakstart
  # heatwave streak number, even numbers are heatwaves, odd are non-heatwaves
  df['streakid'] = df['streakstart'].cumsum()
  # counts the number of days in each streak, multiplies by zero if not a heatwave
  df['streakcounter'] = (df.groupby('streakid').cumcount() + 1)*df.hot
  df = df[df.streakcounter>0]
  # longest heatwave across the entire dataset
  longeststreak = df.streakcounter.max()
  return longeststreak


def longestannualheatwaveD(df):
  #longest stretch of time across the entire duration that temps reach >=30
  # strategy implemented from https://joshdevlin.com/blog/calculate-streaks-in-pandas/ 
  df = df[["Year", "Max Temp (°C)"]].dropna()
  # creating a column where heatwave conditions are satisfied 
  df['hot'] = df["Max Temp (°C)"] >= 30
  # column that says "does the streak start over" -- includes both "heatwave" streak and "not a heatwave" streaks for now
  df['streakstart'] = df.hot.ne(df.hot.shift())
  # a new column that is True if this is the start of a heatwave streak, not just any streak
  df['heatstart'] = df.hot & df.streakstart
  # heatwave streak number, even numbers are heatwaves, odd are non-heatwaves
  df['streakid'] = df['streakstart'].cumsum()
  # counts the number of days in each streak, multiplies by zero if not a heatwave
  df['streakcounter'] = (df.groupby('streakid').cumcount() + 1)*df.hot
  df = df[df.streakcounter>0]
  # grouping by years, taking the longest heatwave length per year and averaging across years
  averagedlongestannualheatwaves = df[['Year', 'streakcounter']].groupby(['Year']).max().streakcounter.mean()
  return averagedlongestannualheatwaves


def averageheatwaveD(df):
  #longest stretch of time across the entire duration that temps reach >=30
  # strategy implemented from https://joshdevlin.com/blog/calculate-streaks-in-pandas/ 
  df = df[["Year", "Max Temp (°C)"]].dropna()
  # creating a column where heatwave conditions are satisfied 
  df['hot'] = df["Max Temp (°C)"] >= 30
  # column that says "does the streak start over" -- includes both "heatwave" streak and "not a heatwave" streaks for now
  df['streakstart'] = df.hot.ne(df.hot.shift())
  # a new column that is True if this is the start of a heatwave streak, not just any streak
  df['heatstart'] = df.hot & df.streakstart
  # heatwave streak number, even numbers are heatwaves, odd are non-heatwaves
  df['streakid'] = df['streakstart'].cumsum()
  # counts the number of days in each streak, multiplies by zero if not a heatwave
  df['streakcounter'] = (df.groupby('streakid').cumcount() + 1)*df.hot
  df = df[df.streakcounter>0]
  # average of all heatwaves >=3 days
  streaklengths =  df[df["hot"] == 1].groupby(["streakid"]).size()
  averagestreak = streaklengths[streaklengths>=3].mean()
  return averagestreak
  

def dtn(date):
  # dtn = date to number, nth day of the year
  # also adjusts to +1 for leap years correctly
  newyears = pd.Timestamp(year=date.year, month=1, day=1)
  return (date-newyears).days+1


def firstfallfrostD(df):
  df = df[["Year", "Month", "Date/Time", "Min Temp (°C)"]].dropna()
  # i'm not sure if this conversion line actually did anything
  df['Date/Time'] = pd.to_datetime(df['Date/Time'], format='%Y-%m-%d')
  # filter to late summer/fall 
  df = df[df.Month >=7]
  # filter by frost conditions met
  df = df[df['Min Temp (°C)']<=0]
  # first day of each year
  df = df[['Year', 'Date/Time']].groupby(['Year']).min()
  df['nth'] = df['Date/Time'].apply(dtn)
  df = df.nth.mean()
  return df


def lastspringfrostD(df):
  df = df[["Year", "Month", "Date/Time", "Min Temp (°C)"]].dropna()
  # i'm not sure if this conversion line actually did anything
  df['Date/Time'] = pd.to_datetime(df['Date/Time'], format='%Y-%m-%d')
  # filter to late summer/fall 
  df = df[df.Month <= 6]
  # filter by frost conditions met
  df = df[df['Min Temp (°C)']<=0]
  # first day of each year
  df = df[['Year', 'Date/Time']].groupby(['Year']).max()
  df['nth'] = df['Date/Time'].apply(dtn)
  df = df.nth.mean()
  return df


def onedayprecipD(df):
  df = df[["Year", "Total Precip (mm)"]].dropna()
  df = df[['Year', "Total Precip (mm)"]].groupby(['Year']).max()
  df = df.mean().values[0]
  return df


def threedayprecipD(df):
  df = df[["Year", "Total Precip (mm)"]].dropna()
  df['sum'] = df[["Total Precip (mm)"]].rolling(3).sum().dropna()
  df = df[['Year', "Total Precip (mm)", "sum"]].groupby(['Year']).max()
  df = df.mean().values[1]
  return df


def fivedayprecipD(df):
  df = df[["Year", "Total Precip (mm)"]].dropna()
  df['sum'] = df[["Total Precip (mm)"]].rolling(5).sum().dropna()
  df = df[['Year', "Total Precip (mm)", "sum"]].groupby(['Year']).max()
  df = df.mean().values[1]
  return df
  

  

# to do from nathan's additional parameters list
  # date of first fall frost
  # date of last spring frost
  # frost free season
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
