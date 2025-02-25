# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 14:53:33 2025

@author: judithg
"""

import pandas as pd
import os

inputfiledir = '/mnt/DATA/production/outputs'
outputfile = '/mnt/DATA/production/outputs/cyclone_track.csv'

# def edit_RMSC_track_riskscape(trackfile):
#     trk = pd.read_csv(trackfile,skiprows=6)
#     ftrk = trk[~trk.isin(['# Start of data']).any(axis=1)]
#     ftrk.to_csv('/home/divesha/data/production/outputs/cyclone_track.csv',sep=',',index=False,header=True)
#     return(ftrk)

for ifile in os.listdir(inputfiledir):
    if ifile.endswith('.csv'):
        trk = pd.read_csv(os.path.join(inputfiledir,ifile),skiprows=6)
        ftrk = trk[~trk.isin(['# Start of data']).any(axis=1)]
        ftrk.to_csv(outputfile,sep=',',index=False,header=True)




    
