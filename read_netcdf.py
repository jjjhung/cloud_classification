import matplotlib
# Force plot to not default to Xwindow, otherwise it won't run through ssh
matplotlib.use('Agg')
    
import os
import re
import time
import helpers
import copy
import xarray as xr
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

def read_files(year):
    '''
    Reads files and does some visualization
    '''
    C1_dataframes = []

    if PARAMS['LOAD_DATA_FROM_SCRATCH']:
        C1_dataframes = load_files(year)
        helpers.save_obj(C1_dataframes, 'C1_dataframes_' + str(year))

    else:
        C1_dataframes = helpers.read_obj('C1_dataframes_' + str(year))


    cloudy_counts = {"Clear": 0, "Thin": 0, "Thick": 0}

    brightness_template = {"All": [], "Clear": [], "Thin": [], "Thick": []}

    um10_brightness_temps = {"W": copy.deepcopy(brightness_template), 
                             "F/S": copy.deepcopy(brightness_template),
                             "S": copy.deepcopy(brightness_template)}

    um20_brightness_temps = {"W": copy.deepcopy(brightness_template), 
                             "F/S": copy.deepcopy(brightness_template),
                             "S": copy.deepcopy(brightness_template)}

    for ind,df in enumerate(C1_dataframes):
        print(ind)

        temp = df.reset_index()
        time_values = temp['time'].unique()
        g = temp.groupby(['time'])
        
        for timee in time_values:
            # Work with small dataframe for a particular AERI spectra timeslice
            small_series = g.get_group(timee)

            # Retrieve date and time info for spectra 
            date = str(small_series.iloc[0]['time_offset']).split(' ')  

            if PARAMS['PLOT_DATA']: 
                save_plot(date, year, small_series)
            
            truncated_850_950 = helpers.read_wavenumber_slice(small_series, (850,950))
            truncated_850_950.mean_rad = truncated_850_950.mean_rad / 1000


            # Classify scene as clear/thin/thick cloudy, and season of measurement
            cloudy, season = helpers.cloudify(date, truncated_850_950)

            # Wavenumbers truncated in the 10um range, can be plotted to visualize
            truncated_10um = helpers.read_wavenumber_slice(small_series, (985,998))
            truncated_20um = helpers.read_wavenumber_slice(small_series, (529.9, 532))
            #save_plot(date, year, truncated_10um)
            #save_plot(date, year, truncated_20um)

            #10um wavenumbers with brightness temperature calculations added as additional col
            truncated10um_brighttemp = avg_brightness_temp(truncated_10um)
            truncated20um_brighttemp = avg_brightness_temp(truncated_20um)


            try:
                holder = truncated10um_brighttemp['avg_brightness_temp'].mean()
                um10_brightness_temps[season]['All'] += [holder]
                um10_brightness_temps[season][cloudy] += [holder]

                #print('10um mean', holder)

                holder = truncated20um_brighttemp['avg_brightness_temp'].mean()
                um20_brightness_temps[season]['All'] += [holder]
                um20_brightness_temps[season][cloudy] += [holder]
            except e:
                print(e)
                printt(truncated19um_brighttemp)
            #print('20um mean', holder)

            cloudy_counts[cloudy] += 1

    print(year, cloudy_counts)

    total = cloudy_counts['Thin'] + cloudy_counts['Clear'] + cloudy_counts['Thick']
    print("Thin", cloudy_counts['Thin'] / total)
    print("Clear", cloudy_counts['Clear'] / total)
    print("Thick", cloudy_counts['Thick'] / total)

    return {'10um': um10_brightness_temps, '20um': um20_brightness_temps} 


