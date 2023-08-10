import numpy as np
import xarray as xr


# __all__= [ minuspipi_to_twopi, twopi_to_minuspipi, hav, archav,  thetaphi_to_unit_xyz ]

def minuspipi_to_twopi(x):
    """
    Converts (-pi, pi) to (0, 2pi)
    """
    return (x < 0.) * (x + 2 * np.pi) + (x >= 0.) * x



def twopi_to_minuspipi(x:np.ndarray)->np.ndarray:
    """
    Converts (0, 2pi) to (-pi, pi)
    """
    return (x <= np.pi) * x + (x > np.pi) * (x - 2 * np.pi)




def hav(x:np.ndarray)->np.ndarray:
    """
    Returns the haversine of the argument
    defined as 
    hav(x) = sin^2(x/2)
    """
    _temp = np.sin(x/2.)
    return _temp * _temp




def archav(y:np.ndarray)->np.ndarray:
    """
    Returns the inverse haversine of the argument
    See hav
    """
    return 2 * np.arcsin(np.sqrt(y))




def thetaphi_to_unit_xyz(theta:np.ndarray, phi:np.ndarray)->tuple[np.ndarray, np.ndarray, np.ndarray]:
    "converts angles theta, phi to (x, y, z) on unit circle"
    return (np.sin(theta) * np.cos(phi), 
            np.sin(theta) * np.sin(phi),
            np.cos(theta)
            )
    
