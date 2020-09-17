import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from readers import lbldis 


'''
Some tests for plotting and determining cloud phases

'''

folders = ['simulations/water/', 'simulations/ice/', 'simulations/mixed/']
output_file_dir = '../../Models/lbldis/out/'


data_clr_sky = {}
data_blackbody = {}

#Calculated downwelling radiances for various cloud phases and particle shapes
data_cld = {'wat2um' : {}, 'wat3um' : {},'wat5um' : {},'wat7um' : {},'wat10um' : {},'wat15um' : {},
            'ice10um' : {}, 'ice20um' : {}, 'ice30um' : {}, 'ice50um' : {}, 'ice70um' : {}, 'ice100um' : {},
            'mixed_wat3_ice20' : {}, 'mixed_wat_3ice_30' : {}, 'mixed_wat_5ice_30' : {}, 'mixed_wat_7ice_20' : {}, 
                    'mixed_wat_7ice_30' : {}, 'mixed_wat_10ice_40' : {}}


for file in os.listdir(output_file_dir + "clear_sky/"):
    data_clr_sky[file[10:]] = lbldis.read_lbldis(output_file_dir + "clear_sky/" + file, 2)
for file in os.listdir(output_file_dir + "blackbody_clouds/"):
    data_blackbody[file[14:]] = lbldis.read_lbldis(output_file_dir + "blackbody_clouds/" + file, 2)

# print(list(data_clr_sky))

#Read simulated cloud optical depths
for file in os.listdir(output_file_dir + 'simulations/water/'):
    file_vals = file.split("_")
    if file_vals[2] == '2':
        data_cld['wat2um']["_".join(file_vals[-2:])] = lbldis.read_lbldis(output_file_dir + 'simulations/water/' + file, 17)
    if file_vals[2] == '3':
        data_cld['wat3um']["_".join(file_vals[-2:])] = lbldis.read_lbldis(output_file_dir + 'simulations/water/' + file, 17)
    if file_vals[2] == '5':
        data_cld['wat5um']["_".join(file_vals[-2:])] = lbldis.read_lbldis(output_file_dir + 'simulations/water/' + file, 17)
    if file_vals[2] == '7':
        data_cld['wat7um']["_".join(file_vals[-2:])] = lbldis.read_lbldis(output_file_dir + 'simulations/water/' + file, 17)
    if file_vals[2] == '10':
        data_cld['wat10um']["_".join(file_vals[-2:])] = lbldis.read_lbldis(output_file_dir + 'simulations/water/' + file, 17)
    if file_vals[2] == '15':
        data_cld['wat15um']["_".join(file_vals[-2:])] = lbldis.read_lbldis(output_file_dir + 'simulations/water/' + file, 17)

for file in os.listdir(output_file_dir + 'simulations/ice/'):
    file_vals = file.split("_")
    if file_vals[2] == '10':
        data_cld['ice10um']["_".join(file_vals[-2:])] = lbldis.read_lbldis(output_file_dir + 'simulations/ice/' + file, 17)
    if file_vals[2] == '20':
        data_cld['ice20um']["_".join(file_vals[-2:])] = lbldis.read_lbldis(output_file_dir + 'simulations/ice/' + file, 17)
    if file_vals[2] == '30':
        data_cld['ice30um']["_".join(file_vals[-2:])] = lbldis.read_lbldis(output_file_dir + 'simulations/ice/' + file, 17)
    if file_vals[2] == '50':
        data_cld['ice50um']["_".join(file_vals[-2:])] = lbldis.read_lbldis(output_file_dir + 'simulations/ice/' + file, 17)
    if file_vals[2] == '70':
        data_cld['ice70um']["_".join(file_vals[-2:])] = lbldis.read_lbldis(output_file_dir + 'simulations/ice/' + file, 17)
    if file_vals[2] == '100':
        data_cld['ice100um']["_".join(file_vals[-2:])] = lbldis.read_lbldis(output_file_dir + 'simulations/ice/' + file, 17)

