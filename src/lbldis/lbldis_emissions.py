import numpy as np
import seaborn as sns
import os
import matplotlib.pyplot as plt

output_file_dir = '../../Models/lbldis/out/'

data_clr_sky = {}
data_cld = {'wat7um': {}, 'ice21um': {}, 'wat10um': {}, 'ice18um': {}, 'wat5um':{}, 'ice26um':{}}
data_blackbody_cld = {}

def planck_wlen(temp, wnum):
    c1 = 1.191042e8
    c2 = 1.4387752e4

    denom = (wnum**5) * (np.exp(c2 / wnum / temp) - 1)

    return c1 / denom

def planck_wnum(temp, wnum):
    c1 = 1.191042e-5
    c2 = 1.4387752

    denom = np.exp(c2 * wnum / temp) - 1

    return c1 * wnum**3/ denom

for file in os.listdir(output_file_dir + "clear_sky/"):
    data_clr_sky[file[10:]] = np.genfromtxt(output_file_dir + "clear_sky/" + file, skip_header=2)

for file in os.listdir(output_file_dir + "water_7um/"):
    data_cld['wat7um'][file[14:]] = np.genfromtxt(output_file_dir + "water_7um/" + file, skip_header=2, usecols=(0,1,2,3,4,5))
for file in os.listdir(output_file_dir + "ice_21um/"):
    data_cld['ice21um'][file[13:]] = np.genfromtxt(output_file_dir + "ice_21um/" + file, skip_header=2, usecols=(0,1,2,3,4,5))
for file in os.listdir(output_file_dir + "water_10um/"):
    data_cld['wat10um'][file[15:]] = np.genfromtxt(output_file_dir + "water_10um/" + file, skip_header=2, usecols=(0,1,2,3,4,5))
for file in os.listdir(output_file_dir + "ice_18um/"):
    data_cld['ice18um'][file[13:]] = np.genfromtxt(output_file_dir + "ice_18um/" + file, skip_header=2, usecols=(0,1,2,3,4,5))
for file in os.listdir(output_file_dir + "water_5um/"):
    data_cld['wat5um'][file[14:]] = np.genfromtxt(output_file_dir + "water_5um/" + file, skip_header=2, usecols=(0,1,2,3,4,5))
for file in os.listdir(output_file_dir + "ice_26um/"):
    data_cld['ice26um'][file[13:]] = np.genfromtxt(output_file_dir + "ice_26um/" + file, skip_header=2, usecols=(0,1,2,3,4,5))

#print(list(data_cld['wat7um']))
#print(list(data_cld['wat10um']))
#print(list(data_cld['ice18um']))

for file in os.listdir(output_file_dir + "blackbody_clouds/"):
    data_blackbody_cld[file[14:]] = np.genfromtxt(output_file_dir + "blackbody_clouds/" + file, skip_header=2)

#Differences between modeled optical depths of clear sky and 7um water cloud
#Formatted as differences[microwindow][opt_depth]
differences_transmittances = {'wat7um': {}, 'ice21um': {}, 'wat10um': {}, 'ice18um': {}, 'wat5um':{}, 'ice26um':{}} 
differences_blackbody = {'wat7um': {}, 'ice21um': {}, 'wat10um': {}, 'ice18um': {}, 'wat5um':{}, 'ice26um':{}} 

microwindows = ["495.5_498", "529.9_531.5", "558.5_562", "830_834.5", "843_847.5", "873.2_875.5", "898.5_904.7", "1095_1098.2", "1113.5_1116.1", "1231.3_1232.2"]
microwindow_val = [496.75, 530.7, 560.25, 832.25, 845.25, 874.35, 901.6, 1096.6, 1114.8, 1231.75]
#microwindow_wlen = [20.13, 18.84, 17.85, 12.02, 11.83, 11.44, 11.09, 9.12, 8.97, 8.12]



# ----------- Read in transmittances from the lblrtm ------------------
transmittance_file = "../../Models/aer_lblrtm_v12.9_lnfl_v3.2/lblrtm_v12.9/TAPE28"

with open(transmittance_file,"r") as ff:
    content=ff.readlines()[28:]

content_holder = np.zeros((len(content),2))
for i,line in enumerate(content):
    content[i] = line.split('       ')
    content_holder[i][0] = float(content[i][0]) 
    content_holder[i][1] = float(content[i][1])

transmittances = []
for i,j in enumerate(microwindow_val):
    transmittances.append(content_holder[:,1][np.argmin(np.abs(content_holder[:,0] - microwindow_val[i]))])
    

