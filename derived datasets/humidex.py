# creating drydays from canrcm4 using xclim
# attempt 1: uses entire dataset, probably too big
import xarray as xr
import xclim
import os

# setting up input datasets
tashistfolder = r"C:\Data\tas\historical\originals\*.nc"
tas45folder = r'C:\Data\tas\rcp45\originals\*.nc'
tas85folder = r'C:\Data\tas\rcp85\originals\*.nc'
histtasds = xr.open_mfdataset(tashistfolder, combine='by_coords')
dstas45 = xr.open_mfdataset(tas45folder, combine='by_coords')
dstas85 = xr.open_mfdataset(tas85folder, combine='by_coords')
taslist = [histtasds, dstas45, dstas85]

husshistfolder = r"C:\Data\huss\historical\originals\*.nc"
huss45folder = r'C:\Data\huss\rcp45\originals\*.nc'
huss85folder = r'C:\Data\huss\rcp85\originals\*.nc'
histhussds = xr.open_mfdataset(husshistfolder, combine='by_coords')
dshuss45 = xr.open_mfdataset(huss45folder, combine='by_coords')
dshuss85 = xr.open_mfdataset(huss85folder, combine='by_coords')
husslist = [histhussds, dshuss45, dshuss85]

pshistfolder = r"C:\Data\ps\historical\originals\*.nc"
ps45folder = r'C:\Data\ps\rcp45\originals\*.nc'
ps85folder = r'C:\Data\ps\rcp85\originals\*.nc'
histpsds = xr.open_mfdataset(pshistfolder, combine='by_coords')
dsps45 = xr.open_mfdataset(ps45folder, combine='by_coords')
dsps85 = xr.open_mfdataset(ps85folder, combine='by_coords')
pslist = [histpsds, dsps45, dsps85]

# output datasets
parametername = "humidex30"
histname = "parametername_NAM-22_CCCma-CanESM2_historical_r1i1p1_CCCma-CanRCM4_r2_day_19500101-20051231.nc".replace("parametername",parametername)
name45 = "parametername_NAM-22_CCCma-CanESM2_rcp45_r1i1p1_CCCma-CanRCM4_r2_day_20060101-21001231.nc".replace("parametername",parametername)
name85 = "parametername_NAM-22_CCCma-CanESM2_rcp85_r1i1p1_CCCma-CanRCM4_r2_day_20060101-21001231.nc".replace("parametername",parametername)
names = [histname, name45, name85]
newfolder = r"C:\Data\parametername".replace("parametername",parametername)

def attempt1():
    for ind,ds in enumerate(husslist):
        print(f"dataset {ind}...")
        print(f"running rh xclim")
        rh = xclim.indices.relative_humidity(taslist[ind].tas, tdps=None, huss=husslist[ind].huss, ps=pslist[ind].ps)
        print(f"running humidex xclim")
        humidex = xclim.indices.humidex(taslist[ind].tas, tdps=None, hurs=rh)
        humidex.attrs['units'] = "K"
        #humidex30 = xclim.indices.generic.count_occurrences(humidex, 273+30, freq='YS', op='>=', constrain=None)
        print(f"running yearly threshold xclim")
        humidex30 = xclim.indices.generic.threshold_count(humidex, op = ">=", threshold = 303, freq = "YS", constrain=None)
        var = parametername

        newds = humidex30.to_dataset(name = var)
        print(f"computing")
        newds = newds.compute()
        newds.attrs = ds.attrs
        newds[var].attrs['xclim conversion 1'] = "RH: CanRCM4 tas huss ps used to calculate rh via xclim.indices.relative_humidity(taslist[ind].tas, tdps=None, huss=husslist[ind].huss, ps=pslist[ind].ps)"
        newds[var].attrs['xclim conversion 2'] = "CanRCM4 tas rh used to calculate humidex via xclim.indices.humidex(taslist[ind].tas, tdps=None, hurs=rh)"
        newds[var].attrs['xclim conversion 3'] = "humidex daycount for annual number of occurrences humidex > 30 via xclim.indices.generic.threshold_count(humidex, op = '>=', threshold = 303, freq = 'YS', constrain=None)"
        print(newds)
        newpath = os.path.join(newfolder,names[ind])
        newds.to_netcdf(newpath)
        print(f"file at {newpath}")

print(attempt1())
### attempt 2, recreates 5y chunks