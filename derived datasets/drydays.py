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
histname = "drydays_NAM-22_CCCma-CanESM2_historical_r1i1p1_CCCma-CanRCM4_r2_day_19500101-20051231.nc"
name45 = "drydays_NAM-22_CCCma-CanESM2_rcp45_r1i1p1_CCCma-CanRCM4_r2_day_20060101-21001231.nc"
name85 = "drydays_NAM-22_CCCma-CanESM2_rcp85_r1i1p1_CCCma-CanRCM4_r2_day_20060101-21001231.nc"
names = [histname, name45, name85]
newfolder = r"C:\Data\drydays"


for ind,ds in enumerate(dslist):
    dry = xclim.indices.dry_days(ds.pr, thresh='0.2 mm/d', freq='YS', op='<')
    newds = dry.to_dataset(name = "drydays")
    newds = newds.compute()
    newds.attrs = ds.attrs
    newds.drydays.attrs['xclim conversion'] = "CanRCM4 pr dataset converted using xclim.indices.dry_days(ds.pr, thresh='0.2 mm/d', freq='YS', op='<')"
    print(newds)

    newpath = os.path.join(newfolder,names[ind])
    newds.to_netcdf(newpath)
    print(f"file at {newpath}")


