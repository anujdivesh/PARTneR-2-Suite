#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 11:41:57 2024

@author: judith
"""
import os
import shutil
import pandas as pd
import numpy as np

from datetime import datetime

pathruns = '/media/judith/10TB1/ECIKS/synthetic_TCs_Rarotonga/'
domain_code = 'Rarotonga'

destination = '/media/judith/10TB1/ECIKS/synthetic_TCs_Rarotonga/resuts_synthetic/'

# read list of selected storm
df = pd.read_csv('/media/judith/10TB1/ECIKS/synthetic_TCs_Rarotonga/common/synthetic_TCs_Rarotonga.csv', header=None)
    
tcs = np.unique(df[0])
    

for itc in range(1,tcs.max()):
    
    try:

        stormname= str(itc) .zfill(3)
        

        pathorig = os.path.join(pathruns + stormname + '_'  + domain_code + '/results/')
        
      
    
        source_file = pathorig + '/' + 'point_results.csv'
        
        destination_file = destination +  stormname +'.csv'
    
        shutil.copy2(source_file, destination_file)
        
    except:
        
        print("TC %s has not run succesfully" % (stormname ))
