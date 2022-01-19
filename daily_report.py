import pandas as pd

def freeze_thaw():
  df = pd.read_csv("temporarydailydata.csv")
  df = df[df["Max Temp (°C)"] * df["Min Temp (°C)"] < 0]
  df = df[["Max Temp (°C)", "Min Temp (°C)"]]
  print(df)

def heat_wave():
  df = pd.read_csv("temporarydailydata.csv")
  df = df[["Max Temp (°C)"]].rolling(3).min()
  df = df[df["Max Temp (°C)"] > 30]
  print(df.size)

# more info: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.index.html 