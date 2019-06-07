import scipy as sp
import numpy as np
import pickle
import time
import os
import re
import copy
import xarray as xr
import seaborn as sns
import matplotlib.pyplot as plt

from scipy import constants

def brightness_temp(radiance, wnum):
    '''
    Returns the brightness temperature given the radiance (radiance) and wavenumber of measured light
    radiance is mW/m^2 * sr * cm
    Wavenumber is 1/cm

    Limit brightness temperature to [0,1000]

    '''
    wavenum = wnum * 100 # Convert wavenumber to 1/m

    # ln_elements = 2 * constants.Planck * (constants.speed_of_light ** 2)
    # ln_elements /= (radiance * (wavelength ** 5))
    # ln_elements += 1

    # coeff = (constants.Planck * constants.speed_of_light) / (constants.Boltzmann * wavelength)

    # divid = coeff / sp.log(ln_elements)

    ln_elements = -2 * constants.Planck * (wavenum**3) * (constants.speed_of_light**2) / (radiance/1000)
    ln_elements += 1
    
    coeff = constants.Planck * constants.speed_of_light * wavenum / constants.Boltzmann 
        
    divid = coeff / sp.log(ln_elements)

    # Sometimes divid is complex, probably because conversion error from xarray -> dataframe?
    real = divid if not np.iscomplex(divid) else np.real(divid)  

    # Enforce boundary conditions
    real = 0 if real < 0 else real
    real = 1000 if real > 1000 else real

    return real

    #divid = divid / (wavenum ** 2)
    # Times  1/wavenumber**2

    #Sometimes the result is complex..? I think this is because the source data is complex sometimes too
    #return divid if not np.iscomplex(divid) else np.real(divid)


def load_files(year):
    '''
    Loads C1/C1/cdf datafiles for the provided year into a pandas dataframe
        Params
        ==============
        - year: int of year to retrieve 

        Returns
        ==============
            List of Pandas dataframe

    '''

    #prepended_dir = '../' + str(year)  # For running on the server
    prepended_dir = str(year)

    C1_dataframes = [], []
    for file in os.listdir(prepended_dir):
        if re.search('[0-9]*C1.cdf', file): #This finds all the YYMMDDC1.cdf files
            C1_dataframes += [xr.open_dataset(prepended_dir + '/' + file).to_dataframe()]
        if re.search('^[0-9]*(?!C1|C2).cdf', file):  # Use negative lookahead to find YYMMDD.cdf files only
            pass 
        # if re.search('[0-9]*C2.cdf', file): #This finds all the C2 files
        #     C2_dataframes += [xr.open_dataset(prepended_dir + '/' + file).to_dataframe()]

    
    return C1_dataframes

def read_wavenumber_slice(df, slice_range):

    '''
    Returns a truncated dataframe with only datapoints contained within the provided wavenumber range
        Params
        ==============
        - df : Pandas dataframe
        - slice_range: tuple of wavenumber (low,high), inclusive

        Returns
        ==============
            Pandas dataframe
    '''
    truncated = df.loc[(df['wnum1'] >= slice_range[0]) & (df['wnum1'] <= slice_range[1])]

    return truncated


def create_dir(directory):
    '''
    Creates a directory if it does not already exist.
    
    '''

    if not os.path.exists(directory):
        os.makedirs(directory)

def save_obj(obj, name):
    '''
    Pickle an object to file
    Saves picked object in the ./pickle folder
    
    '''
    create_dir('pickle')
    file_handler = open('./pickle/' + name + '.obj', 'wb')
    pickle.dump(obj, file_handler)

def read_obj(name):
    '''
    Retrieves object from pickled file
    Returns object

    '''
    file_handler = open('./pickle/' + name + '.obj', 'rb')
    obj = pickle.load(file_handler)

    return obj
 
def histogram_plot(data, save_path):

    if data == []:
        return 
    sns.distplot(data, kde=False, rug=True)
    plt.savefig(save_path)
    plt.clf()



def det_season(date):
    month = int(date[0][5:7])

    if month >= 6 and month <= 8:
        season = "S"
    elif month == 5 or month == 9:
        season = "F/S"
    else:
        season = "W"

    return season

def winter_radiances(rad):
    #rad = rad / 1000

    #print(rad)
    if rad < 0.0015:
        return "Clear"
    elif rad <= 0.009:
        return "Thin"
    else:
        return "Thick"

def fallspr_radiances(rad):
    #rad = rad / 1000

    if rad < 0.007:
        return "Clear"
    elif rad <= 0.02:
        return "Thin"
    else:
        return "Thick"

def summer_radiances(rad):
    #radiance = rad / 1000

    if rad < 0.015:
        return "Clear"
    elif rad <= 0.045:
        return "Thin"
    else:
        return "Thick"

def cloudify(date, df):
    season = det_season(date)
    temp_df = df
    
    rad_mean = temp_df['mean_rad'].mean()

    if season == 'W': #Winter
        return winter_radiances(rad_mean), season
    elif season == 'F/S': #Fall / Spring
        return fallspr_radiances(rad_mean), season
    elif season == 'S': #Summer
        return summer_radiances(rad_mean), season
