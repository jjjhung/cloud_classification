'''
    This file plots the differences in the calculated brightness temperatures and
        the recorded brightness temperatures in the cdf files
'''
import matplotlib
# Force plot to not default to Xwindow, otherwise it won't run through ssh
matplotlib.use('Agg')
import os
import re
import time
import helpers
import math
import copy
import pandas as pd
import xarray as xr
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(style="darkgrid")

PARAMS = {"LOAD_DATA_FROM_SCRATCH": False, 
          "PLOT_DATA": False}

def avg_brightness_temp(df):
    '''
    Calculates the average brightness temperature at 10um wavelength, 
        averaged over each 7 minute measurement period
        Adds the additional values as a new column titled 'avg_brightness_temp'
        Also classifies period as sunny or not, in new column titled 'sunny'

    '''
    temp_df = df
    temp_df['avg_brightness_temp'] = temp_df.apply(lambda row: helpers.brightness_temp(row.mean_rad, row.wnum1), axis=1)
    temp_df['sunny'] = temp_df.apply(lambda row: row.avg_brightness_temp > 225, axis=1)

    return temp_df


def histogram_plot(data, save_path):

    if data == []:
        return 
    sns.distplot(data, kde=False, rug=True)
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

def read_wavenumber_slice_set(df, slice_range):

    '''
    Returns a truncated dataframe with only datapoints contained within the provided wavenumber range
        Params
        ==============
        - df : Pandas dataframe
        - slice_range: 10 or 20um range

        Returns
        ==============
            Pandas dataframe
    '''
    #truncated = df.loc[(df['wnum11'] >= slice_range[0]) & (df['wnum11'] <= slice_range[1])]
    if slice_range == 10:
        return df.loc[np.abs(df['wnum11'] - 999.776897) < 0.05]
    elif slice_range == 20:
        return df.loc[np.abs(df['wnum11'] - 524.772602) < 0.05] 


def read_dataframes(years):
    xarrays, dataframes_C1, dataframes_cdf = [], {}, {}

    for year in years:
        if PARAMS['LOAD_DATA_FROM_SCRATCH']:
            #prepended_dir = '../' + str(year)
            prepended_dir = str(year)

            for file in os.listdir(prepended_dir):
                # Use negative lookahead to ignore C1/C2 files
                if re.search('^[0-9]*(?!C1|C2).cdf', file):
                    date = str(str(file[:6]))
                    C1_filename = date + "C1.cdf"

                    sample = xr.open_dataset(prepended_dir + '/' + file)
                    #dropped_sample = sample.drop_dims(['wnum2','wnum1','wnum3','wnum4','wnum12'])
                    #dropped_sample = sample.drop_dims(['wnum2'])

                    #print(sample)
                    skybrightness_temps = sample[['SkyBrightnessTempSpectralAveragesCh1','date','base_time']]
                    pandified = skybrightness_temps.to_dataframe()
                    
                    sample2 = xr.open_dataset(prepended_dir + "/" + C1_filename)
                    rad = sample2[['date','base_time','time_offset','mean_rad']]

                    pandified2 = rad.to_dataframe()
                    pandified['base_time'] = pd.to_datetime(pandified['base_time'])
                    pandified2['base_time'] = pd.to_datetime(pandified2['base_time'])

                    #print(type(pandified))
                    # if date in dataframes_C1:
                    #     dataframes_cdf[date] += [pandified]
                    #     dataframes_C1[date] += [pandified2]
                    # else:
                    dataframes_cdf[date] = pandified
                    dataframes_C1[date] = pandified2

            helpers.save_obj(dataframes_C1,"dataframes_C1_" + str(year))
            helpers.save_obj(dataframes_cdf,"dataframes_cdf_" + str(year))
    
        else:
            dataframes_C1 = helpers.read_obj("dataframes_C1_" + str(year))
            dataframes_cdf = helpers.read_obj("dataframes_cdf_" + str(year))

    return dataframes_C1, dataframes_cdf


