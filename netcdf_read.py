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

import sys 
print(sys.path)

import ahrsl as ah
import eaeri as er

PARAMS = {"LOAD_DATA_FROM_SCRATCH": True, 
          "PLOT_DATA": False,
          "RUN_PROGRAM_FROM_SCRATCH": False}

# keep = ['radar_backscattercrosssection','radar_reflectivity',
# 'radar_spectralwidth','radar_dopplervelocity','beta_a',
# 'circular_depol','linear_depol','profile_circular_depol','profile_linear_depol',
# 'beta_a_backscat_parallel','profile_beta_a_backscat_parallel', 
# 'beta_a_backscat','profile_beta_a_backscat']

# Revelant headers for determining cloudiness and cloud phases
keep_revelant = ['radar_backscattercrosssection', 'radar_dopplervelocity','linear_depol']
ahsrl_dataframes = helpers.read_LIDAR_netcdf([2008], keep_revelant)


#dataframes = dataframes.reset_index()
#print(pd.MultiIndex.from_frame(dataframes).names)
#print(dataframes.loc[(4545.0,0,'2009-02-04 12:00:00')])
#print(dataframes.get_level_values(1))

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
eaeri_dataframes = helpers.read_eaeri(["2008"])

Xfeatures = []

for header in keep_revelant:
    print(header)
    #unique = reformatted[header].nunique()
    #print(header + ' has ' + str(unique) + ' unique elments')000



#Find intersection of days both eaeri and lidar have measurements recorded
intersect = set(ahsrl_dataframes).intersection(set(eaeri_dataframes))
ahsrl, eaeri = {},{}

# Keep intersection only for ahrsl data, since lidar data only useful with corresponding aeri data
# for days in intersect:
#     ahsrl[days] = ah.Ahrsl(ahsrl_dataframes[days])


for days in eaeri_dataframes:
    eaeri[days] = er.EAERI(eaeri_dataframes[days])

user_select = []
while True:
    inp = input("Enter a classified day (ee to finish) [YYYY-MM-DD HH:MM:SS == (thick|thin|clear)]: ")
    # Sample 2008-11-13 07:14:43 == Thick
    if inp == "ee":
        break

    splitted = inp.split(" == ")
    timestamp = splitted[0]
    tag = splitted[1]

    #Split tag into classes: Thick -> 0; Thin -> 1; Clear -> 2
    if tag == "thick":
        tag = 0
    elif tag == "thin":
        tag = 1
    elif tag == "clear":
        tag = 2

    # Will pick the closest time to this with a spectra recorded
    user_select.append((tag,timestamp)) 

for tag_pair in user_select:
    date = tag_pair[1][2:4] + tag_pair[1][5:7] + tag_pair[1][8:10]
    time = eaeri[date].find_closest_spectra(tag_pair[1])

    BT_features = eaeri[date].retrieve_microwindow_averages(time)

    extracted_features = er.EAERI.retrieve_microwindow_differences(BT_features)

    for window in extracted_features:
        print(window)
        
    Xfeatures.append()


#a = eaeri[days].retrieve_microwindow_averages("2008-11-13 00:08:15")
#b = er.EAERI.retrieve_microwindow_differences(a)




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
