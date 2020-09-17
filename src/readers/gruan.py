'''
	Module for code to read Eureka Radiosonde profiles into pandas dataframes
	
	Also contains additional helper functions related to gruan operations
'''


import os
import xarray as xr
import seaborn as sns
import pickle
import numpy as np
import pandas as pd


def load_gruan_by_year(year):
    '''
    Loads GRUAN datafiles for the provided year into a pandas dataframe
        Params
        ==============
        - year: int of year to retrieve 

        Returns
        ==============
            List of Pandas dataframe

    '''

    #prepended_dir = '../' + str(year)  # For running on the server
    #prepended_dir = '/net/aurora/ground/eureka/radiosondes/GRUAN/' + str(year)
    prepended_dir = './GRUAN/' + str(year)
    
    dataframes = []
    for file in os.listdir(prepended_dir):

        dataframes.append(xr.open_dataset(prepended_dir + '/' + file).to_dataframe())
    
    return dataframes

def load_gruan_by_date(fname):
    '''
    Loads GRUAN datafiles for the provided date into a pandas dataframe

        Params
        ==============
        - datetime: datetime to retrive radiosonde profile for 

        Returns
        ==============
            Pandas dataframe

    '''

    return xr.open_dataset(fname).to_dataframe()

