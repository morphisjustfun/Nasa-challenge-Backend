from ..constants.constants import constantsVaccines

def getVaccineEffect (dose, brand, risk):
    if dose == 0:
        return risk
    
    elif dose == 1:
        if brand == constantsVaccines['PFIZER']:
            return risk * (1 - 0.78)
        elif brand == constantsVaccines['ASTRAZENECA']:
            return risk * (1 - 0.6401)
        elif brand == constantsVaccines['SINOPHARM']:
            return risk * (1 - 0.68397)
        else:
            return risk * ((1 - 0.68397) + (1 - 0.6401) + (1 - 0.78))/3
        
    elif dose == 2:
        if brand == constantsVaccines['PFIZER']:
            return risk * (1 - 0.95)
        elif brand == constantsVaccines['ASTRAZENECA']:
            return risk * (1 - 0.704)
        elif brand == constantsVaccines['SINOPHARM']:
            return risk * (1 - 0.79)
        else:
            return risk * ( (1 - 0.79) + (1 - 0.704) + (1 - 0.95))/3
