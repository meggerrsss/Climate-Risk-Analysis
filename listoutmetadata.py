import xarray as xr
import os
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

## after downloading the downscaled gcm data from climate-data.ca,
## trying to find which file correlates to each climate variable

folder = r"C:\Climate-Data\stjohns\annual data"
files = os.listdir(folder)

for file in files:
    db = xr.open_dataset(os.path.join(folder,file))
    firstvar = list(db.data_vars)[0]
    #fullname = db[firstvar].attrs['description']
    print(file, db.attrs, db[firstvar].attrs, file)
    _ = input()

dic = {
    "cdd":"Maximum consecutive days with daily precipitation below 1 mm/day",
    "cddcold_18":"Cumulative sum of temperature degrees for mean daily temperature above 18 degc",
    "dlyfrzthw_tx0_tn-1":"Number of days where maximum daily temperatures are above 0 degc and minimum daily temperatures are at or below -1 degc",
    "first_fall_frost":"First day of year with a period of at least 1 days of minimum temperature below 0 degc",
    "frost_days":"Number of days where the daily minimum temperature is below 0 degc",
    "frost_free_season":"Maximum number of consecutive days with minimum temperature at or above 0 degc",
    "gddgrow_0":"Cumulative sum of temperature degrees for mean daily temperature above 0 degc",
    "gddgrow_5":"Cumulative sum of temperature degrees for mean daily temperature above 5 degc",
    "hddheat_18":"Cumulative sum of temperature degrees for mean daily temperature below 18 degc",
    "HXmax30":"Number Of Days Per year with Daily Humidex Greater Than 30",
    "HXmax35":"Number Of Days Per year with Daily Humidex Greater Than 35",
    "HXmax40":"Number Of Days Per year with Daily Humidex Greater Than 40",
    "ice_days":"Number of days with maximum daily temperature below 0 degc",
    "last_spring_frost":"Last day of minimum daily temperature below a threshold of 0 degc for at least 1 days before a given date (07-15)",
    "nr_cdd":"Number of dry periods of 6 day(s) or more, during which the maximal precipitation on a window of 6 day(s) is below 1.0 mm",
    "prcptot":"Total accumulated precipitation",
    "r10mm":"Number of days with daily precipitation at or above 10 mm/day",
    "r1mm":"Number of days with daily precipitation at or above 1 mm/day",
    "r20mm":"Number of days with daily precipitation at or above 20 mm/day",
    "rx1day":"Maximum 1-day total precipitation",
    "rx5day":"Maximum 5-day total precipitation amount",
    "tnlt_-15":"The number of days with minimum temperature below -15 degc",
    "tnlt_-25":"The number of days with minimum temperature below -25 degc",
    "tn_mean":"Mean daily minimum temperature",
    "tn_min":"Minimum daily minimum temperature",
    "tr_18":"Number of days with minimum daily temperature above 18 degc",
    "tr_20":"Number of days with minimum daily temperature above 20 degc",
    "tr_22":"Number of days with minimum daily temperature above 22 degc",
    "txgt_25":"The number of days with maximum temperature above 25 degc",
    "txgt_27":"The number of days with maximum temperature above 27 degc",
    "txgt_29":"The number of days with maximum temperature above 29 degc",
    "txgt_30":"The number of days with maximum temperature above 30 degc",
    "txgt_32":"The number of days with maximum temperature above 32 degc",
    "tx_max":"Maximum daily maximum temperature",
    "tx_mean":"Mean daily maximum temperature"
}
