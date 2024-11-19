#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 12:26:21 2024

@author: judith
"""


import datetime as dt
import os 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from matplotlib import pyplot as plt

import tropycal.tracks as tracks


import make_forcings as mf 
import run_model as rm
import process_output  as po 


## Define domain
domain_code = 'Niue'

## number of proccessors
nproc = 40
ramp = True
pathruns = '/media/judith/10TB1/ECIKS/synthetic_TCs_Niue/'
## define location of the mesh data to use
input_folder = '/media/judith/10TB1/ECIKS/synthetic_TCs_Niue/common/'
## tide model
#tide_model_dir = '/media/judith/10TB1/QuickSurge/Tides/'
output_locations_csv1 = input_folder + 'eval_Niue_XB_transects_20241007_LL.csv'
outfilename1 = 'point_results.csv'

# read list of selected storm
df = pd.read_csv('/media/judith/10TB1/ECIKS/synthetic_TCs_Niue/common/synthetic_TCs_Niue.csv', header=None)
    
tcs = np.unique(df[0])
tcs.max()



for itc in range(0,tcs.max()):
    
    try: 
    
        indices = df.index[df[0] == itc].tolist()
          
        # Define cyclone name, year and id
        stormname= str(itc) .zfill(3)
        
        dfa = np.array(df.iloc[indices,:].astype(int))      
        times = np.array([dt.datetime(year, month, day, hour) for year, month, day, hour in zip(dfa[:,1], dfa[:,2],dfa[:,3], dfa[:,4])])
    
        dfa = np.array(df.iloc[indices,:].astype(float))    
        storm = mf.Storm_synt(dfa[:, 5], dfa[:, 6], dfa[:, 8], dfa[:, 7], times)
    
        # define and create parent directory
        pathres = os.path.join(pathruns + stormname +
                               '_' + domain_code + '/')
        mf.make_run_folder(pathres)
    
        pathnewrun = pathres
        pathresults = os.path.join(pathnewrun, 'results/')
        mf.make_run_folder(pathnewrun)
        mf.make_run_folder(pathresults)
    
        mf.copy_remaining_forcing_files_and_change_dates(
            input_folder, pathres, pathnewrun)
        # get the part of the track inside the domain
        storm_ = mf.trackinsidemesh(storm, pathnewrun)
        # generate ADCIRC meteorological forcing fort.22
        start_time_real = storm_.time[0]
        end_time_real = storm_.time[-1]
        
        datetimes = [start_time_real,end_time_real]
        dft = pd.DataFrame({'datetime': datetimes})
        dft.to_csv(pathresults + 'datetimes.csv', index=False)
                    
        
        
        mf.generate_fort22_from_tropycal(storm_, pathnewrun, rampdays=0)
        # define the times of the simulation
        start_time, end_time = mf.get_start_and_end_time_from_besttrack(
            pathnewrun + 'fort.22')
        # modify the dates in ADCIRC configuration file (fort.15)
        mf.change_dates_and_copy_f15_swan(
            input_folder, pathnewrun, start_time, end_time)
        # generate tidal harmonics (amplitude and phase) and tidal potential for the simulation
        # mf.fill_tide_fort15(pathnewrun, tide_model_dir, start_time_real, end_time_real)
        # modify the dates in SWAN configuration file (fort.26)
        mf.change_dates_and_copy_f26(input_folder, pathnewrun, start_time, end_time)
        # run the model, coupled ADCIRC+SWAN
        #rm.run_model(nproc, pathnewrun)
        
        # plot maps of storm tide and Hs maxima
        po.plot_and_save_figures(pathnewrun)
        
        # generate csv with the TWL estimated along the coast (wave contribution is included with Merrifield et al., 2014)
        po.store_output_max_at_point_locations_angle(pathnewrun,output_locations_csv1,outfilename1)
        plt.close('all')

    except :
        print("TC: %s doesn't get into the domain" % (str(itc)))

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
        
        
        
        
        
        
        
        
        