#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 13:24:19 2024

@author: judith
"""
import os
import shutil
import pandas as pd

from datetime import datetime

pathruns = '/media/judith/10TB1/ECIKS/historic_TCs_Rarotonga/'
domain_code = 'Rarotonga'

destination = '/media/judith/10TB1/ECIKS/historic_TCs_Rarotonga/results_historic/'

# read list of selected storm
df = pd.read_csv('/media/judith/10TB1/ECIKS/historic_TCs_Rarotonga/common_5d/selected_historic_Rarotonga.csv')
    

for itc in range(1,len(df.id)):
    
    try:
    
        stormname = df.tcname[itc]
        stormyear = df.tcyear[itc]
        
        pathorig = os.path.join(pathruns + stormname + '_' + str(stormyear) + '_'  + domain_code + '/Run_000/results/')
        
        dtimes = pd.read_csv(pathorig +  'datetimes.csv')
        
        try:
            date1 = datetime.strptime(dtimes['datetime'][0],'%Y-%m-%d %H:%M:%S')
        except: 
            date1 = datetime.strptime(dtimes['datetime'][0],'%Y-%m-%d')
            
        try:    
            date2 = datetime.strptime(dtimes['datetime'][1],'%Y-%m-%d %H:%M:%S')
        except:
            date2 = datetime.strptime(dtimes['datetime'][1],'%Y-%m-%d')
        
        midpoint = date1 + (date2 - date1) / 2
    
        source_file = pathorig + '/' + 'point_results.csv'
        
        destination_file = destination +  midpoint.strftime('%d-%b-%Y') +'.csv'
    
        shutil.copy2(source_file, destination_file)
        
    except:
        
        print("TC %s has not run succesfully" % (stormname ))



























