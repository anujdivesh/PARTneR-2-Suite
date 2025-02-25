import WindDamage_Loss_Buildings
import WindDamage_Loss_Infrastructure

def function(exposure, hazard):
    asset_type = exposure['Asset']

    if hazard is None or hazard == 0:
        return {'Exposure': 0, 'Loss_p16': 0, 'Loss_p50': 0, 'Loss_p84': 0, 'Vulnerability_curve': 'N/A'}

    if asset_type == 'Population' or exposure['Value'] == 0:
        return {'Exposure': 1, 'Loss_p16': 0, 'Loss_p50': 0, 'Loss_p84': 0, 'Vulnerability_curve': 'N/A'}

    if asset_type == 'Building':
        return WindDamage_Loss_Buildings.function(exposure, hazard)
    elif asset_type == 'Crop':
        # TODO crop loss function still needed
        return {'Exposure': 1, 'Loss_p16': 0, 'Loss_p50': 0, 'Loss_p84': 0, 'Vulnerability_curve': 'N/A'}
    else:
        return WindDamage_Loss_Infrastructure.function(exposure, hazard)

