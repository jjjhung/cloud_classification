import scipy as sp
import numpy as np
import pandas as pd
import pickle
import time
import os
import re
import copy
import xarray as xr
import seaborn as sns
import matplotlib.pyplot as plt

from scipy import constants
from pathlib import Path

def brightness_temp(radiance, wnum):
    '''
    Returns the brightness temperature given the radiance (radiance) and wavenumber of measured light
    radiance is mW/m^2 * sr * cm
    Wavenumber is 1/cm

    Limit brightness temperature to [0,1000]

    '''
    wavenum = wnum * 100 # Convert wavenumber to 1/m
    radiance /= 1000 # Convert mW to W
    radiance *= -0.01001

    #radiance /= (2*constants.pi**2)

    ln_elements = -2 * constants.Planck * (wavenum**3) * (constants.speed_of_light**2) / (radiance)
    #ln_elements += 1
    
    coeff = constants.Planck * constants.speed_of_light * wavenum / constants.Boltzmann 
    
    # Numerical stability - log1p(x) does log(x + 1) stably 
    divid = coeff / np.log1p(ln_elements)

    # Sometimes divid is complex, probably because conversion error from xarray -> dataframe?
    real = divid if not np.iscomplex(divid) else np.real(divid)  

    # Enforce boundary conditions
    real = 0 if real < 0 else real
    real = 1000 if real > 1000 else real

    return real

def coefficient_calculate(wavenum, temp, intensity):
    '''
    Calcutes the solid angle adjustment factor for converting the field of view in radians
    to the steradians given in the provided radiances
    '''

    expon = constants.Planck * constants.speed_of_light * wavenum / (temp * constants.Boltzmann)
    expon = np.exp(expon)
    expon = 1 - expon

    expon = 1/expon

    return expon * 2 * constants.Planck * constants.speed_of_light**2 * wavenum ** 3 / intensity


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

    C1_dataframes = []
    for file in os.listdir(prepended_dir):
        if re.search('[0-9]*C1.cdf', file): #This finds all the YYMMDDC1.cdf files
            C1_dataframes.append(xr.open_dataset(prepended_dir + '/' + file).to_dataframe())
        if re.search('^[0-9]*(?!C1|C2).cdf', file):  # Use negative lookahead to find YYMMDD.cdf files only
            pass 
        # if re.search('[0-9]*C2.cdf', file): #This finds all the C2 files
        #     C2_dataframes += [xr.open_dataset(prepended_dir + '/' + file).to_dataframe()]

    
    return C1_dataframes

def read_LIDAR_netcdf(years, columns_to_keep):
    '''
    Reads in nc files from LIDAR (ahrsl) data
    Returns a dictionary of dataframes with revelant columns (backscatter coefficient
        and depolarization ratios), used for determining cloudiness and cloud phase
        of the form dict[date] = dataframe
    

    Params 
    =============
    - years : Selected years to read in 
    - columns_to_keep : List[String] of datacolumns to keep
    '''
    dataframes = {}

    for year in years:
        prepended_dir = str(year)

        for file in os.listdir(prepended_dir):
            if Path('./' + file).suffix == '.nc': # Only read nc filename
                xar = xr.open_dataset(prepended_dir + '/' + file)

                date = Path(file).stem
                print(date)
                dataframes[date] = xar[columns_to_keep].to_dataframe()

    return dataframes

def read_eaeri(years):
    '''
    Reads in the C1 datafiles from E-AERI data
    Returns a dictionary of dataframes with only the mean_rad data, and some datetime metadata
        of the form dict[date] = (dataframe for that day)_

    '''
    
    dataframes = {}

    for year in years:
        prepended_dir = str(year)

        for file in os.listdir(prepended_dir):
            if re.search('^[0-9]*(?!C1|C2).cdf', file):
                date = str(str(file[:6]))
                C1_filename = date + "C1.cdf"

                eaeri_c1 = xr.open_dataset(prepended_dir + '/' + C1_filename)
                rad = eaeri_c1[['date','base_time','time_offset','mean_rad']]

                pandified = rad.to_dataframe()
                pandified['base_time'] = pd.to_datetime(pandified['base_time'])

                dataframes[date] = pandified

    return dataframes                


def print_full(df):
    '''
    Prints dataframe, displays all data

    '''
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(df)


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
 
def histogram_plot(data, save_path, color, save, legend):

    if data == []:
        return 
    sns.distplot(data, kde=False, hist_kws={"histtype":"step", "color": color, "label": legend})

    if save:
        plt.legend()
        plt.savefig(save_path)
        plt.clf()


def plot(df, axis_x, axis_y, save_path):
    '''
    Plots a particular dataframe with given x and y axes
    Saves plotted figure to provided path
    '''

    sns.lineplot(axis_x, axis_y,data=df)
    plt.savefig(save_path)
    plt.clf()



def save_plot(date, year, data):
    '''
    Wrapper for plotting function - checks if appropriate organizing folders exist and 
        plot radiance against wavenumber

        Saves plots in ./[year]_plots/[date]
    '''
    path_save = './' + str(year) + '_plots/' + date[0] + '/' + date[1]
    helpers.create_dir('./' + str(year) + '_plots/' + date[0])
    plot(data, 'wnum1', 'mean_rad', path_save)


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