if __name__ == '__main__':
    #years = [2008,2009,2011,2012,2013,2014]:
    years = [2008]

    brightness_template = {"All": [], "Clear": [], "Thin": [], "Thick": []}

    um10_counts = {"W": copy.deepcopy(brightness_template), 
                   "F/S": copy.deepcopy(brightness_template),
                   "S": copy.deepcopy(brightness_template)}
    um20_counts = {"W": copy.deepcopy(brightness_template), 
                   "F/S": copy.deepcopy(brightness_template),
                   "S": copy.deepcopy(brightness_template)}
    
    all_10um_counts = copy.deepcopy(brightness_template)
    all_20um_counts = copy.deepcopy(brightness_template)
    
    # Do a lot of plotting - histograms of brightness temperatures
    for year in years:
        counts = read_files(year)

        for season in ["W", "F/S", "S"]:
            season_sanitized = "FS" if season == "F/S" else season#Manually sanitize string to make it suitable for filename

            um10_counts[season]['All'] += counts['10um'][season]['All']
            um10_counts[season]['Clear'] += counts['10um'][season]['Clear']
            um10_counts[season]['Thin'] += counts['10um'][season]['Thin']
            um10_counts[season]['Thick'] += counts['10um'][season]['Thick']

            um20_counts[season]['All'] += counts['20um'][season]['All']
            um20_counts[season]['Clear'] += counts['20um'][season]['Clear']
            um20_counts[season]['Thin'] += counts['20um'][season]['Thin']
            um20_counts[season]['Thick'] += counts['20um'][season]['Thick']

            all_10um_counts['All'] += counts['10um'][season]['All']
            all_10um_counts['Clear'] += counts['10um'][season]['Clear']
            all_10um_counts['Thin'] += counts['10um'][season]['Thin']
            all_10um_counts['Thick'] += counts['10um'][season]['All']

            all_20um_counts['All'] += counts['20um'][season]['All']
            all_20um_counts['Clear'] += counts['20um'][season]['Clear']
            all_20um_counts['Thin'] += counts['20um'][season]['Thin']
            all_20um_counts['Thick'] += counts['20um'][season]['Thick']   

            # Some debugging helpers
            print("10 " + season + 'All' + str(um10_counts[season]['All']))
            print("10 " + season + 'Clear' + str(um10_counts[season]['Clear']))
            print("10 " + season + 'Thin' + str(um10_counts[season]['Thin']))
            print("10 " + season + 'Thick' + str(um10_counts[season]['Thick']))
            print("20 " + season + 'All' + str(um20_counts[season]['All']))
            print("20 " + season + 'Clear' + str(um20_counts[season]['Clear']))
            print("20 " + season + 'Thin' + str(um20_counts[season]['Thin']))
            print("20 " + season + 'Thick' + str(um20_counts[season]['Thick']))

            # Save some checkpoints in case the server disconnects
            helpers.save_obj(um10_counts[season]['All'], "um10_counts_" + season_sanitized + "_" + str(year) + "_All")
            helpers.save_obj(um10_counts[season]['Clear'], "um10_counts_" + season_sanitized + "_" + str(year) + "_Clear")
            helpers.save_obj(um10_counts[season]['Thin'], "um10_counts_" + season_sanitized + "_" + str(year) + "_Thin")
            helpers.save_obj(um10_counts[season]['Thick'], "um10_counts_" + season_sanitized + "_" + str(year) + "_Thick")
            helpers.save_obj(um20_counts[season]['All'], "um20_counts_" + season_sanitized + "_" + str(year) + "_All")
            helpers.save_obj(um20_counts[season]['Clear'], "um20_counts_" + season_sanitized + "_" + str(year) + "_Clear")
            helpers.save_obj(um20_counts[season]['Thin'], "um20_counts_" + season_sanitized + "_" + str(year) + "_Thin")
            helpers.save_obj(um20_counts[season]['Thick'], "um20_counts_" + season_sanitized + "_" + str(year) + "_Thick")
            
            helpers.save_obj(all_10um_counts['All'], "all_um10_counts_" + str(year) + "_All")
            helpers.save_obj(all_10um_counts['Clear'], "all_um10_counts_" + str(year) + "_Clear")
            helpers.save_obj(all_10um_counts['Thin'], "all_um10_counts_" + str(year) + "_Thin")
            helpers.save_obj(all_10um_counts['Thick'], "all_um10_counts_" + str(year) + "_Thick")
            helpers.save_obj(all_20um_counts['All'], "all_um20_counts_" + str(year) + "_All")
            helpers.save_obj(all_20um_counts['Clear'], "all_um20_coun_" + str(year) + "_Clear")
            helpers.save_obj(all_20um_counts['Thin'], "all_um20_counts_" + str(year) + "_Thin")
            helpers.save_obj(all_20um_counts['Thick'], "all_um20_counts_" + str(year) + "_Thick")

    # Plot seasonal graphs for both  10um and 20um slice_range
    # Only plot for nonempty results
    for season in ["W", "F/S", "S"]:
        
        season_sanitized = "FS" if season == "F/S" else season #Manually sanitize string to make it suitable for filename
        helpers.histogram_plot(um10_counts[season]['All'], './seasonal_plots/10um/' + season_sanitized + '_all')
        helpers.histogram_plot(um10_counts[season]['Clear'], './seasonal_plots/10um/' + season_sanitized + '_clear')
        helpers.histogram_plot(um10_counts[season]['Thin'], './seasonal_plots/10um/' + season_sanitized + '_thin')
        helpers.histogram_plot(um10_counts[season]['Thick'], './seasonal_plots/10um/' + season_sanitized + '_thick')

        helpers.histogram_plot(um20_counts[season]['All'], './seasonal_plots/20um/' + season_sanitized + '_all')
        helpers.histogram_plot(um20_counts[season]['Clear'], './seasonal_plots/20um/' + season_sanitized + '_clear')
        helpers.histogram_plot(um20_counts[season]['Thin'], './seasonal_plots/20um/' + season_sanitized + '_thin')
        helpers.histogram_plot(um20_counts[season]['Thick'], './seasonal_plots/20um/' + season_sanitized + '_thick')


    # Plot overall pattern, without seasonal dependence
    helpers.histogram_plot(all_10um_counts['All'], './non_seasonal_plots/10um/all')
    helpers.histogram_plot(all_10um_counts['Clear'], './non_seasonal_plots/10um/clear')
    helpers.histogram_plot(all_10um_counts['Thin'], './non_seasonal_plots/10um/all')
    helpers.histogram_plot(all_10um_counts['Thick'], './non_seasonal_plots/10um/Thick')

    helpers.histogram_plot(all_20um_counts['All'], './non_seasonal_plots/20um/all')
    helpers.histogram_plot(all_20um_counts['Clear'], './non_seasonal_plots/20um/Clear')
    helpers.histogram_plot(all_20um_counts['Thin'], './non_seasonal_plots/20um/Thin')
    helpers.histogram_plot(all_20um_counts['Thick'], './non_seasonal_plots/20um/Thick')





'''
RESULTS FROM MEAN RADIANCE

2008 {'Thick': 1692, 'Clear': 1728, 'Thin': 2123}
Thin 0.38300559263936496
Clear 0.31174454266642615
Thick 0.3052498646942089

2009 {'Thick': 18624, 'Clear': 5188, 'Thin': 2442}
Thin 0.0930143978060486
Clear 0.19760798354536452
Thick 0.7093776186485868

2011 {'Thick': 7812, 'Clear': 5546, 'Thin': 3833}
Thin 0.22296550520621256
Clear 0.32261066837298585
Thick 0.4544238264208016

2012 {'Thick': 24644, 'Clear': 9427, 'Thin': 10395}
Thin 0.23377411955201727
Clear 0.21200467773130033
Thick 0.5542212027166824

2013 {'Thick': 19579, 'Clear': 11503, 'Thin': 8386}
Thin 0.2124759298672342
Clear 0.2914513023208675
Thick 0.49607276781189824

2014 {'Thin': 12968, 'Clear': 10331, 'Thick': 19599}
Thin 0.3022984754534011
Clear 0.2408270781854632
Thick 0.4568744463611357

'''