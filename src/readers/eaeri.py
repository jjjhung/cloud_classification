import re
import xarray as xr
import pandas as pd
import os


def read_eaeri(years):
    '''
    Loads C1 datafiles for the provided year into a pandas dataframe

    Only loads files with date.C1 and date.C2 files available. 

        Params
        ==============
        - years: list[int] of years to retrieve 

        Returns
        ==============
            Dict of Pandas dataframe

    '''
    
    dataframes = {}

    for year in years:
        #prepended_dir = '/home/jhung/CDFs/' + str(year)
        prepended_dir = '/home/joseph/Documents/Atmosp/Ice/data/eaeri/' + str(year)
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
