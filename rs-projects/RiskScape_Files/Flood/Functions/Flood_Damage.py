import numpy as np

# Calculate building loss
def building_loss(buildings, hazard):
    
    # Set defaults flood depths
    floor_height = 0.4
    
    if hazard is None:
        depth = 0
    else:
        depth = hazard - floor_height

    # Flood depths for vulnerability curve interpolation.
    depth_x = [0.0, 0.25, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 10.0]

    # Damage ratios for building classes. Add new array for each new building class. 
    B1_ydr = [0.0, 0.01, 0.02, 0.051, 0.134, 0.329, 0.626, 0.859, 0.989, 1.0]# Class 1 i.e., Residential
    B2_ydr = [0.0, 0.0122, 0.024, 0.052, 0.105, 0.2, 0.345, 0.524, 0.825, 1.0]# Class 2 i.e., Commercial
    B3_ydr = [0.0, 0.0175, 0.035, 0.102, 0.255, 0.504, 0.748, 0.896, 0.986, 1.0]# Class 3 i.e., Industrial or infrastructure
    B4_ydr = [0.0, 0.0122, 0.024, 0.052, 0.105, 0.2, 0.345, 0.524, 0.825, 1.0]# Class 4 i.e., Public
    B5_ydr = [0.0, 0.025, 0.059, 0.135, 0.296, 0.544, 0.78, 0.915, 0.991, 1.0]# Class 5 i.e., Outbuilding

    # Define building use from exposure layer.
    usebld = buildings["UseType"]
    valuebld = buildings["Value"]

	#Calculate loss
    if usebld == 'Residential':
        damage_ratio = np.interp(depth, depth_x, B1_ydr)
    elif usebld == 'Commercial' or usebld == 'Commercial - Accommodation':
        damage_ratio = np.interp(depth, depth_x, B2_ydr)
    elif usebld == 'Industrial' or usebld == 'Infrastructure':
        damage_ratio = np.interp(depth, depth_x, B3_ydr)
    elif usebld == 'Public':
        damage_ratio = np.interp(depth, depth_x, B4_ydr)
    elif usebld == 'Outbuilding':
        damage_ratio = np.interp(depth, depth_x, B5_ydr)
    else:
        damage_ratio = np.interp(depth, depth_x, B1_ydr)# Class 1 as default vulnerability curve

    loss = int(damage_ratio * valuebld)
    return {'Direct_Loss': loss}

# Calculate crop loss
def crop_loss(crops, depth):
	
	# Flood depths for depth-damage curve interpolation.
    depth_x = [0.0, 0.25, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.1, 10.0]

    # Damage ratios for point infrastructure classes. Add new array for each new crop class. 
    CR1_ydr = [0.0, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.65, 1.0]# Class 1 i.e., Tree Crop 
    CR2_ydr = [0.0, 0.025, 0.5, 1, 1, 1, 1, 1, 1, 1.0]# Class 2 i.e., Annual, root and other crops
	
	# Define infrastructure point use from exposure layer.
    useCR = crops["UseType"]
#    subuseCR = crops["SubUseType"]
    valueCR = crops["Value"]

    if useCR  == 'Tree Crop':
        damage_ratio = np.interp(depth, depth_x, CR1_ydr)
    else:
        damage_ratio = np.interp(depth, depth_x, CR2_ydr)

    loss = int(damage_ratio * valueCR)
    return {'Direct_Loss': loss}

# Calculate road loss	
def road_loss(infrastructure_lines, depth):
	
	# Flood depths for depth-damage curve interpolation.
    depth_x = [0.0, 0.25, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.1, 10.0]

    # Damage ratios for point infrastructure classes. Add new array for each new infrastructure class. 
    IL1_ydr = [0.0, 0.01, 0.03, 0.08, 0.11, 0.13, 0.16, 0.21, 0.25, 1.0]# Class 1 i.e., Sealed Road
    IL2_ydr = [0.0, 0.08, 0.16, 0.23, 0.3, 0.33, 0.39, 0.42, 0.45, 1.0]# Class 2 i.e., Unsealed Road

	# Define infrastructure point use from exposure layer.
    useIL = infrastructure_lines["UseType"]
    valueIL = infrastructure_lines["Value"]

    if useIL  == 'primary':
        damage_ratio = np.interp(depth, depth_x, IL1_ydr)
    else:
        damage_ratio = np.interp(depth, depth_x, IL2_ydr)

    loss = int(damage_ratio * valueIL)
    return {'Direct_Loss': loss}

