'''Script to load ndacc trace gas retrivals

'''

import matplotlib
# Force plot to not default to Xwindow, otherwise it won't run through ssh
matplotlib.use('Agg')

import pickle
import scipy as sp
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import helpers
import hdfreader

from scipy.interpolate import interp1d

#Grid to interpolate to 
wacam_heights_a = open('./pickle/heightpickle.obj', 'rb')
wacam_heights = pickle.load(wacam_heights_a)
wacam_heights = np.append(wacam_heights[:-1],np.array([0])) * 1000 #Extend the bottom layer to 0km from 0.61km

# ================= O3 ====================
df_o3 = hdfreader.read_hdf('../ndacc','O3')
o3_retr_time =  hdfreader.find_closest_retrival(df_o3,"200309T7:15:00")
print("Closest O3 retrival", o3_retr_time)

o3_selected_retrival = df_o3.loc[o3_retr_time]['O3.MIXING.RATIO.VOLUME_ABSORPTION.SOLAR']
o3_altitude = df_o3.loc[o3_retr_time]['ALTITUDE']
o3_pressure = df_o3.loc[o3_retr_time]['PRESSURE_INDEPENDENT']
o3_temperature = df_o3.loc[o3_retr_time]['TEMPERATURE_INDEPENDENT']


#interp_o3_f = interp1d(o3_altitude,o3_selected_retrival,fill_value="extrapolate", kind="linear")
#interp_o3 = interp_o3_f(wacam_heights)

plt.plot(o3_selected_retrival, o3_altitude)
plt.savefig('o3_profile')

# ====================== N20 =====================
plt.clf()
df_n2o = hdfreader.read_hdf('../ndacc','N2O')
n2o_retr_time = hdfreader.find_closest_retrival(df_n2o,"200309T7:15:00")
print("Closest N2O retrival", n2o_retr_time)
n2o_selected_retrival = df_n2o.loc[n2o_retr_time]['N2O.MIXING.RATIO.VOLUME_ABSORPTION.SOLAR']
n2o_altitude = df_n2o.loc[n2o_retr_time]['ALTITUDE']
n2o_pressure = df_n2o.loc[n2o_retr_time]['PRESSURE_INDEPENDENT']
n2o_temperature = df_n2o.loc[n2o_retr_time]['TEMPERATURE_INDEPENDENT']
#print(n2o_selected_retrival)


plt.plot(n2o_selected_retrival, n2o_altitude)
plt.savefig('n2o_profile')


# ====================== CO ================
plt.clf()
df_co = hdfreader.read_hdf('../ndacc','CO')
co_retr_time = hdfreader.find_closest_retrival(df_co,"200309T7:15:00")
print("Closest CO retrival", co_retr_time)
co_selected_retrival = df_co.loc[co_retr_time]['CO.MIXING.RATIO.VOLUME_ABSORPTION.SOLAR']
co_altitude = df_co.loc[co_retr_time]['ALTITUDE']
co_pressure = df_co.loc[co_retr_time]['PRESSURE_INDEPENDENT']
co_temperature = df_co.loc[co_retr_time]['TEMPERATURE_INDEPENDENT']
plt.plot(co_selected_retrival, co_altitude)
plt.savefig('co_profile')
#===================== CH4 ===================

plt.clf()
df_ch4 = hdfreader.read_hdf('../ndacc','CH4')
ch4_retr_time = hdfreader.find_closest_retrival(df_ch4,"200309T7:15:00")
print("Closest CH4 retrival", ch4_retr_time)
ch4_selected_retrival = df_ch4.loc[ch4_retr_time]['CH4.MIXING.RATIO.VOLUME_ABSORPTION.SOLAR']
ch4_altitude = df_ch4.loc[ch4_retr_time]['ALTITUDE']
ch4_pressure = df_ch4.loc[ch4_retr_time]['PRESSURE_INDEPENDENT']
ch4_temperature = df_ch4.loc[ch4_retr_time]['TEMPERATURE_INDEPENDENT']

#print(ch4_selected_retrival)
plt.plot(ch4_selected_retrival, ch4_altitude)
plt.savefig('ch4_profile')



# df_o2 = hdfreader.read_hdf('.','O2')
# o2_retr_time = find_closest_retrival(df_o2,"200309T7:15:00")
# print("Closest O2 retrival", o2_retr_time)
# o2_selected_retrival = df_o2.loc[o2_retr_time]
# print(o2_selected_retrival)

plt.clf()
plt.plot(o3_pressure, o3_altitude, label='o3')
plt.plot(n2o_pressure, n2o_altitude, label='n2o')
plt.plot(co_pressure, co_altitude, label='co')
plt.plot(ch4_pressure, ch4_altitude, label='ch4')
plt.legend()
plt.savefig('pressure')


# h2o contribution factor to spectrum I think, not useful
# plt.clf()
# o3_h2o = df_o3.loc[o3_retr_time]['H2O.MIXING.RATIO.VOLUME_ABSORPTION.SOLAR']
# n2o_h2o = df_n2o.loc[n2o_retr_time]['H2O.MIXING.RATIO.VOLUME_ABSORPTION.SOLAR']
# co_h2o = df_co.loc[co_retr_time]['H2O.MIXING.RATIO.VOLUME_ABSORPTION.SOLAR']
# ch4_h2o = df_ch4.loc[ch4_retr_time]['H2O.MIXING.RATIO.VOLUME_ABSORPTION.SOLAR']

plt.plot(o3_temperature, o3_altitude, label='o3')
plt.plot(n2o_temperature, n2o_altitude, label='n2o')
plt.plot(co_temperature, co_altitude, label='co')
plt.plot(ch4_temperature, ch4_altitude, label='ch4')
plt.legend()
plt.savefig('temperature')


# ======= SAVE THINGS ==========
helpers.save_obj(o3_selected_retrival[::-1], "o3_RETRIVAL")
helpers.save_obj(n2o_selected_retrival[::-1], "n2o_RETRIVAL")
helpers.save_obj(co_selected_retrival[::-1], "co_RETRIVAL")
helpers.save_obj(ch4_selected_retrival[::-1], "ch4_RETRIVAL")

helpers.save_obj(o3_pressure[::-1], "pressure_RETRIVAL")
helpers.save_obj(o3_temperature[::-1], "temperature_RETRIVAL")
helpers.save_obj(o3_altitude[::-1], "altitude_RETRIVAL")
