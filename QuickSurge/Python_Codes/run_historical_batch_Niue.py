#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 09:52:33 2024

@author: judith
"""



import datetime as dt
import os 
import pandas as pd
import matplotlib.pyplot as plt


import tropycal.tracks as tracks


import make_forcings as mf 
import run_model as rm
import process_output  as po 


## Define domain
domain_code = 'Niue'

## number of proccessors
nproc = 40
ramp = True
pathruns = '/media/judith/10TB1/ECIKS/historic_TCs_Niue/'
## define location of the mesh data to use
input_folder = '/media/judith/10TB1/ECIKS/historic_TCs_Niue/common/'
## tide model
tide_model_dir = '/media/judith/10TB1/QuickSurge/Tides/'
output_locations_csv1 = input_folder + 'eval_pts_100_LL_20241104_LL.csv'
outfilename1 = 'point_results100.csv'

basin = tracks.TrackDataset(basin='south_pacific', source='ibtracs', ibtracs_mode='wmo',interpolate_data='True',
                             ibtracs_url='/media/judith/10TB1/QuickSurge_04032024/BestTrack/ibtracs.SP.list.v04r01.csv')


# read list of selected storm
df = pd.read_csv('/media/judith/10TB1/ECIKS/historic_TCs_Niue/common/selected_historic_Niue.csv')
    

for itc in range(1,len(df.id)):
    
    # Define cyclone name, year and id
    stormname = df.tcname[itc]
    print(stormname)
    stormyear = df.tcyear[itc]
    id = df.id[itc]
    
    try:
    
        # # id = basin.get_storm_id(storm=(stormname[i] ,stormyear[i]))
        # id = basin.get_storm_id(storm=(stormname ,stormyear))
        # storm = basin.get_storm((stormname, stormyear))
        
        storm = basin.get_storm(id)
        
        
        storm.lon[storm.lon<0] += 360
        storm.vmax = mf.fill_nan(storm.vmax).copy()
        try:
            storm.mslp = mf.fill_nan(storm.mslp).copy()   
        except:     
            storm.mslp =-(storm.vmax/3.86)**(1/0.645)+1010;
        
        # define and create parent directory
        pathres = os.path.join(pathruns + stormname + '_' + str(stormyear) + '_'  + domain_code + '/')
        mf.make_run_folder(pathres) 
        # pathresults = os.path.join(pathres,'results/')
        # mf.make_run_folder(pathresults) 
        
        basin.plot_storm(id,domain="dynamic",plot_all_dots='true',save_path=pathres+'Track')
        
        # ramp up the model, creatide tide only run directory
        pathramp = os.path.join(pathres + '/ramp/')
        
        # in case of updating the simulation with a newer TC analysis track
        # check if the model has been already rampped up
        newrun, ramp = mf.define_run_directory(pathres)
        
        # # plot country domain and track
        # po.plot_track_domain(input_folder,pathres,storm,stormname,stormyear,newrun)
        
        # check if the hotstart has been created, if not ramp up the tide
        if not os.path.isfile(pathramp+'fort.67'):
            
            print('ramping up tide') 
            # generate path to ramp up the model
            mf.make_run_folder(pathramp) 
            # copy files needed to run ADCIRC only
            mf.copy_remaining_forcing_files_and_change_dates(input_folder, pathramp, pathramp)
            # get the part of the track inside the domain
            storm_ = mf.trackinsidemesh(storm, pathramp)
            # generate ADCIRC meteorological forcing fort.22, just to define the times to spin up the model
            start_time_real = storm_.time[0]
            end_time_real = storm_.time[-1]
            
            datetimes = [start_time_real,end_time_real]
            dft = pd.DataFrame({'datetime': datetimes})
            dft.to_csv(pathramp + 'datetimes.csv', index=False)
                        
            time_diff = start_time_real - dt.datetime(2000, 1, 5, 0, 0)# ADCIRC only handles one natural year, it will crash with the TC going before 31 December
            storm_.time = storm_.time - time_diff
            
            mf.generate_fort22_from_tropycal(storm_, pathramp, rampdays=4)
            start_time,end_time = mf.get_start_and_end_time_from_besttrack(pathramp  +'fort.22')
            end_time2 = start_time+dt.timedelta(days= 4) # 4 days of ramping up 
            # modify the dates in ADCIRC configuration file (fort.15)
            mf.change_dates_and_copy_f15_ramp(input_folder,pathramp,start_time,end_time2)
            # generate tidal harmonics (amplitude and phase) and tidal potential for the simulation
            mf.fill_tide_fort15(pathramp,tide_model_dir,start_time_real,end_time_real)
            # run the model, tide only
            #rm.run_ramp_model(nproc, pathramp)
            
            # po.plot_and_save_figures(pathramp)
            # xy = np.array([[168.38,-11.62],[167.37,-16.06],[167.32,-15.94]])
            # po.plot_timser_at_point_locations(pathramp,input_folder,xy,start_time,True)
        
        
        print('tide has been aready ramped up')    
        
        # define and generate path of the new run
        pathnewrun = os.path.join(pathres + '/' + newrun + '/')
        pathresults = os.path.join(pathnewrun, 'results/')
        mf.make_run_folder(pathnewrun)
        mf.make_run_folder(pathresults)
        
        
        # copy files needed to run ADCIRC+SWAN in coupled mode, it should copy the hotstartfile too (fort.67)
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
                    
        time_diff = start_time_real - dt.datetime(2000, 1, 5, 0, 0)# ADCIRC only handles one natural year, it will crash with the TC going before 31 December
        storm_.time = storm_.time - time_diff
        
        mf.generate_fort22_from_tropycal(storm_, pathnewrun, rampdays=4)
        # define the times of the simulation
        start_time, end_time = mf.get_start_and_end_time_from_besttrack(
            pathnewrun + 'fort.22')
        # modify the dates in ADCIRC configuration file (fort.15)
        mf.change_dates_and_copy_f15_swan(
            input_folder, pathnewrun, start_time, end_time)
        start_time_ = start_time+dt.timedelta(days=4)
        # generate tidal harmonics (amplitude and phase) and tidal potential for the simulation
        mf.fill_tide_fort15(pathnewrun, tide_model_dir, start_time_real, end_time_real)
        # modify the dates in SWAN configuration file (fort.26)
        mf.change_dates_and_copy_f26(input_folder, pathnewrun, start_time_, end_time)
        # run the model, coupled ADCIRC+SWAN
        rm.run_model_hotstart(nproc, pathnewrun)
        
        # plot maps of storm tide and Hs maxima
        po.plot_and_save_figures(pathnewrun)
        
        # generate csv with the TWL estimated along the coast (wave contribution is included with Merrifield et al., 2014)
        po.store_output_max_at_point_locations_angle(pathnewrun,output_locations_csv1,outfilename1)
        plt.close('all')
        
    except:
        
        print("All done")
        
        # po.plot_merrifield(pathnewrun,outfilename1,'TWL_merrifield')
        
        # # optional
        # # define start time  to plot timeseries
        # start_time_ = start_time+dt.timedelta(days= 4) 
        # # based on the storm tide map define a few points to check timeseries
        # xy = np.array([[168.38,-11.62],[167.37,-16.06],[167.32,-15.94]])
        # po.plot_timser_at_point_locations(pathnewrun,input_folder,xy,start_time_,True)