# for file in os.listdir(output_file_dir + 'simulations/mixed/'):
#     file_vals = file.split("_")
#     if file_vals[1] == '3' and file_vals[3] == '20':
#         data_cld['mixed_wat3_ice20']["_".join(file_vals[-2:])] = lbldis.read_lbldis(output_file_dir + 'simulations/mixed/' + file, 17)
#     if file_vals[1] == '3' and file_vals[3] == '30':
#         data_cld['mixed_wat_3ice_30']["_".join(file_vals[-2:])] = lbldis.read_lbldis(output_file_dir + 'simulations/mixed/' + file, 17)
#     if file_vals[1] == '5' and file_vals[3] == '30':
#         data_cld['mixed_wat_5ice_30']["_".join(file_vals[-2:])] = lbldis.read_lbldis(output_file_dir + 'simulations/mixed/' + file, 17)
#     if file_vals[1] == '7' and file_vals[3] == '20':
#         data_cld['mixed_wat_7ice_20']["_".join(file_vals[-2:])] = lbldis.read_lbldis(output_file_dir + 'simulations/mixed/' + file, 17)
#     if file_vals[1] == '7' and file_vals[3] == '30':
#         data_cld['mixed_wat_7ice_30']["_".join(file_vals[-2:])] = lbldis.read_lbldis(output_file_dir + 'simulations/mixed/' + file, 17)
#     if file_vals[1] == '10' and file_vals[3] == '40':
#         data_cld['mixed_wat_10ice_40']["_".join(file_vals[-2:])] = lbldis.read_lbldis(output_file_dir + 'simulations/mixed/' + file, 17)

microwindows = ["495.5_498", "529.9_531.5", "558.5_562", "830_834.5", "843_847.5", "873.2_875.5", "898.5_904.7", "1095_1098.2", "1113.5_1116.1", "1231.3_1232.2"]

emissivities = {'wat7um': {}, 'ice10um': {}, 'wat10um': {}, 'ice20um': {}, 'wat5um':{}, 'ice30um':{}} 

for cloud_spec in emissivities:
    for window in microwindows:
        emissivities[cloud_spec][window] = {}
        emissivities[cloud_spec][window][0.2] = np.mean((data_cld[cloud_spec][window][:,2] - data_clr_sky[window][:,1] ) / (data_blackbody[window][:,1] - data_clr_sky[window][:,1]))
        emissivities[cloud_spec][window][0.5] = np.mean((data_cld[cloud_spec][window][:,5] - data_clr_sky[window][:,1] ) / (data_blackbody[window][:,1] - data_clr_sky[window][:,1]))
        emissivities[cloud_spec][window][1.0] = np.mean((data_cld[cloud_spec][window][:,9] - data_clr_sky[window][:,1] ) / (data_blackbody[window][:,1] - data_clr_sky[window][:,1]))
        emissivities[cloud_spec][window][3.0] = np.mean((data_cld[cloud_spec][window][:,13] - data_clr_sky[window][:,1] ) / (data_blackbody[window][:,1] - data_clr_sky[window][:,1]))
        emissivities[cloud_spec][window][8.0] = np.mean((data_cld[cloud_spec][window][:,16] - data_clr_sky[window][:,1] ) / (data_blackbody[window][:,1] - data_clr_sky[window][:,1]))

#Calculating the emissivity slope between 800, 900 wavenumbers is given by [6]-[3]
emissivity_slope = {'wat7um': {}, 'ice10um': {}, 'wat10um': {}, 'ice20um': {}, 'wat5um':{}, 'ice30um':{}} 

for cloud_spec in emissivity_slope:
    emissivity_slope[cloud_spec] = {}

    for opd in [0.2, 0.5, 1.0, 3.0, 8.0]:
        emissivity_slope[cloud_spec][opd] = (emissivities[cloud_spec][microwindows[6]][opd] - emissivities[cloud_spec][microwindows[3]][opd]) / 69.35 #Wavenumber difference

#Calculation of ratio of mean emissivity between 17-19um (558.5 - 562) to (529.9 - 531.5) and 11 - 12um
emissivity_ratio = {'wat7um': {}, 'ice10um': {}, 'wat10um': {}, 'ice20um': {}, 'wat5um':{}, 'ice30um':{}} 


for cloud_spec in emissivity_ratio:
    emissivity_ratio[cloud_spec] = {}
    for opd in [0.2, 0.5, 1.0, 3.0, 8.0]:
        emissivity_ratio[cloud_spec][opd] = np.mean((np.mean(emissivities[cloud_spec][microwindows[1]][opd]), np.mean(emissivities[cloud_spec][microwindows[2]][opd]))) / np.mean((np.mean(emissivities[cloud_spec][microwindows[3]][opd]), np.mean(emissivities[cloud_spec][microwindows[4]][opd]), 
                                                        np.mean(emissivities[cloud_spec][microwindows[5]][opd]),np.mean(emissivities[cloud_spec][microwindows[6]][opd])))


