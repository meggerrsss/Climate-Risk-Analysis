import xarray as xr
import os
import cftime
import sys
sys.path.append(r"C:\Users\CAMG038492\Code\Climatology\rasterization")
import rotated_coordinate #type:ignore

# primarily an attempt to open all canrcm4 datasets at once and process it manually, at a point, bypassing the raster creation step
# dask is a nightmare though, and values cannot be extracted easily without significant memory use at the final stage
# defeats the purpose

folder = r"C:\Data\ros"

histsub = os.path.join(folder,'historical','originals')

hist = xr.open_mfdataset("C:\\Data\\ros\\historical\\originals\\*.nc",
                         combine = 'by_coords',
                         chunks = None,
                         parallel = False)
hist = rotated_coordinate.rotated_pole_2_regular(hist, input_format = 'ds', setting = 'canrcm4')

r45 = xr.open_mfdataset("C:\\Data\\ros\\rcp45\\originals\\*.nc",
                         combine = 'by_coords',
                         chunks = None,
                         parallel = False)
r45 = rotated_coordinate.rotated_pole_2_regular(r45, input_format = 'ds', setting = 'canrcm4')

r85 = xr.open_mfdataset("C:\\Data\\ros\\rcp85\\originals\\*.nc",
                         combine = 'by_coords',
                         chunks = None,
                         parallel = False)
r85 = rotated_coordinate.rotated_pole_2_regular(r85, input_format = 'ds', setting = 'canrcm4')

intervals = [ [1976,2005], [1991,2020], [2021,2050], [2051,2080], [2071,2100]]
scens = ['hist','r45','r85']
loc = [-53.251,47.427]

d = {} # key is interval, value is scen/time-subsetted dataset
for scen in scens:
    for inte in intervals:
        starttime = cftime.DatetimeNoLeap(inte[0], 1, 1)
        endtime = cftime.DatetimeNoLeap(inte[1], 12, 31)
        if scen == "hist":
            subset = hist.sel(time = slice(starttime,endtime))
        if scen == "r45":
            subset = r45.sel(time = slice(starttime,endtime))
        if scen == "r85":
            subset = r85.sel(time = slice(starttime,endtime))

        #spot = subset.sel(lat = loc[1], lon = loc[0], method = 'nearest')
        for var in list(subset.data_vars):
            combo = f"{scen} {inte} {var}"
            print(combo)
            q = subset[var].mean(dim = 'time') #
            r = q
            s = r.sel(lat = loc[1], lon = loc[0], method = 'nearest') # location filtering
            t = s.compute() # yeah this method isn't going to work
            d[combo] = t
            print(t)
            exit()

print(d)
#d.to_netcdf(r"C:\Users\CAMG038492\Code\Wood-Climate\test.nc")