#print(transmittances)
# ------------ Calculate the cloud emissivity --------------
for i,window in enumerate(data_clr_sky):
    print(window)
    rad = planck_wnum(250, microwindow_val[i])

    # Calculate Emissivity for various cloud specifications (wat/ice, different particle size) 
    for cloud_spec in differences_transmittances:
        differences_transmittances[cloud_spec][window] = {}
        differences_transmittances[cloud_spec][window][0.2] = np.mean(data_cld[cloud_spec][window][:,1] - data_clr_sky[window][:,1]) / rad / transmittances[i]
        differences_transmittances[cloud_spec][window][0.5] = np.mean(data_cld[cloud_spec][window][:,2] - data_clr_sky[window][:,1]) / rad / transmittances[i]
        differences_transmittances[cloud_spec][window][1.0] = np.mean(data_cld[cloud_spec][window][:,3] - data_clr_sky[window][:,1]) / rad / transmittances[i]
        differences_transmittances[cloud_spec][window][3.0] = np.mean(data_cld[cloud_spec][window][:,4] - data_clr_sky[window][:,1]) / rad / transmittances[i]
        differences_transmittances[cloud_spec][window][8.0] = np.mean(data_cld[cloud_spec][window][:,5] - data_clr_sky[window][:,1]) / rad / transmittances[i]  
        
        differences_blackbody[cloud_spec][window] = {}
        differences_blackbody[cloud_spec][window][0.2] = np.mean((data_cld[cloud_spec][window][:,1] - data_clr_sky[window][:,1] ) / (data_blackbody_cld[window][:,1] - data_clr_sky[window][:,1]))
        differences_blackbody[cloud_spec][window][0.5] = np.mean((data_cld[cloud_spec][window][:,2] - data_clr_sky[window][:,1] ) / (data_blackbody_cld[window][:,1] - data_clr_sky[window][:,1]))
        differences_blackbody[cloud_spec][window][1.0] = np.mean((data_cld[cloud_spec][window][:,3] - data_clr_sky[window][:,1] ) / (data_blackbody_cld[window][:,1] - data_clr_sky[window][:,1]))
        differences_blackbody[cloud_spec][window][3.0] = np.mean((data_cld[cloud_spec][window][:,4] - data_clr_sky[window][:,1] ) / (data_blackbody_cld[window][:,1] - data_clr_sky[window][:,1]))
        differences_blackbody[cloud_spec][window][8.0] = np.mean((data_cld[cloud_spec][window][:,5] - data_clr_sky[window][:,1] ) / (data_blackbody_cld[window][:,1] - data_clr_sky[window][:,1]))



opd02_trans,opd05_trans,opd1_trans,opd3_trans,opd8_trans = [],[],[],[],[] #Optical depth per window for transmittance calculation
opd02_bb,opd05_bb,opd1_bb,opd3_bb,opd8_bb = [],[],[],[],[] #Optical depth per window for blackbody cloud calculation

# Load the blackbody optical depth calculations
headers = ['wat7um', 'ice21um', 'wat10um', 'ice18um', 'wat5um', 'ice26um']
for ind,cloud_spec in enumerate(headers):
    opd02_bb,opd05_bb,opd1_bb,opd3_bb,opd8_bb = [],[],[],[],[] #Optical depth per window for blackbody cloud calculation
    for i,window in enumerate(microwindows):
        opd02_bb.append(differences_blackbody[cloud_spec][window][0.2])
        opd05_bb.append(differences_blackbody[cloud_spec][window][0.5])
        opd1_bb.append(differences_blackbody[cloud_spec][window][1.0])
        opd3_bb.append(differences_blackbody[cloud_spec][window][3.0])
        opd8_bb.append(differences_blackbody[cloud_spec][window][8.0])

    legend,c = ("ice", "r+-") if ind % 2 == 1 else ("water","g*-")

    plt.plot(microwindow_val, opd02_bb, c,alpha=0.7, label=legend)
    plt.plot(microwindow_val, opd05_bb, c,alpha=0.7)
    plt.plot(microwindow_val, opd1_bb, c,alpha=0.7)
    plt.plot(microwindow_val, opd3_bb, c,alpha=0.7)
    plt.plot(microwindow_val, opd8_bb, c,alpha=0.7)
    

    if ind % 2 == 1:
        plt.legend()
        plt.title(headers[ind] + " " + headers[ind-1])
        plt.show()

# for cloud_spec in differences_transmittances:   
#     for i,window in enumerate(microwindows):
#         opd02_trans.append(differences_transmittances[cloud_spec][window][0.2])
#         opd05_trans.append(differences_transmittances[cloud_spec][window][0.5])
#         opd1_trans.append(differences_transmittances[cloud_spec][window][1.0])
#         opd3_trans.append(differences_transmittances[cloud_spec][window][3.0])
#         opd8_trans.append(differences_transmittances[cloud_spec][window][8.0])



# plt.plot(microwindow_val, opd02_trans, label="0.2")
# plt.plot(microwindow_val, opd05_trans, label="0.5")
# plt.plot(microwindow_val, opd1_trans, label="1.0")
# plt.plot(microwindow_val, opd3_trans, label="3.0")
# plt.plot(microwindow_val, opd8_trans, label="8.0")

# plt.legend()
# plt.show()


