#  -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 15:09:59 2024

@author: antonioh
"""
import datetime as dt
import os

import make_forcings as mf
import run_model as rm
import process_output as po
import bathtub_flood as bf
import helper as gpath
import shutil
from datetime import datetime
import sys
#CREATE LOG FILE
filename = "/QuickSurge/logs.txt"

def writelog(msg,filename):
    now = datetime.now() # current date and time
    date_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    f = open(filename,'r+')
    lines = f.readlines() # read old content
    f.seek(0) # go back to the beginning of the file
    f.write(date_time+' : '+msg+'\n')# write new content at the beginning
    for line in lines: # write old content after new
        f.write(line)
    f.close()


if os.path.exists(filename):
    os.remove(filename)
    print(f"Clearing log file.")

file = open(filename, 'w')  # Open the file in write mode\
file.close()      
writelog('Starting model run...',filename)

#Load directory paths
paths = gpath.load_paths()
is_pending = gpath.get_input_file(paths.baseDir)[0]

# # Define cyclone, country and track file
# stormname = 'Lola'
# stormyear = 2023
# domain_code = 'TO'
# trackfile = '/media/judith/10TB/QuickSurge/BestTrack/20231023T030000Z_Official_Forecast_Track_2324_01F_Lola_TO.csv'


# # Define cyclone, country and track file
# stormname = 'Lola'
# stormyear = 2023
# domain_code = 'CK_north'
# trackfile = '/media/judith/10TB/QuickSurge/BestTrack/20231023T030000Z_Official_Forecast_Track_2324_01F_Lola_CK_north.csv'


# # Define cyclone, country and track file
# stormname = 'Lola'
# stormyear = 2023
# domain_code = 'CK_south'
# trackfile = '/media/judith/10TB/QuickSurge/BestTrack/20231023T030000Z_Official_Forecast_Track_2324_01F_Lola_CK_south.csv'


# # Define cyclone, country and track file
# stormname = 'Lola'
# stormyear = 2023
# domain_code = 'SA'
# trackfile = '/media/judith/10TB/QuickSurge/BestTrack/20231023T030000Z_Official_Forecast_Track_2324_01F_Lola_SA.csv'


# Define cyclone, country and track file
# stormname = 'Gita'
# stormyear = 2018
# domain_code = 'TO'
# trackfile = '/media/judith/10TB1/QuickSurge/BestTrack/Official_Forecast_Track_GITA_SA.csv'


# Define cyclone, country and track file
# stormname = 'Gita'
# stormyear = 2018
# domain_code = 'TO'
# trackfile = '/media/judith/10TB1/QuickSurge/BestTrack/20180207T060000Z_GP_Analysis_Track_XXXX_XXF_GITA.csv'


# Define cyclone, country and track file
# stormname = 'Harold'
# stormyear = 2020
# domain_code = 'TO'
# trackfile = '/media/judith/10TB1/QuickSurge/BestTrack/20200402T060000Z_GP_Analysis_Track_1920_12F_Harold.csv'

if is_pending:
    writelog('Step 1 : Found a model run file, executing...',filename)
    input_file_path = gpath.get_input_file(paths.baseDir)[1]
    run_file = gpath.open_file(input_file_path)
    stormname = run_file.stormName
    stormyear = run_file.stormYear
    domain_code = run_file.domainCode
    trackfile = "/QuickSurge/"+run_file.trackFile
    # Define cyclone, country and track file
    #stormname = 'Meena'
    #stormyear = 2005
    #domain_code = 'CK_south'
    #trackfile = '/QuickSurge/BestTrack/20050201T000000Z_GP_Analysis_Track_XXXX_XXF_MEENA.csv'

    # number of proccessors
    nproc = 20
    # define running folder
    pathruns = '/QuickSurge/Runs/'
    # define location of the mesh data to use
    input_folder = '/QuickSurge/Input_files/' + domain_code + '/'
    # tide model
    tide_model_dir = '/QuickSurge/Tides/'
    # output_locations_csv1 = input_folder + 'coastline_points.csv'
    output_locations_csv1 = input_folder + 'shore_vertices_' + domain_code + '.csv'
    input_geotiff = input_folder + 'merged_WGS84.tif'
    subdomains = input_folder + 'bathtub_domains_' + domain_code + '.shp'
    aux_points = input_folder + 'inner_vertices_' + domain_code + '.shp'
    outfilename1 = 'TWL_results.csv'


    # read TCtrack csv
    storm = mf.read_RMSC_Fiji_TCtracks(trackfile)
    storm.vmax = mf.fill_nan(storm.vmax).copy()
    storm.mslp = mf.fill_nan(storm.mslp).copy()
    storm.lon[storm.lon<0] += 360

    # define and create parent directory
    pathres = os.path.join(pathruns + stormname +
                        str(stormyear) + '_' + domain_code)
    mf.make_run_folder(pathres)

    #Move Config file to runs Folder
    shutil.move(input_file_path, paths.baseDir+"Runs/"+stormname + str(stormyear) + '_' + domain_code+"/"+gpath.get_input_file(paths.baseDir)[3])
    shutil.move(trackfile,paths.baseDir+"Runs/"+stormname + str(stormyear) + '_' + domain_code+"/"+gpath.get_input_file(paths.baseDir)[3])
    #print(paths.baseDir+"Runs/"+stormname + str(stormyear) + '_' + domain_code+"/"+gpath.get_input_file(paths.baseDir)[3])
    #print(input_file_path)
    #sys.exit(0)
    # ramp up the model, creatide tide only run directory
    pathramp = os.path.join(pathres + '/ramp/')
    # in case of updating the simulation with a newer TC analysis track
    # check if the model has been already rampped up
    newrun, ramp = mf.define_run_directory(pathres)
    # plot country domain and track
    po.plot_track_domain(input_folder, pathres, storm,
                        stormname, stormyear, newrun)

    # check if the hotstart has been created, if not ramp up the tide
    if not os.path.isfile(pathramp+'fort.67'):
        
        print('ramping up tide') 
        # generate path to ramp up the model
        mf.make_run_folder(pathramp) 
        # copy files needed to run ADCIRC only
        mf.copy_remaining_forcing_files_and_change_dates(input_folder, pathramp, pathramp)
        # get the part of the track inside the domain
        storm_ = mf.trackinsidemesh(storm,pathramp)
        # generate ADCIRC meteorological forcing fort.22, just to define the times to spin up the model
        mf.generate_fort22_from_tropycal(storm_,pathramp,rampdays=4)   
        start_time,end_time = mf.get_start_and_end_time_from_besttrack(pathramp  +'fort.22')
        end_time2 = start_time+dt.timedelta(days=4)  # 4 days of ramping up
        # modify the dates in ADCIRC configuration file (fort.15)
        mf.change_dates_and_copy_f15_ramp(input_folder,pathramp,start_time,end_time2)
        # generate tidal harmonics (amplitude and phase) and tidal potential for the simulation
        mf.fill_tide_fort15(pathramp,tide_model_dir,start_time,end_time)
        # run the model, tide only
        rm.run_ramp_model(nproc, pathramp)
        
        # po.plot_and_save_figures(pathramp)
        # xy = np.array([[168.38,-11.62],[167.37,-16.06],[167.32,-15.94]])
        # po.plot_timser_at_point_locations(pathramp,input_folder,xy,start_time,True)


    print('tide has been aready ramped up')    

    # define and generate path of the new run
    pathnewrun = os.path.join(pathres + '/'+ newrun +'/')
    pathresults = os.path.join(pathnewrun,'results/')
    mf.make_run_folder(pathnewrun)    
    mf.make_run_folder(pathresults) 


    # copy files needed to run ADCIRC+SWAN in coupled mode, it should copy the hotstartfile too (fort.67)
    mf.copy_remaining_forcing_files_and_change_dates(input_folder,pathres,pathnewrun)
    # get the part of the track inside the domain
    storm_ = mf.trackinsidemesh(storm,pathnewrun)
    # generate ADCIRC meteorological forcing fort.22
    mf.generate_fort22_from_tropycal(storm_,pathnewrun,rampdays=4) 
    # define the times of the simulation
    start_time,end_time = mf.get_start_and_end_time_from_besttrack(pathnewrun +'fort.22')
    # modify the dates in ADCIRC configuration file (fort.15)
    mf.change_dates_and_copy_f15_swan(input_folder,pathnewrun,start_time,end_time)
    start_time_ = start_time+dt.timedelta(days= 4) 
    # generate tidal harmonics (amplitude and phase) and tidal potential for the simulation
    mf.fill_tide_fort15(pathnewrun,tide_model_dir,start_time,end_time)
    # modify the dates in SWAN configuration file (fort.26)
    mf.change_dates_and_copy_f26(input_folder,pathnewrun,start_time_,end_time)
    # run the model, coupled ADCIRC+SWAN
    rm.run_model_hotstart(nproc, pathnewrun)

    # plot maps of storm tide and Hs maxima
    po.plot_and_save_figures(pathnewrun)
    po.ADCIRC_SWAN_2_tiff(pathnewrun)
    # generate csv with the TWL estimated along the coast (wave contribution is included with Merrifield et al., 2014)
    po.store_output_max_at_point_locations(pathnewrun,output_locations_csv1,outfilename1)

    po.plot_merrifield(pathnewrun,outfilename1,'TWL_merrifield')

    # generate inundation extends by interesecting the TWL 2D surface with island subdomains
    bathtubextends = os.path.join(pathresults,'bathtubextends/')
    mf.make_run_folder(bathtubextends) 
    twl_points = pathresults + 'TWL_results.csv'
        
    bf.bathtub_flood(input_geotiff,subdomains,twl_points,aux_points,bathtubextends)

    # optional
    # define start time  to plot timeseries
    # import numpy as np
    # start_time_ = start_time+dt.timedelta(days= 4) 
    # # based on the storm tide map define a few points to check timeseries
    # xy = np.array([[168.38,-11.62],[167.37,-16.06],[167.32,-15.94]])
    # po.plot_timser_at_point_locations(pathnewrun,input_folder,xy,start_time_,True)
else:
    writelog(gpath.get_input_file(paths.baseDir)[2],filename)
    print(gpath.get_input_file(paths.baseDir)[2])
