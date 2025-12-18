# creating drydays from canrcm4 using xclim

import xarray as xr
import xclim
import os


prhistfolder = r"C:\Data\pr\historical\originals\*.nc"
pr45folder = r'C:\Data\pr\rcp45\originals\*.nc'
pr85folder = r'C:\Data\pr\rcp85\originals\*.nc'
histds = xr.open_mfdataset(prhistfolder, combine='by_coords')
ds45 = xr.open_mfdataset(pr45folder, combine='by_coords')
ds85 = xr.open_mfdataset(pr85folder, combine='by_coords')
dslist = [histds, ds45, ds85]
newvalue = "pr50"
histname = "drydays_NAM-22_CCCma-CanESM2_historical_r1i1p1_CCCma-CanRCM4_r2_day_19500101-20051231.nc".replace("drydays",newvalue)
name45 = "drydays_NAM-22_CCCma-CanESM2_rcp45_r1i1p1_CCCma-CanRCM4_r2_day_20060101-21001231.nc".replace("drydays",newvalue)
name85 = "drydays_NAM-22_CCCma-CanESM2_rcp85_r1i1p1_CCCma-CanRCM4_r2_day_20060101-21001231.nc".replace("drydays",newvalue)
names = [histname, name45, name85]
newfolder = r"C:\Data\drydays".replace("drydays",newvalue)


for ind,ds in enumerate(dslist):
    #temp = xclim.indices.snw_storm_days(ds.pr, thresh='50cm/d', freq='YS-JUL')
    #temp = xclim.indices.snowfall_frequency(ds.pr, thresh='10 mm/day', freq='YS-JUL')
    #temp = xclim.indices.days_with_snow(ds.pr, low='50 kg m-2 d-1', high='1E6 kg m-2 d-1', freq='YS-JUL')
    temp = xclim.indices.generic.count_occurrences(ds.pr, threshold = '50 kg m-2 d-1', freq = 'YS', op = '>', constrain=None)

    newds = temp.to_dataset(name = newvalue)
    newds = newds.compute()
    newds.attrs = ds.attrs
    newds[newvalue].attrs['xclim conversion'] = "CanRCM4 pr dataset converted using xclim.indices.generic.count_occurrences(ds.pr, threshold = '50 kg m-2 d-1', freq = 'YS', op = '>', constrain=None)"
    newds[newvalue].attrs['long_name'] = "Number of days per year where pr > 50 kg/m^2"
    print(newds)
    newpath = os.path.join(newfolder,names[ind])
    newds.to_netcdf(newpath)
    print(f"file at {newpath}")


