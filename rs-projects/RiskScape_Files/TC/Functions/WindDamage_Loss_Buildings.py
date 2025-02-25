import os
import pandas as pd
import numpy as np
from scipy.stats import truncnorm, scoreatpercentile
from statistics import median

# Define the bounds for the truncated normal distribution
a, b = 0, 1

# Specify folder paths to input data
path = os.path.dirname(__file__)+"/VulnerabilityCurves/buildings/"

# Calculate building loss
def function(exposure, hazard):
    # Define building properties from the exposure layer.
    usebld = exposure["UseType"]   
    framing = exposure["Structure"]
    wall = exposure["Wall_Material"]
    condition = exposure["Condition"] ## this value was an average of the wall, roof and foundation condition
    valueBld = exposure['Value'] ## total value determined from bclasscode, floor area, floor levels and urb percentage

    ## taking all buildings to be Low rise (assumption from Luganville analysis)
    rise='L'

    # Map usage from survey to GAR flood uses
    if usebld == "Residential":
        usebldGAR = 'Residential'
    if usebld == "Out building":
        usebldGAR = 'Residential'
    elif usebld == "Industrial":
        usebldGAR = 'Industrial'
    elif usebld == "Commercial":
        usebldGAR = 'Industrial'
    elif usebld == "Infrastructure":
        usebldGAR = 'Else'
    else:
        usebldGAR = 'Else'
 
    
    # Select GAR material type based on survey data
    # Define W1 and W2 as defaults   
    if usebldGAR == 'Residential':
        label = 'W1'
    else:
        label = 'W2'
    # if there's no framing information, use wall material information
    if framing == '' or framing == 'Unknown' or framing=='Other' or framing == None:
        # if framing is unknown but wall material is concrete, use C4. Otherwise assume wood.
        if wall == 'Concrete':
            label = 'C4'
        elif wall == 'Fibre-cement sheet':
            if usebldGAR == 'Residential':
                label = 'W1'
            else:
                label = 'W2'
        elif usebldGAR == 'Residential':
            label = 'W1'
        else:
            label = 'W2'
    # if there is framing information, use wall material only to clarify
    if framing == 'Concrete column':
        if wall == 'Concrete':
            label = 'C4'
        elif wall == 'Masonry':
            label = 'C3'
        elif usebldGAR == 'Residential':
            label = 'C3'
        elif usebldGAR == 'Industrial':
            label = 'C2'
        elif usebldGAR == 'Else':
            label = 'C2'
    elif framing == 'Wooden pole':
        if usebldGAR == 'Residential':
            label = 'W1'
        else:
            label = 'W2'
    elif framing == 'Timber frame':
        if usebldGAR == 'Residential':
            label = 'W1'
        else:
            label = 'W2'
    elif framing == 'Load bearing wall':
        label = 'URM'
    # if there is no wall, use Falae curve
    if wall == 'None':
        label = 'W1'

    # determine building resistance based on building condition and depending on hazard. Flood: Consider wall condition, Wind: Consider roof condition
    # report:   "Associated with most building types is a Resistance Level (High, Medium, Low, Poor) which is a measure of a building’s resistance to the hazard in question."  
    #           "For flood, where damage is associated with inundation rather than structural strength, three classes of building non-structural component value were proposed rather than notional lateral resistance to flow.
    #           This reflects the greater repair cost incurred for exposure with a more expensive non-structural component. The percentage of building replacement cost that is non-structural is related to building usage."
    # If for a certain build material and resistance level combination, no curve exists, default to the next lower resistance level curve.

    survey_condition = condition
    if survey_condition == "Excellent":
        # for Wind, there is no URM High resistance curve, so we are using Medium
        if label == 'URM' and rise == 'L':
            resistance = 'Medium'
        else:
            resistance = 'High'
    elif survey_condition == "Good":
        if label == 'URM' and rise == 'L':
            resistance = 'Medium'
        else:
            resistance = 'High'
    elif survey_condition == "Fair":
        resistance = 'Medium'    
    elif survey_condition == "Poor":
        resistance = 'Low'
    elif survey_condition == "Very poor":
        resistance = 'Poor'
    else:
        resistance = 'Medium'

    # Select csv_file / curve depending on building properties - original file names
    if label == 'W1' or label == 'W2' or label == 'S3':
        # Account for W1, W2, S3 not having an 'L'/'M'/'H' rise tag
     
        curve_DR = label+"_"+resistance+".csv"
    else:
    
        curve_DR = label+rise+"_"+resistance+".csv"

# Select csv_file / curve depending on building properties - labeled file names
# Reinforced concrete shear walls

    if curve_DR == "C2L_High.csv":
        curve_DR = "W-B_R_H-DR"+".csv"
    if curve_DR == "C2L_Medium.csv":
        curve_DR = "W-B_R_M-DR"+".csv"
    if curve_DR == "C2L_Low.csv":
        curve_DR = "W-B_R_L-DR"+".csv"
    if curve_DR == "C2L_Poor.csv":
        curve_DR = "W-B_R_P-DR"+".csv"