# Calculate infrastructure loss
def infrastructure_loss(exposure, depth):
	
	# Flood depths for depth-damage curve interpolation.
    depth_x = [0.0, 0.25, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.1, 10.0]

    # Damage ratios for point infrastructure classes. Add new array for each new infrastructure class. 
    IP1_ydr = [0.0, 0.1, 0.24, 0.36, 0.44, 0.52, 0.56, 0.6, 0.62, 1.0]# Class 1 i.e., Facilities
    IP2_ydr = [0.0, 0.1, 0.24, 0.36, 0.44, 0.52, 0.56, 0.6, 0.62, 1.0]# Class 2 i.e., Substations
    IP3_ydr = [0.0, 0.09, 0.18, 0.34, 0.4, 0.52, 0.58, 0.64, 0.7, 1.0]# Class 3 i.e., Storage, nodes
    IP4_ydr = [0.0, 0.2, 0.08, 0.14, 0.16, 0.185, 0.21, 0.23, 0.25, 1.0]# Class 4 i.e., Bridges
    IP5_ydr = [0.0, 0.2, 0.3, 0.45, 0.575, 0.65, 0.725, 0.8, 0.9, 1.0]# Class 5 i.e., Buildings
    
	# Define infrastructure point use from exposure layer.
    useIP = exposure["UseType"]
    valueIP = exposure["Value"]
	
    if useIP  == 'Communication' or useIP  == 'Generator' or useIP  ==  'Fossil Fuel Power Plant' or useIP  ==  'Hybrid Fossil Fuel and Solar Power Plant' or useIP  ==  'Solar Power Plant' or useIP  == 'Water Treatment' or useIP == 'Hydroelectric Power Plant' or useIP == 'Wind Farm':
        damage_ratio = np.interp(depth, depth_x, IP1_ydr)
    elif useIP  ==  'Sub-Station':
        damage_ratio = np.interp(depth, depth_x, IP2_ydr)
    elif useIP  == 'Water Intake' or useIP  == 'Storage Tank' or useIP  == 'Satellite Dish':
        damage_ratio = np.interp(depth, depth_x, IP3_ydr)
    elif useIP ==  'Non-Steel/Concrete Bridge' or useIP  ==  'Concrete Bridge' or useIP  ==  'Steel Bridge' or useIP  ==  'Helipad':
        damage_ratio = np.interp(depth, depth_x, IP4_ydr)
    elif useIP ==  'Bus Station':
        damage_ratio = np.interp(depth, depth_x, IP5_ydr)
    elif useIP ==  'Dam' or useIP ==  'Mine':
        damage_ratio = 0
    else:
        damage_ratio = np.interp(depth, depth_x, IP1_ydr)# Class 1 as default depth-damage curve

    loss = int(damage_ratio * valueIP)
    return {'Direct_Loss': loss}

# Calculate airport/port infrastructure
def infrastructure_ports_loss(exposure, depth):
	
	# Flood depths for depth-damage curve interpolation.
    depth_x = [0.0, 0.25, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.1, 10.0]

    # Damage ratios for point infrastructure classes. Add new array for each new infrastructure class. 
    IPG1_ydr = [0.0, 0.01, 0.025, 0.04, 0.065, 0.085, 0.105, 0.125, 0.15, 1.0]# Class 1 i.e., Paved Airport
    IPG2_ydr = [0.0, 0.08, 0.16, 0.23, 0.3, 0.33, 0.39, 0.42, 0.45, 1.0]# Class 2 i.e., Unpaved Airport
    IPG3_ydr = [0.0, 0.02, 0.04, 0.08, 0.12, 0.14, 0.2, 0.3, 0.32, 1.0]# Class 3 i.e., Port pavement
	
	# Define infrastructure point use from exposure layer.
    useIPG = exposure["UseType"]
    valueIPG = exposure["Value"]

    if useIPG  == 'Paved Airport':
        damage_ratio = np.interp(depth, depth_x, IPG1_ydr)
    elif useIPG  == 'Unpaved Airport':
        damage_ratio = np.interp(depth, depth_x, IPG2_ydr)
    elif useIPG  == 'Dock' or useIPG  == 'Port':
        damage_ratio = np.interp(depth, depth_x, IPG3_ydr)
    else:
        damage_ratio = np.interp(depth, depth_x, IPG2_ydr)

    loss = int(damage_ratio * valueIPG)
    return {'Direct_Loss': loss}

def function(exposure, hazard):
    asset_type = exposure['Asset']

    if hazard is None or hazard == 0:
        return {'Direct_Loss': 0}

    if asset_type == 'Population' or exposure['Value'] == 0 or asset_type == 'Unknown':
        return {'Direct_Loss': 0}

    if asset_type == 'Building':
        return building_loss(exposure, hazard)
    elif asset_type == 'Road':
        return road_loss(exposure, hazard)
    elif asset_type == 'Crop':
        return crop_loss(exposure, hazard)
    elif asset_type == 'Port' or asset_type == 'Airport':
        return infrastructure_ports_loss(exposure, hazard)
    else:
        return infrastructure_loss(exposure, hazard)

