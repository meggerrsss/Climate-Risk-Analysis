import xarray as xr
import os
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

## after downloading the downscaled gcm data from climate-data.ca,
## trying to find which file correlates to each climate variable

folder = r"C:\Climate-Data\stjohns"
files = os.listdir(folder)

for file in files:
    db = xr.open_dataset(os.path.join(folder,file))
    firstvar = list(db.data_vars)[0]
    #fullname = db[firstvar].attrs['description']
    print(file, db.attrs, db[firstvar].attrs, file)
    _ = input()