# Concrete Frame with Unreinforced Masonry Infill Walls

    if curve_DR == "C3L_Medium.csv":
        curve_DR = "W-B_R_M.B_SF_CC.B_WC_M-DR"+".csv"
    if curve_DR == "C3L_Low.csv":
        curve_DR = "W-B_R_L.B_SF_CC.B_WC_M-DR"+".csv"            
    if curve_DR == "C3L_High.csv":
        curve_DR = "W-B_R_H.B_SF_CC.B_WC_M-DR"+".csv"
    if curve_DR == "C3L_Poor.csv":
        curve_DR = "W-B_R_P.B_SF_CC.B_WC_M-DR"+".csv"
# Reinforced Concrete Frames and Concrete Shear Walls           

    if curve_DR == "C4L_High.csv":
        curve_DR = "W-B_R_H.B_SF_CC-DR"+".csv"
    if curve_DR == "C4L_Low.csv":
        curve_DR = "W-B_R_L.B_SF_CC-DR"+".csv"
    if curve_DR == "C4L_Medium.csv":
        curve_DR = "W-B_R_M.B_SF_CC-DR"+".csv"
    if curve_DR == "C4L_Poor.csv":
        curve_DR = "W-B_R_P.B_SF_CC-DR"+".csv"

# Unreinforced Masonry Bearing Walls 

    if curve_DR == "URML_Low.csv":
        curve_DR = "W-B_R_L.B_WC_M-DR"+".csv"
    if curve_DR == "URML_Medium.csv":
        curve_DR = "W-B_R_M.B_WC_M-DR"+".csv"
    if curve_DR == "URML_Poor.csv":
        curve_DR = "W-B_R_P.B_WC_M-DR"+".csv"
# Wood, Light Frame (<5,000 sq. ft.)


    if curve_DR == "W1_High.csv":
        curve_DR = "W-B_R_H.B_U_R-DR"+".csv"
    if curve_DR == "W1_Low.csv":
        curve_DR = "W-B_R_L.B_U_R-DR"+".csv"
    if curve_DR == "W1_Medium.csv":
        curve_DR = "W-B_R_M.B_U_R-DR"+".csv"
    if curve_DR == "W1_Poor.csv":
        curve_DR = "W-B_R_P.B_U_R-DR"+".csv"

# Wood, Commercial and Industrial (>5,000 sq. IL.)


    if curve_DR == "W2_High.csv":
        curve_DR = "W-B_R_H.B_U_NR-DR"+".csv"
    if curve_DR == "W2_Low.csv":
        curve_DR = "W-B_R_L.B_U_NR-DR"+".csv"
    if curve_DR == "W2_Medium.csv":
        curve_DR = "W-B_R_L.B_U_NR-DR"+".csv"
    if curve_DR == "W2_Poor.csv":
        curve_DR = "W-B_R_P.B_U_I-DR"+".csv"

    
    # # Generate file path using selected curve
    file_path_DR = os.path.join(path, curve_DR)

    # Read the CSV file into a DataFrame
    df_DR = pd.read_csv(file_path_DR)

    # Wind intensity for vulnerability curve interpolation and Damage ratios for building classes. 
    wind_speed_x_DR = df_DR['IM']
    B_ydr_DR = df_DR['MEAN']

    if hazard == None:
        intensity = 0
    else:
        intensity = hazard
    
    threshold_wind = 120 
    if intensity > threshold_wind:
        exposure = 1.0
    else:
        exposure = 0.0


    # Calculate loss
    if intensity == None:
        lossp16_DR = 0
        lossp50_DR = 0
        lossp84_DR = 0  

    else:
        wind_speed_x_DR = df_DR['IM']
        B_ydr_DR = df_DR['MEAN']
        DR = np.interp(intensity, wind_speed_x_DR, B_ydr_DR)
        mean_DR = DR
    
        std_dev_upper_DR = DR + (DR * 0.2)
        std_dev_lower_DR = DR - (DR * 0.2)
        std_dev_DR = std_dev_upper_DR - std_dev_lower_DR
        
        ## some null values in the data
        if (DR > 0) and (valueBld is not None) and (intensity > threshold_wind):

            loss_DR = truncnorm.rvs((a - mean_DR) / std_dev_DR, (b - mean_DR) / std_dev_DR, loc=mean_DR, scale=std_dev_DR, size=10000)
            lossp16_DR = scoreatpercentile(loss_DR, 16) * valueBld
            lossp50_DR = scoreatpercentile(loss_DR, 50) * valueBld
            lossp84_DR = scoreatpercentile(loss_DR, 84) * valueBld

        else:
            lossp16_DR = 0
            lossp50_DR = 0
            lossp84_DR = 0  

        ## Change output selected curve
        return {'Exposure':exposure, 'Loss_p16': lossp16_DR, 'Loss_p50': lossp50_DR, 'Loss_p84': lossp84_DR, 'Vulnerability_curve':curve_DR}
