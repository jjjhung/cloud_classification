'''
    This file is for visualizing a single datafile. For testing purposes. 
'''
import matplotlib
# Force plot to not default to Xwindow, otherwise it won't run through ssh
matplotlib.use('Agg')
import os
import re
import time
import helpers
import xarray as xr
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(style="darkgrid")

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
    '''
    path_save = './' + str(year) + '_plots/' + date[0] + '/' + date[1]

    if not os.path.exists('./' + str(year) + '_plots/' + date[0]):
        os.makedirs('./' + str(year) + '_plots/' + date[0])
    
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

    print(rad)
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
        return winter_radiances(rad_mean)
    elif season == 'F/S': #Fall / Spring
        return fallspr_radiances(rad_mean)
    elif season == 'S': #Summer
        return summer_radiances(rad_mean)




def histogram_plot(data, save_path):

    if data == []:
        return 
    sns.distplot(data, kde=False, rug=True)
    plt.savefig(save_path)
    plt.clf()



#df = xr.open_dataset('./2008/081020C1.cdf').to_dataframe()
C1_dataframes = helpers.read_obj('C1_dataframes_2008')

tally = []
for ind,df in enumerate(C1_dataframes):
    print(ind)

    temp = df.reset_index()
    time_values = temp['time'].unique()
    g = temp.groupby(['time'])

    for timee in time_values:
        small_series = g.get_group(timee)
        #print(small_series)
        title = str(small_series.iloc[0]['time_offset']).split(' ')
        date = str(small_series.iloc[0]['time_offset']).split(' ')

        #if not os.path.exists('./' + str('2008') + '_plots/' + title[0]):
        #   os.makedirs('./' + str('2008') + '_plots/' + title[0])

        path_save = './' + str('2008') + '_plots/' + title[0] + '/' + title[1]

        #print(path_save)

        #plot(small_series, 'wnum1', 'mean_rad', path_save)
        #truncated_10um = read_wavenumber_slice(small_series, (985,998))
        #plot(truncated_10um, 'wnum1', 'mean_rad', path_save + '_truncated')

        truncated_10um = read_wavenumber_slice(small_series, (985,998))
        truncated10um_brighttemp = avg_brightness_temp(truncated_10um)

        '''
        truncated_850_950 = read_wavenumber_slice(small_series, (850,950))
        #print(truncated_850_950)
        truncated_850_950['mean_rad'] = truncated_850_950['mean_rad'] / 1000

        #save_plot(date, "2008-new", truncated_850_950)

        truncated_850_950_clouded = cloudify(date, truncated_850_950)
        print(timee, truncated_850_950_clouded)
        '''
        #truncated10um_brighttemp = avg_brightness_temp(truncated_10um)

        #print(truncated10um_brighttemp)
        print(truncated10um_brighttemp['avg_brightness_temp'].mean())
        tally += [truncated10um_brighttemp['avg_brightness_temp'].mean()]

histogram_plot(tally, "2008 sample stuff")