#Calculation of the emissivity difference between the mean emissivities of the 17-19um and 11-12um windows
emissivity_difference = {'wat7um': {}, 'ice10um': {}, 'wat10um': {}, 'ice20um': {}, 'wat5um':{}, 'ice30um':{}} 

for cloud_spec in emissivity_difference:
    emissivity_difference[cloud_spec] = {}
    for opd in [0.2, 0.5, 1.0, 3.0, 8.0]:
        emissivity_difference[cloud_spec][opd] = np.mean((np.mean(emissivities[cloud_spec][microwindows[1]][opd]), np.mean(emissivities[cloud_spec][microwindows[2]][opd]))) - np.mean((np.mean(emissivities[cloud_spec][microwindows[3]][opd]), np.mean(emissivities[cloud_spec][microwindows[4]][opd]), 
                                                        np.mean(emissivities[cloud_spec][microwindows[5]][opd]),np.mean(emissivities[cloud_spec][microwindows[6]][opd])))
        emissivity_difference[cloud_spec][opd] *= 10
        emissivity_difference[cloud_spec][opd] += 1

emis_900 = {'wat7um': [], 'ice10um': [], 'wat10um': [], 'ice20um': [], 'wat5um':[], 'ice30um':[]} 
for s in emissivities:
    for op in [0.2, 0.5, 1.0, 3.0, 8.0]:
        emis_900[s].append(emissivities[s]['898.5_904.7'][op])
    #print(emissivities[s]['898.5_904.7'])

#print(emis_900)
# Load the blackbody optical depth calculations
emis_slope = [[],[],[],[],[],[]] #Optical depths

for i,cloud_spec in enumerate(emissivity_slope):
    emis_slope[i].append(emissivity_slope[cloud_spec][0.2]*1e4)
    emis_slope[i].append(emissivity_slope[cloud_spec][0.5]*1e4)
    emis_slope[i].append(emissivity_slope[cloud_spec][1.0]*1e4)
    emis_slope[i].append(emissivity_slope[cloud_spec][3.0]*1e4)
    emis_slope[i].append(emissivity_slope[cloud_spec][8.0]*1e4)
    #plt.plot([0.2, 0.5, 1.0, 3.0, 8.0], emis_slope[i])
    plt.plot(emis_900[cloud_spec], emis_slope[i], label=cloud_spec)
    #plt.xscale('log')
    #plt.plot(emis_slope[i])
plt.title("Emissivity slope at 900cm-1 for various cloud phases and particle size")
plt.xlabel("Emissivity at 900cm-1")
plt.ylabel("Emissivity Slope (x1000)")
plt.legend()
plt.show()

emis_ratio = [[],[],[],[],[],[]] #Optical depths

for i,cloud_spec in enumerate(emissivity_ratio):
    emis_ratio[i].append(emissivity_ratio[cloud_spec][0.2])
    emis_ratio[i].append(emissivity_ratio[cloud_spec][0.5])
    emis_ratio[i].append(emissivity_ratio[cloud_spec][1.0])
    emis_ratio[i].append(emissivity_ratio[cloud_spec][3.0])
    emis_ratio[i].append(emissivity_ratio[cloud_spec][8.0])
    plt.plot(emis_900[cloud_spec], emis_ratio[i], label=cloud_spec)
    #plt.plot(emis_ratio[i])
plt.title("Emissivity ratio comparison (between 550cm-1 to 900cm-1)")
plt.xlabel("Emissivity at 900cm-1")
plt.ylabel("Emissivity Ratio")
plt.legend()
plt.show()

emis_difference = [[],[],[],[],[],[]] #Optical depths

for i,cloud_spec in enumerate(emissivity_difference):
    emis_difference[i].append(emissivity_difference[cloud_spec][0.2])
    emis_difference[i].append(emissivity_difference[cloud_spec][0.5])
    emis_difference[i].append(emissivity_difference[cloud_spec][1.0])
    emis_difference[i].append(emissivity_difference[cloud_spec][3.0])
    emis_difference[i].append(emissivity_difference[cloud_spec][8.0])
    plt.plot(emis_900[cloud_spec], emis_difference[i], label=cloud_spec)
    #plt.plot(emis_difference[i])

plt.title("Emissivity Difference comparison (between between 550cm-1 to 900cm-1)")
plt.xlabel("Emissivity at 900cm-1")
plt.ylabel("Emissivity Difference (*10 + 1)")
plt.legend()
plt.show()

