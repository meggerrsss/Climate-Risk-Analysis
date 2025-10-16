import pandas as pd
import xarray as xr
import numpy as np
import os
import tomllib as tomli
from datetime import datetime

with open('config.toml', 'rb') as f:
    conf = tomli.load(f)

folder = conf['folder']
scens = conf['scenarios']
intervals = conf['intervals']
threshold = 15.0

# from annual files
def anndiurnaltemperaturevariation():
    dbmin = xr.open_dataset(os.path.join(folder, 'tn_min.nc'))
    dbmax = xr.open_dataset(os.path.join(folder, 'tx_max.nc'))
    dbmin, dbmax = xr.align(dbmin, dbmax, join = 'exact')
    #diff = np.subtract(dbmax, dbmin)
    dbdiff = dbmax.copy(deep = True)
    for var in list(dbdiff.data_vars):
        var = var.replace('tx_max','var')
        dbdiff[var] = np.subtract(dbmax[var.replace('var','tx_max')],dbmin[var.replace('var','tn_min')])
    dbdiff = dbdiff.drop_vars([x for x in list(dbdiff.data_vars) if "tx_max" in x])
    return dbdiff


# using the daily files in folders by variable name, convert the diurnal diff to one megamerged file
def dailydiurnaltempvar():
    tasminlist = os.listdir(os.path.join(folder,'tasmin'))
    tasmaxlist = os.listdir(os.path.join(folder,'tasmax'))
    filesfull = []
    #filesfilt = []

    for item in tasminlist:
        name = item.replace('tasmin','diurnalvar')
        dbmin = xr.open_dataset(os.path.join(folder,'tasmin',item))
        dbmax = xr.open_dataset(os.path.join(folder,'tasmax',item.replace('tasmin','tasmax')))
        dbmin, dbmax = xr.align(dbmin, dbmax, join = 'exact')

        dbdiff = dbmax.copy(deep = True)
        for var in list(dbdiff.data_vars):
            var = var.replace('tasmax','var')
            dbdiff[name] = np.subtract(dbmax[var.replace('var','tasmax')],dbmin[var.replace('var','tasmin')])
        dbdiff = dbdiff.drop_vars([x for x in list(dbdiff.data_vars) if "tasmax" in x])
        dbdiff = dbdiff.convert_calendar("standard", use_cftime = True, align_on='year')
        #dbfilt = dbdiff.where(dbdiff >= threshold)

        filesfull.append(dbdiff)
        #filesfilt.append(dbfilt)
    ds_merged = xr.concat(filesfull, dim="filetitle", data_vars="different")
    ds_merged.to_netcdf(os.path.join(folder, 'diurnal-variation', 'generated_full.nc'))

    #ds_filt = xr.concat(filesfilt, dim="filetitle", data_vars="different")
    #ds_filt.to_netcdf(os.path.join(folder, 'diurnal-variation', 'generated_filt.nc'))
    return ds_merged



def write():
    # opening the diurnal diff file again
    varidb = xr.open_dataset(os.path.join(folder, 'diurnal-variation', 'generated_full.nc'))

    intervals = conf['intervals']

    # converting to threshold exceedence # xr.where(ds["value"] >= 80, 1., 0.)
    filtered = xr.where(varidb >= 15, 1., 0.)

    # making the csv
    filename = os.path.join(folder, 'diurnal-variation', 'output.xlsx')

    with pd.ExcelWriter(filename) as writer:

        for inte in intervals:

            starttime = datetime(year=inte[0], month=1, day=1)
            endtime = datetime(year=inte[1], month=12, day=31)
            subset = filtered.sel(time = slice(starttime, endtime))
            mean = subset.mean(dim = 'time')
            intedata = mean.to_pandas().transpose()
            inte_tabname = f"{inte[0]}-{inte[1]}"

            intedata.to_excel(writer, sheet_name=inte_tabname, index=True)


# alright attempt #3 using chris's preferred methodology
# take model average daily high - daily low, determine count of days / 30y that are >= 15

def modelavgfirst():
    maxdata = pd.read_csv(r"C:\Climate-Data\stjohns\tasmax_ssp_averages.csv")
    mindata = pd.read_csv(r"C:\Climate-Data\stjohns\tasmin_ssp_averages.csv")
    maxdata['time'] = pd.to_datetime(maxdata['time'])
    mindata['time'] = pd.to_datetime(mindata['time'])
    maxdata = maxdata.set_index('time')
    mindata = mindata.set_index('time')
    diff = maxdata-mindata
    #range = (np.max(diff), np.min(diff))
    output = pd.DataFrame()
    for inte in intervals:
        starttime = datetime(year=inte[0], month=1, day=1)
        endtime = datetime(year=inte[1], month=12, day=31)
        timefiltered_diff = diff.loc[starttime:endtime]
        thres = timefiltered_diff.where(timefiltered_diff>=15).count()
        output[f"{inte[0]}-{inte[1]}"] = thres
    print(output)

print(modelavgfirst())
