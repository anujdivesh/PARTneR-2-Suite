import os.path
import pandas as pd
import numpy as np
from scipy.stats import truncnorm, scoreatpercentile
from statistics import median

# Define the bounds for the truncated normal distribution
a, b = 0, 1

# Specify folder paths to input data
path = os.path.dirname(__file__)+"/VulnerabilityCurves/"

def function(exposure, hazard):

    # Define infrastructure use from exposure layer.
    usetype = exposure['UseType']
    asset = exposure['Asset']
    value = exposure['Value'] 

    # Read index.csv that maps from a exposure type to a curve CSV file
    lookup_df = pd.read_csv(os.path.join(path, 'index.csv'))
    lookup_df = lookup_df.set_index(['Asset', 'UseType'])
    if (asset, usetype) not in lookup_df.index:
        # unknown sub-type - just use the 'default' curve for that asset type
        usetype = 'default'

    curve_details = lookup_df.loc[(asset, usetype)]


    # now get the specific curve CSV file we want to use
    file_path_DR = os.path.join(path, curve_details['dir'], curve_details['file'])
    df_DR = pd.read_csv(file_path_DR)
 
    if hazard == None:
        intensity = 0
    else:
        intensity = hazard
    
    threshold_wind = 120 
    if intensity > threshold_wind:
        exposure = 1.0
    else:
        exposure = 0.0


   # Intensities for vulnerability curve interpolation and Damage ratios for building classes. 
    intensity_x_DR = df_DR['IM']
    B_ydr_DR = df_DR['MEAN']

    # Calculate loss       
    
    if intensity == None:
        lossp50_DR = 0
        lossp16_DR = 0
        lossp84_DR = 0

    else:
        intensity_x_DR = df_DR['IM']
        B_ydr_DR = df_DR['MEAN']

        
        damage_ratio = np.interp(intensity, intensity_x_DR, B_ydr_DR)
        
        mean = damage_ratio
        std_dev_upper = damage_ratio + (damage_ratio * 0.2)
        std_dev_lower = damage_ratio - (damage_ratio * 0.2)
        std_dev = std_dev_upper - std_dev_lower

        if (damage_ratio > 0.0) and (value is not None) and (intensity > threshold_wind):
            loss = truncnorm.rvs((a - mean) / std_dev, (b - mean) / std_dev, loc=mean, scale=std_dev, size=10000)

            lossp50_DR = scoreatpercentile(loss, 50) *value
            lossp16_DR = scoreatpercentile(loss, 16) *value
            lossp84_DR = scoreatpercentile(loss, 84) *value
    

        else:
            lossp50_DR = 0
            lossp16_DR = 0
            lossp84_DR = 0


        
        ## Change output selected curve
        return {'Exposure': exposure, 'Loss_p16': lossp16_DR, 'Loss_p50': lossp50_DR, 'Loss_p84': lossp84_DR, 'Vulnerability_curve': curve_details['file']}
