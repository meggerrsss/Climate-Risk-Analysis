# want to create a chart from a dataframe formatted like the daily climate data

# create dataframe
import pandas as pd
import matplotlib.pyplot as plt


def runplot(col = 7):
  # using example4.csv for now
  data = pd.read_csv('temporarydailydata.csv')

  print(data)
  headings = data.head()


  plt.close("all")
  data.plot(x="Date/Time", y=["Max Temp (°C)"])
  plt.show()