if __name__ == '__main__':
    #years = [2008,2009,2011,2012,2013,2014]
    years = [2008]

    dataframes_C1, dataframes_cdf = read_dataframes(years)
    # print(dataframes[0]['base_time'])
    # print(C1_dataframes[0]['base_time'])

    cloudy_counts = {"Clear": 0, "Thin": 0, "Thick": 0}

    brightness_template = {"All": [], "Clear": [], "Thin": [], "Thick": []}

    um10_brightness_temps = {"W": copy.deepcopy(brightness_template), 
                             "F/S": copy.deepcopy(brightness_template),
                             "S": copy.deepcopy(brightness_template)}

    um20_brightness_temps = {"W": copy.deepcopy(brightness_template), 
                             "F/S": copy.deepcopy(brightness_template),
                             "S": copy.deepcopy(brightness_template)}

    all_10um_counts = copy.deepcopy(brightness_template)
    all_20um_counts = copy.deepcopy(brightness_template)

    # Each key in dataframes_cdf is a date - iterate through all of them and count revelant info
    for ind,df in enumerate(dataframes_cdf):
        
        print(ind)
        single_cdf_frame = dataframes_cdf[df]
        single_c1_frame = dataframes_C1[df]

        try:
            cdf_temp = single_cdf_frame.reset_index()
            c1_temp = single_c1_frame.reset_index()
        except:
            continue

        time_values = cdf_temp['time'].unique()

        cdf_grp = cdf_temp.groupby(['time'])
        c1_grp = single_c1_frame.groupby(['time'])

        differences10, differences20, calculated_10, calculated_20, cdf_10, cdf_20 = [], [], [], [], [] ,[]

        for timee in time_values:
            try:
                small_series_cdf = cdf_grp.get_group(timee)
                small_series_c1 = c1_grp.get_group(timee)

                small_series_c1 = small_series_c1.reset_index()
                small_series_cdf = small_series_cdf.reset_index()
            except:
                continue

            truncated_850_950 = helpers.read_wavenumber_slice(small_series_c1, (850,950))
            truncated_850_950.mean_rad = truncated_850_950.mean_rad / 1000
            # Get brightness temperature at 10um

            truncated_10um = helpers.read_wavenumber_slice(small_series_c1, (985,998))
            truncated_20um = helpers.read_wavenumber_slice(small_series_c1, (529.9, 532))
            
            truncated10um_brighttemp = avg_brightness_temp(truncated_10um)
            truncated20um_brighttemp = avg_brightness_temp(truncated_20um)

            brighttemp_10 = truncated10um_brighttemp['avg_brightness_temp'].mean()
            brighttemp_20 = truncated20um_brighttemp['avg_brightness_temp'].mean()

            intermediary10 = read_wavenumber_slice_set(small_series_cdf, 10)
            intermediary20 = read_wavenumber_slice_set(small_series_cdf, 20)

            date = str(small_series_c1.iloc[0]['time_offset']).split(' ')  
        
    #        cloudy, season = helpers.cloudify(date, truncated_850_950)


            try: # Retrieve cdf calculated brightness temperature, plot differences

                brightness_temps_10 = intermediary10.iloc[0]['SkyBrightnessTempSpectralAveragesCh1']
                brightness_temps_20 = intermediary20.iloc[0]['SkyBrightnessTempSpectralAveragesCh1']
                
                differences10.append(abs(brightness_temps_10 - brighttemp_10))
                differences20.append(abs(brightness_temps_20 - brighttemp_20))

                calculated_10.append(brighttemp_10)
                calculated_20.append(brighttemp_20)

                cdf_10.append(brightness_temps_10)
                cdf_20.append(brightness_temps_20)

            except:
                print(intermediary10.iloc[0]['SkyBrightnessTempSpectralAveragesCh1'])
                print(brightness_temps_20)
                print(differences10)
            
        helpers.create_dir('./difference_plots/10um')
        helpers.create_dir('./difference_plots/20um')

        helpers.save_obj(differences10, 'differences10')
        helpers.save_obj(differences20, 'differences20')
        helpers.save_obj(calculated_10, 'calculated_10')
        helpers.save_obj(calculated_20, 'calculated_20')
        helpers.save_obj(cdf_10, 'cdf_10')
        helpers.save_obj(cdf_20, 'cdf_20')

        sns.tsplot(data=differences10)
        plt.savefig('./difference_plots/10diff')
        plt.clf()

        # differences10 = [x for x in differences10 if not math.isnan(x)]
        # differences20 = [x for x in differences20 if not math.isnan(x)]
        # histogram_plot(differences10, "./difference_plots/10um/" + str(date))
        # histogram_plot(differences20, "./difference_plots/20um/" + str(date))

