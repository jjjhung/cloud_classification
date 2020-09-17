import matplotlib
# Force plot to not default to Xwindow, otherwise it won't run through ssh
#matplotlib.use('Agg')
import os
import re
import time
import helpers
import copy
import xarray as xr
import seaborn as sns
import pickle
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

'''
This file reads data from GRUAN radiosonde data -- Basic setup for interpolating
the water vapour profile
'''

data_single_2012 = helpers.load_gruan_by_year(2012)[0] #oct 17,2012
data_single_2013 = helpers.load_gruan_by_year(2013)[0] #This one has Dec 29, 2013
	
#Smaller dataframes indexed on time
heights_2012 = data_single_2012['alt']
wvmr_2012 = data_single_2012['WVMR']
pressure_2012 = data_single_2012['press']

heights_2013 = data_single_2013['alt']
wvmr_2013 = data_single_2013['WVMR']
pressure_2013 = data_single_2013['press']

#with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#print(data_single_2012[['alt','WVMR']])
#print(data_single_2013[['alt','WVMR']])
#print(list(data_single))
#print(wvmr)


#plt.plot(wvmr,heights)
#plt.savefig("height-wvmr")

wacam_heights_a = open('./Models/tape5_generator/PyLBLRTM/pylblrtm/profiles/pickle/heightpickle.obj', 'rb')
wacam_heights = pickle.load(wacam_heights_a)

wacam_heights = np.append(wacam_heights[:-1],np.array([0])) * 1000 #Extend the bottom layer to 0km from 0.61km
print(wacam_heights)
print(len(wvmr_2012))
interpolated_wvmr_f = interp1d(heights_2012, wvmr_2012,fill_value="extrapolate")
interpolated_wvmr = interpolated_wvmr_f(wacam_heights) * 1e6


interpolated_wvmr[:14] = np.zeros((14)) #Set high altitudes to 0 

print(wacam_heights)
print(interpolated_wvmr)

plt.plot(wvmr_2012,heights_2012,label='Original profile')
plt.plot(interpolated_wvmr, wacam_heights, label="Interpolated profile")
plt.title("Comparison of original vs interpolated wvmr profiles (Onto WACAM grid)")
plt.legend()
plt.savefig("Interpoalted_comparison")
#plt.show()

#Save this profile
file_handler = open('./Models/tape5_generator/PyLBLRTM/pylblrtm/profiles/pickle/H2Opickle.obj', 'wb')
pickle.dump(interpolated_wvmr,file_handler)
