# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 13:48:51 2025

@author: wds_chris.lander
"""
import xarray as xr
import os
import gc
# import time
# import glob
import xclim
# from datetime import datetime
import pandas as pd
from tqdm import tqdm
# from dask.diagnostics import ProgressBar
# import canesm_reproject

#=======================================================================================================================
# Declare Arrays
#=======================================================================================================================
model_arr   = ['CanESM5'] #i
param_arr   = ['prfr'] #k
param_units = ['kg m-2 s-1']#k
scenario_arr= ['historical','ssp245','ssp585'] #j
variant_arr = ['r1i1p2f1'] # 'r3i1p1f1','r4i1p1f1'] #l
stat_arr    = ['']

#=======================================================================================================================
# Define input folder
#=======================================================================================================================
basefolder = r'D:\Climate Data\CanRCM5'
file_folder = r'prfr\ssp245'
inputfolder = os.path.join(basefolder,file_folder)


#=======================================================================================================================
# Define output folder and create if doesn't exist
#=======================================================================================================================
outputfolder = os.path.join(inputfolder,'output')
if not os.path.exists(outputfolder):
    # Create the folder
    os.makedirs(outputfolder)

# inputfile = os.path.join(outputfolder,'prfr_NAM-12_CanESM5_ssp245_r1i1p2f1_OURANOS_CRCM5_v1-r1_1hr_2070-12-31_tot_2041-2070_.nc')
# df=xr.open_dataset(inputfile)

    
#=======================================================================================================================
# generates an average of the data
#=======================================================================================================================
def average_variable(ds_merged, start_time, end_time, param, stat, scenario):
    # Initialize an array to store the sum of the bands
    
    starttime = ''.join([char for char in start_time if char != "-"])
    starttime = starttime[:6]
    endtime = ''.join([char for char in end_time if char != "-"])
    endtime = endtime[:6]
            
    df = ds_merged #.sel(time=slice(start_time, end_time))
    
    out_file = os.path.join(basefolder, param + '\\' + param +'_NAM-12_CanESM5_' + scenario + '_r1i1p2f1_OURANOS_CRCM5_v1-r1_day_' + starttime+"-"+ endtime + "_30y_tot" + stat + ".nc")
   
    
    # df = ds_merged.sel(time=slice(start_time, end_time))

    average_band = df.mean('time')
    # sum_band = df.sum('time')
    average_band.to_netcdf(out_file)
    
    print("NetCDF file " + os.path.basename(out_file) + " created successfully!")

def list_files_in_range(directory, start, end):
    files_in_range = []
    for file in os.listdir(directory):
        # Extract numeric part from file name if applicable
        try:
            for yr in range(start, end):
                index = file.find(str(yr))
                if index != -1:
                    files_in_range.append(directory + '\\' + file)
        except ValueError:
            continue  # Skip files without numeric parts
    return files_in_range



count = 0                

# Clear old files in the output directory
for file in os.listdir(outputfolder):
    if file.endswith(".tif") or file.endswith(".xml"):
        os.remove(os.path.join(outputfolder, file))

i = j = k = l = 0

#------------------------------------------------------------------------------------------ 
# Main
#------------------------------------------------------------------------------------------
for k in range(len(param_arr)):
    for j in range(len(scenario_arr)):
        inputfolder = os.path.join(basefolder,param_arr[k],scenario_arr[j])
        outputfolder = basefolder + "\\"  + param_arr[k] +"\\" + scenario_arr[j] +"\\output\\"
        
        if not os.path.exists(outputfolder):
          os.makedirs(outputfolder)
          
        # Iterate over files in directory to convert hourly data into daily
        for name in os.listdir(inputfolder):
            #checks if a file has been previously created or if a folder
            if name.endswith("reproj.nc") or name.endswith("merged.nc") or name.endswith("tot.nc") or name.endswith("reproj.tif")  or not name.endswith(".nc"):
                print("skipping generated file: ")
            else:
                # Open file
                with open(os.path.join(inputfolder, name)) as f:
                
                    param = param_arr[k]
     
                    ncfile = os.path.splitext(f.name)[0]
                    basename = os.path.basename(ncfile)
    
                    infile = os.path.join(ncfile+ ".nc")
    
                    df=xr.open_dataset(infile)
                    df[param]
                    df[param].units

                    
                    # determine start and end time from filename
                    if scenario_arr[j] == 'historical':
                        YR = int(basename[64:68])
                        starttime = basename[64:76]
                        endtime = basename[77:89]
                    else:
                        YR = int(basename[60:64])
                        starttime = basename[60:72]
                        endtime = basename[73:85]
                        
                    startyear = starttime[0:4]
                    startmonth = starttime[4:6]
                    startday = starttime[6:8]
                                  
 
                              
                    
                    start_time = str(YR) + "-" + "01" + "-" + "01"
                    end_time = str(YR) + "-" + "12" + "-" + "31"
   
                    #outfile = basename.replace(starttime + "-" + endtime, start_time)
                    outfile = os.path.join(outputfolder,basename + "_tot.nc")

                    #clip to time frame of interest                   
                    if os.path.exists(outfile):
                         print( outfile + " already exists. Skipping!")
                    else:
                        # df_tc = df.sel(time=slice(start_time,end_time))
                        # df_tc.attrs["units"] = 'kg/m2/s'

                        # df =  xclim.core.units.convert_units_to(df[param], "mm/s")
                        df[param] = xclim.core.units.rate2amount(df[param], dim = 'time', sampling_rate_from_coord=False)
                        df_sum = df.sum('time')
                        # df[param] = df[param] * 86400
                        time_arr = pd.date_range(start_time, periods=1)

                        # start_timer = time.time()
                        # sum_bands = df_tc['prfr'].sum('time')
                        df_sum = df_sum.expand_dims(time= time_arr)
                        
                        # time.sleep(2)
                        # end_timer = time.time()
                        # execution_time = end_timer - start_timer
                        # print(f"Execution time: {execution_time:.2f} seconds")
                        
                        # average_band = df_tc.mean('time')
                        # sum_bands = (sum_bands * 3600) # converts from kg m-2 s-1 to mm/day

                        # Your code here
                        df_sum.to_netcdf(outfile)

                        del df_sum
                        del df
                        gc.collect()
                        
                        print("NetCDF file " + os.path.basename(outfile) + " created successfully!")

                        # inputfolder = outputfolder
                        # input_files = glob.glob(inputfolder + "/*.nc")
                        
                        # datasets = [xr.open_dataset(f) for f in input_files]
                        # merged = xr.concat(datasets, dim="time")
                        # merged.to_netcdf(outputfolder + '\prfr_NAM-12_CanESM5_ssp245_r1i1p2f1_OURANOS_CRCM5_v1-r1_day_2026-2070_tot_merged.nc')

        #------------------------------------------------------------------------------------
        # Historical
        #------------------------------------------------------------------------------------
        if scenario_arr[j] == 'historical':
            
            #define time frame of interest                   
            start_time = '1985-01-01'
            end_time = '2014-12-31'
            startyear = start_time[0:4]
            endyear = end_time[0:4]

            input_files = list_files_in_range(outputfolder, int(startyear), int(endyear)+1)
            
            # # Open all NetCDF files as a Dask-backed xarray dataset
            # datasets = [xr.open_dataset(f) for f in tqdm(input_files)]
            # combined_dataset = xr.concat(datasets, dim="time")

            # # Enable Dask progress bar
            # with ProgressBar():
            #     combined_dataset = combined_dataset.compute()
    
            print("Merging data::" + start_time + ' = ' + end_time)
            
            mergefolder = os.path.join(inputfolder,'merged')
            if not os.path.exists(mergefolder):
                # Create the folder
                os.makedirs(mergefolder)
            
            merge_file = param_arr[k]+ "_" + model_arr[i] + "_" + scenario_arr[j] + "_" + variant_arr[l] + "_" + startyear + "-" + endyear  + "_merged.nc"
            merge_file = os.path.join(mergefolder,merge_file)
            
            ds_merged = xr.concat([xr.open_dataset(f) for f in input_files], dim = 'time')
            ds_merged.to_netcdf(merge_file)
            print(scenario_arr[j] + " Data merged:" + start_time + ' - ' + end_time)
            # print(f"Execution time: {execution_time:.2f} seconds")
                              
            average_variable(ds_merged, start_time, end_time, param_arr[k], '', scenario_arr[j])
            
            del ds_merged
            gc.collect()  

        else:
        #------------------------------------------------------------------------------------
        # Near Future
        #------------------------------------------------------------------------------------
            start_time = '2027-01-01'
            end_time = '2056-12-31'   
            startyear = start_time[0:4]
            endyear = end_time[0:4]

            input_files = list_files_in_range(outputfolder, int(startyear), int(endyear)+1)
            
            print("Merging data::" + start_time + ' = ' + end_time)
            
            mergefolder = os.path.join(inputfolder,'merged')
            if not os.path.exists(mergefolder):
                # Create the folder
                os.makedirs(mergefolder)
            
            merge_file = param_arr[k]+ "_" + model_arr[i] + "_" + scenario_arr[j] + "_" + variant_arr[l] + "_" + startyear + "-" + endyear  + "_merged.nc"
            merge_file = os.path.join(mergefolder,merge_file)
            
            # ds_merged = xr.open_mfdataset(
            #         input_files,
            #         combine='nested',
            #         concat_dim="time"
            #      )  
            
            # # Display progress
            # ProgressBar(ds_merged)
            
            
         
            ds_merged = xr.concat([xr.open_dataset(f) for f in tqdm(input_files)], dim = 'time')
            ds_merged.to_netcdf(merge_file)
            print(scenario_arr[j] + " Data merged:" + start_time + ' - ' + end_time)
            # print(f"Execution time: {execution_time:.2f} seconds")

            average_variable(ds_merged, start_time, end_time, param_arr[k], '', scenario_arr[j])
            del ds_merged
            # gc.collect()  
            
        #------------------------------------------------------------------------------------
        #Mid Future
        #------------------------------------------------------------------------------------
            start_time = '2041-01-01'
            end_time = '2070-12-31'   
            startyear = start_time[0:4]
            endyear = end_time[0:4]

            input_files = list_files_in_range(outputfolder, int(startyear), int(endyear)+1)
            
            print("Merging data::" + start_time + ' = ' + end_time)
            
            mergefolder = os.path.join(inputfolder,'merged')
            if not os.path.exists(mergefolder):
                # Create the folder
                os.makedirs(mergefolder)
            
            merge_file = param_arr[k]+ "_" + model_arr[i] + "_" + scenario_arr[j] + "_" + variant_arr[l] + "_" + startyear + "-" + endyear  + "_merged.nc"
            merge_file = os.path.join(mergefolder,merge_file)
            
            ds_merged = xr.concat([xr.open_dataset(f) for f in tqdm(input_files)], dim = 'time')
            ds_merged.to_netcdf(merge_file)
            print(scenario_arr[j] + " Data merged:" + start_time + ' = ' + end_time)
            # print(f"Execution time: {execution_time:.2f} seconds")

            average_variable(ds_merged, start_time, end_time, param_arr[k], '', scenario_arr[j])
            del ds_merged
            gc.collect()  

