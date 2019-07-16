import matplotlib
# Force plot to not default to Xwindow, otherwise it won't run through ssh
matplotlib.use('Agg')

import helpers
import os
import re
import xarray as xr
import pandas as pd
import seaborn as sns
import numpy as numpy
import matplotlib.pyplot as plt

PARAMS = {"LOAD_DATA_FROM_SCRATCH": True, 
          "PLOT_DATA": False,
          "RUN_PROGRAM_FROM_SCRATCH": False}

keep = ['radar_backscattercrosssection','radar_reflectivity',
'radar_spectralwidth','radar_dopplervelocity','beta_a',
'circular_depol','linear_depol','profile_circular_depol','profile_linear_depol',
'beta_a_backscat_parallel','profile_beta_a_backscat_parallel', 
'beta_a_backscat','profile_beta_a_backscat']

# Revelant headers for determining cloudiness and cloud phases
keep_revelant = ['radar_backscattercrosssection', 'radar_dopplervelocity','linear_depol']

dataframes = helpers.read_LIDAR_netcdf('ahsrl_20090202T0000_20090202T2300_60s_15m.nc', keep_revelant)

#dataframes = dataframes.reset_index()
#print(pd.MultiIndex.from_frame(dataframes).names)
print(dataframes.loc[(4545.0,0,'2009-02-04 12:00:00')])
print(dataframes.get_level_values(1))

#reformatted = dataframes.reset_index(level=['profile_time','altitude'])

#reformatted_delimited = reformatted[['altitude','profile_time','beta_a_backscat_parallel']]

#print(dataframes[['radar_dopplervelocity']])
'''
df2 = dataframes[['radar_dopplervelocity']].reset_index('profile_time', drop=True)

df2 = df2.reset_index().pivot_table(columns='profile_time',index='altitude',values='radar_dopplervelocity')
print(df2.columns.values)

sns.heatmap(df2)
plt.savefig('testradardoopppler')
plt.clf()
'''


# Plotting function for the profiles

aeri = helpers.read_eaeri(["2008"])
print(aeri)
for header in keep_revelant:
    print(header)
    #unique = reformatted[header].nunique()
    #print(header + ' has ' + str(unique) + ' unique elments')

    df2 = dataframes.reset_index().pivot_table(columns='time', index='altitude',values=header)
    df2 = df2[::-1] # Columns are in reverse order for some reason. 
    #df2 = dataframes['']
    #print(header)
    print(df2)
    sns.heatmap(df2)
    plt.savefig("./heatmaps/" + header + "_heatmap")
    plt.clf()




#helpers.print_full(reformatted)
#print(dataframes.loc[(4545.0,0,'2009-02-04 12:00:00')])
# I think all the values in index 1 are 0?? 


# dataframes_c1 are the corresponding recording times for the eaeri data
# particularly for the brightness temps calculations

#print(dataframes)
#with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    #print(dataframes.index.get_level_values(1))


#print(dataframes.columns.values)
#plt.imshow(dataframes['radar_dopplervelocity'])
#plt.show()


# Match based on datetime

#print(dataframes.index.get_level_values('time')) # This gets list of all time index values
#with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    #print(dataframes.iloc[dataframes.index.get_level_values('time') == '2009-02-04 12:00:00'])

#for single_time in c1 file:
