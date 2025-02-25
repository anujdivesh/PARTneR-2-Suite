from functools import cmp_to_key

# returning negative means left item should be sorted before the right item
def sort_winds(left, right):
    if left['WindSpeed'] != right['WindSpeed']:
        return right['WindSpeed'] - left['WindSpeed']

    # same windspeed: Track Uncertainty is always the lowest
    if left['Danger'] == 'Track Uncertainty' or right['Danger'] == 'Track Uncertainty':
        return 1 if left['Danger'] == 'Track Uncertainty' else -1

    # RMW is always the highest
    if left['Danger'] == 'Radius of Maximum Winds' or right['Danger'] == 'Radius of Maximum Winds':
        return -1 if left['Danger'] == 'Radius of Maximum Winds' else 1

    if left['Danger'].startswith('Possible') or right['Danger'].startswith('Possible'):
        return 1 if left['Danger'].startswith('Possible') else -1

    # shrug?
    return 1

def function(winds):
    if len(winds) == 0:
        return None

    return sorted(winds, key=cmp_to_key(sort_winds))[0]
    

