import matplotlib
# Force plot to not default to Xwindow, otherwise it won't run through ssh
matplotlib.use('Agg')

import helpers
import pandas as pd
import seaborn as sns
import numpy as numpy
import matplotlib.pyplot as plt

keep = ['radar_backscattercrosssection','radar_backscattercrosssection','radar_reflectivity',
'radar_spectralwidth','radar_dopplervelocity','beta_a','atten_beta_a_backscat',
'circular_depol','linear_depol','profile_circular_depol','profile_linear_depol',
'beta_a_backscat_parallel','profile_beta_a_backscat_parallel','beta_a_backscat_perpendicular'
,'profile_beta_a_backscat_perpendicular','beta_a_backscat','profile_beta_a_backscat']

dataframes = helpers.read_netcdf('ahsrl_20090204T1200_20090205T0000_300s_22.5m.nc', keep)

#with pd.option_context('display.max_rows', None, 'display.max_columns', None):
	#print(dataframes)

#dataframes = dataframes.reset_index()
#print(pd.MultiIndex.from_frame(dataframes).names)
print(dataframes.loc[(4545.0,0,'2009-02-04 12:00:00')])
#print(dataframes.columns.values)
#plt.imshow(dataframes['radar_dopplervelocity'])
#plt.show()

