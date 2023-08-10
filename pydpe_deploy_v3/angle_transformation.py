from enum import Enum
from typing import Tuple

import numpy as np
import xarray as xr

#local imports
import utils


"""
Sample orientation requires the following coordinates, 
theta_s : np.float ,
phi_s : np.float , 
rotation_s : np.float
"""

class Det(Enum):
    DETA = 1
    DETB = 2


theta_d_center = np.radians(90)
phi_d_centers = {
                    Det.DETA : np.radians(0.0001),
                    Det.DETB : np.radians(90),
                }

def detector_angle_to_global_angle(theta:np.ndarray, phi:np.ndarray, which_det:Det)->Tuple[np.ndarray, np.ndarray]:
    """
    Converts angles from detector coordinates to global coordinates
    """
    global theta_d_center, phi_d_centers #theta_d_center isn't used?
    phi_d_center = phi_d_centers[which_det] #Should be 0 or pi/2 radians depending on the detector
    
    phi = utils.twopi_to_minuspipi(phi)

    theta_g = np.arccos( np.sin(theta) * np.cos(phi) )     
    phi_g_offset =  np.arcsin( np.sin(phi) * np.sin(theta)/np.sin(theta_g) )
    
    return (theta_g, phi_d_center - phi_g_offset)



def global_angle_to_sample_angle(theta_s:np.ndarray, phi_s:np.ndarray,
                                 theta_g:np.ndarray, phi_g:np.ndarray)->Tuple[np.ndarray, np.ndarray]:
    """
    Converts angles from global angles to sample angles including rotation of sample about sample normal 
    """
    alpha = 2 * np.arcsin(
                    np.hypot(
                        np.sin( (theta_g - theta_s)/2. ), 
                        np.sqrt( np.sin(theta_g) * np.sin(theta_s) )    * np.sin(    (phi_g - phi_s)/2.    ) 
                    )
            )

    _temp = phi_s - phi_g 
    # mimics sign function with sign(0) = 1
    beta_sign = np.piecewise(
         _temp,
         condlist=[_temp >= 0., _temp<0],
         funclist=[1., -1.]
    )
    
    gamma = (theta_g - theta_s - alpha)/2.
    _temp = beta_sign * 2. *\
    np.arcsin( 
        np.sqrt(
            ( np.sin(alpha + gamma) / np.sin(alpha) ) * 
            ( np.sin(theta_s + gamma) / np.sin(theta_s) )
        ) 
    )

    beta = utils.minuspipi_to_twopi(_temp)
    return (alpha, beta)            



def internal_angle_to_k(Ek:np.ndarray, theta:np.ndarray, phi:np.ndarray)->Tuple[np.ndarray, np.ndarray]:
    """
    Converts angles to momenta
    """
    k_mag = 0.512 * np.sqrt(Ek) * np.sin(theta)
    return ( k_mag * np.cos(phi+np.pi/2), k_mag * np.sin(phi+np.pi/2) )




def analyser_angle_to_k(theta_s:np.ndarray, phi_s:np.ndarray, rotation_s:np.ndarray,
                        Ek:np.ndarray, theta:np.ndarray, phi:np.ndarray, which_det:Det)->Tuple[np.ndarray, np.ndarray]:
    """
    Converts angles from analyser coordinates to momenta  
    """
    v1, v2 = detector_angle_to_global_angle(theta, phi, which_det)
    w1, w2 = global_angle_to_sample_angle(theta_s, phi_s, v1, v2)
    return internal_angle_to_k(Ek, w1, w2+rotation_s)   
        



def forward_transformation(data:xr.Dataset, sample_orientation:dict)->xr.Dataset:
    """"
    Transformation from angle->k space
    sample_orientation dictionary must contain the following variables:
        theta_s
        phi_s
        rotation_s
    """
    Ek1 = data.coords['E1'].values
    Ek2 = data.coords['E2'].values
    theta1 = data.coords['theta1'].values
    theta2 = data.coords['theta2'].values
    phi1 = data.coords['phi1'].values
    phi2 = data.coords['phi2'].values

    theta_s = sample_orientation["theta_s"]
    phi_s = sample_orientation["phi_s"]
    rotation_s = sample_orientation["rotation_s"]

    kx1, ky1 = analyser_angle_to_k(theta_s, phi_s, rotation_s, Ek1, theta1, phi1, Det.DETA)
    kx2, ky2 = analyser_angle_to_k(theta_s, phi_s, rotation_s, Ek2, theta2, phi2, Det.DETB)



    d_ret = data.copy(deep=True) 
    d_ret.rename(
                    {
                        'theta1' : 'kx1', 
                        'theta2' : 'kx2',
                        'phi1' : 'ky1',
                        'phi2' : 'ky2'
                     }
                )

    d_ret['kx1'].values = kx1
    d_ret['kx2'].values = kx2
    d_ret['ky1'].values = ky1
    d_ret['ky2'].values = ky2


    return d_ret


def backward_transformation(reference_data:xr.DataArray,
                            sample_orientation:dict,
                            Ek:np.ndarray,
                            which_det:Det, 
                            det_FOV:np.ndarray=np.radians(15),
                            grid_dimensions:Tuple[int, int]=[151, 361]  )->xr.DataArray:
    """
    Calculates backward transformation from k -> angle for alignment of samples 
    """

    theta_s = sample_orientation["theta_s"]
    phi_s = sample_orientation["phi_s"]
    rotation_s = sample_orientation["rotation_s"]

    _theta = np.linspace(0, det_FOV, grid_dimensions[0])
    _phi = np.linspace(0, 2.* np.pi, grid_dimensions[1]) 
    _theta_grid, _phi_grid = np.meshgrid(_theta, _phi)
    # _Ek = Ek * np.ones_like(_theta_grid)
    
    v1, v2 = analyser_angle_to_k(theta_s, phi_s, rotation_s, Ek, _theta_grid, _phi_grid, which_det)
    kx = xr.DataArray(v1.transpose(), dims=['theta', 'phi'], coords={'theta':_theta, 'phi':_phi})
    ky = xr.DataArray(v2.transpose(), dims=['theta', 'phi'], coords={'theta':_theta, 'phi':_phi})
    _transform = reference_data.interp(kx=kx, ky=ky)

    _jac = np.abs(
            kx.differentiate('theta')  * ky.differentiate('phi') -\
            kx.differentiate('phi') * ky.differentiate('theta')
            )
    
    return _transform * _jac
