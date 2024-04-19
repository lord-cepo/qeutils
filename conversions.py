import numpy as np

# k_alat = [0.072118, -0.041637, 0.009725]
# k_crystal = [ 0.02840909, 0, 0]

# k_base = np.linalg.inv(r_base).T

def k_alat2crystal_ibrav5(c4, x):
    '''
    converts a k point in alat coordinates to crystal coordinates, assuming ibrav=5
    parameters:
        c4: celldm(4) = cos(gamma) 
        x: k point in alat coordinates
    returns:
        k point in crystal coordinates
    '''
    tx = np.sqrt((1-c4)/2)
    ty = np.sqrt((1-c4)/6)
    tz = np.sqrt((1+2*c4)/3)
    r_base = np.array([
        [tx, -ty, tz],
        [0, 2*ty, tz],
        [-tx, -ty, tz]
    ])
    return np.dot(r_base, x)
