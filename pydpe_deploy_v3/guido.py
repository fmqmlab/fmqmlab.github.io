import angle_transformation
import io
from js import document, console, Uint8Array, window, File

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img

import skimage.color

import xarray as xr

from enum import IntEnum
import random

def dpe_mod(image_file, extent_x, extent_y, theta_s, phi_s, rotation_s,hv,wf, FOV ):
    E_k1 = (hv-2*wf)/2
    E_k2 = (hv-2*wf)/2
    
    theta_s = np.radians(theta_s)
    phi_s = np.radians(phi_s)
    rotation_s = np.radians(rotation_s)
    FOV = np.radians(FOV)

    _phi = np.linspace(0, 2 * np.pi, 361)
    _theta = FOV * np.ones_like(_phi)
    kp1x, kp1y = angle_transformation.analyser_angle_to_k(theta_s, phi_s, rotation_s, E_k1, _theta, _phi, angle_transformation.Det.DETA)
    kp2x, kp2y = angle_transformation.analyser_angle_to_k(theta_s, phi_s, rotation_s, E_k2, _theta, _phi, angle_transformation.Det.DETB)
    kc1x, kc1y = angle_transformation.analyser_angle_to_k(theta_s, phi_s, rotation_s, E_k1, FOV, np.radians(0), angle_transformation.Det.DETA )
    kc2x, kc2y = angle_transformation.analyser_angle_to_k(theta_s, phi_s, rotation_s, E_k2, FOV, np.radians(0), angle_transformation.Det.DETB )

    extent_list = [extent_y[0], extent_y[1], extent_x[0], extent_x[1], ] ##ky min max kx min max

    
    if image_file == "":
        return
    if image_file != getattr(dpe_mod, "loaded_filename", None) or extent_list != getattr(dpe_mod, 'loaded_extent', None) :
        dpe_mod.loaded_filename = image_file
        dpe_mod.loaded_extent = extent_list


        #Bug in Pyodide's matplotlib.image.imread() - accepts only png. Replacing with Pillow's Image.open() - Fixed
        image_rgb = Image.open(image_file)
        mode = image_rgb.mode

        
        #Change to PIL.Image.convert() in future? Eliminates skimage dependency entirely...
        if mode == 'RGBA' or mode == 'RGBa':
            data = skimage.color.rgb2gray(skimage.color.rgba2rgb(image_rgb)) #rgba2rgb expects a 4 channel image, else throws error, so check if we have 4 channels first
        elif mode == 'L' or mode == '1':
            data = image_rgb #if image is already grayscale, nothing to be done
        else:
            data = skimage.color.rgb2gray(image_rgb) #if image is RGB, convert to grayscale


        dpe_mod.loaded_data = xr.DataArray(data.transpose(), dims=['kx', 'ky'], coords={'ky':np.linspace(extent_list[1], extent_list[0], data.shape[0]),
                                                  'kx':np.linspace(extent_list[2], extent_list[3], data.shape[1])})

   
    
    transform1 = angle_transformation.backward_transformation(dpe_mod.loaded_data, 
                                                                   {'theta_s':theta_s, 'phi_s':phi_s, 'rotation_s':rotation_s}, 
                                                                   E_k1, angle_transformation.Det.DETA, FOV, grid_dimensions=[76, 361])

    transform2 = angle_transformation.backward_transformation(dpe_mod.loaded_data, 
                                                                   {'theta_s':theta_s, 'phi_s':phi_s, 'rotation_s':rotation_s}, 
                                                                   E_k2, angle_transformation.Det.DETB, FOV, grid_dimensions=[76, 361])
    


    document.getElementById("graph-area").innerHTML = '' #clear whatever is inside of graph-area first (this could even be an earlier graph)

    plt.style.use('dark_background')
    fig = plt.figure(figsize=[18, 4.5], dpi = 300)
    ax1 = plt.subplot(131)
    dpe_mod.loaded_data.plot(ax=ax1, x='kx', y='ky')
    ax1.plot(kp1x, kp1y, c='black')
    ax1.plot(kp2x, kp2y, c='black')
    ax1.scatter(kc1x, kc1y, c='black', s=50)
    ax1.scatter(kc2x, kc2y, c='black', s=50)
    ax1.axis('equal')

    ax2= plt.subplot(132, projection='polar')
    ax2.set_theta_offset(np.pi/2)
    ax2.pcolormesh(transform1.coords['phi'].values, np.degrees(transform1.coords['theta'].values), transform1.values, shading='auto')
    
    ax3= plt.subplot(133, projection='polar')
    ax3.set_theta_offset(np.pi/2)
    ax3.pcolormesh(transform2.coords['phi'].values, np.degrees(transform2.coords['theta'].values), transform2.values, shading='auto')

    my_stream = io.BytesIO()
    plt.savefig(my_stream, format="PNG")

    #Create a JS File object with our data and the proper mime type
    image_filename = '{}_pydpe_image_file.png'.format(random.getrandbits(128))
    image_file = File.new([Uint8Array.new(my_stream.getvalue())], image_filename, {type: "image/png"})

    #Create new tag and insert into page
    new_image = document.createElement('img')
    new_image.src = window.URL.createObjectURL(image_file)
    document.getElementById("graph-area").appendChild(new_image)

    #Create download button
    dbtn = document.createElement('a')
    dbtn.classList.add("reference","download","internal")
    dbtn.href = new_image.src
    dbtn.download = image_filename
    dbtn.innerHTML = 'Download Figure'
    document.getElementById("graph-area").appendChild(dbtn)

    return None

