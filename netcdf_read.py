import matplotlib
# Force plot to not default to Xwindow, otherwise it won't run through ssh
matplotlib.use('Agg')

import helpers
import os
import re
import xarray as xr
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import time

import sys 
#print(sys.path)

import ahrsl as ah
import eaeri as er

PARAMS = {"LOAD_DATA_FROM_SCRATCH": True, 
          "PLOT_DATA": False,
          "RUN_PROGRAM_FROM_SCRATCH": False,
          "LOAD_PREVIOUS_TAGS": True}


def find_next_avaliable(eaeri_data, day, month, year):
    for check in range(int(day)+1,33):
        check_next = year + month + str(check).rjust(2,'0')
        if check_next in eaeri_data:
            print("Now classifying: " + check_next)
            return check_next

        if check == 32:
            if not month == '12':
                return find_next_avaliable(eaeri_data, '00', str(int(month)+1).rjust(2,'0'), year)
            else:
                # If loaded more than one year into data, can run
                # return find_next_avaliable(eaeri_data, 0, 0, str(int(year)+1).rjust(2,'0') ) instead
                return "NULL"

# Revelant headers for determining cloudiness and cloud phases
keep_revelant = ['radar_backscattercrosssection', 'radar_dopplervelocity','linear_depol']
#ahsrl_dataframes = helpers.read_LIDAR_netcdf([2009], keep_revelant)


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

eaeri_dataframes = helpers.read_eaeri(["2009"])

if PARAMS['LOAD_PREVIOUS_TAGS']:
    Xfeatures = helpers.read_obj("features_2")
    Xtags = helpers.read_obj("tags_2")
else:
    Xfeatures, Xtags = [], []


#for header in keep_revelant:
 #   print(header)
    #unique = reformatted[header].nunique()
    #print(header + ' has ' + str(unique) + ' unique elments')000



#Find intersection of days both eaeri and lidar have measurements recorded
#intersect = set(ahsrl_dataframes).intersection(set(eaeri_dataframes))
ahsrl, eaeri = {},{}

# Keep intersection only for ahrsl data, since lidar data only useful with corresponding aeri data
# for days in intersect:
#     ahsrl[days] = ah.Ahrsl(ahsrl_dataframes[days])


for days in eaeri_dataframes:
    print(days)
    eaeri[days] = er.EAERI(eaeri_dataframes[days])

user_select = []

#all_eaeri_days = list(eaeri)
#all_eaeri_days_seconds = [time.gmtime(x) for x in all_eaeri_days]

while True:
    inp = input("Enter a classified day (ee to finish|spectra to see day spectra) [YYMMDD]: ")
    # Sample 2008-11-13 07:14:43 == Thick
    if inp == "ee":
        break

    elif inp == "spectra":
        inp2 = input("Enter day of spectra (YYMMDD)")

        print(eaeri[inp2].data['time_offset'].unique())
        continue

    while True:
        time_check = input("Enter time to classify (xx:xx:xx thin) (n to jump to next day): ")

        if time_check == 'n':
            day = inp[4:6]
            month = inp[2:4]
            year = inp[:2]
            # timestring = inp[4:6] + inp[2:4] + inp[:2]
            # struct_time = time.strptime(timestring, "%d %m %y") 

            # current_time = time.gmtime(struct_time)

            # closest_day = np.argmin(all_eaeri_days_seconds - current_time)
            
            next_avaliable_day = find_next_avaliable(eaeri, day, month, year)

            if next_avaliable_day != "NULL":
                inp = next_avaliable_day  
                continue
            else:
                print("Reached end of year - no more days to classify - exiting.")
                sys.exit()
            

        splitted = time_check.split(" ")

        timestamp = str(splitted[0])
        tag = splitted[1]


        #Split tag into classes: Thick -> 0; Thin -> 1; Clear -> 2
        if tag == "thick":
            tag = 0
        elif tag == "thin":
            tag = 1
        elif tag == "clear":
            tag = 2

        # Will pick the closest time to this with a spectra recorded
        try:
            time = eaeri[inp].find_closest_spectra(timestamp)

        except KeyError:
            print("No spectra recorded for specified date")
            continue

        kep = input("The closest recorded spectra found was (Keep[y/n]): " + str(time))
        if kep == 'y':
            BT_features = eaeri[inp].retrieve_microwindow_averages(time)

            extracted_features = er.EAERI.retrieve_microwindow_differences(BT_features)
            
            ft = np.array(extracted_features).T
            Xfeatures = np.append(Xfeatures, ft, axis=0)
            #print(np.shape(extracted_features))
            #print(np.shape(Xfeatures))
#            Xfeatures = np.append([Xfeatures,[])
 #           for window in extracted_features:
 #               Xfeatures[-1].append(window[1])
            Xtags = np.append(Xtags, [tag])
            #Xtags.append(tag)
        else:
            continue

        helpers.save_obj(Xfeatures, "features_2")
        helpers.save_obj(Xtags, "tags_2")



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

