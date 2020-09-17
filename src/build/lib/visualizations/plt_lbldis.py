import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
'''
data_1 = np.genfromtxt('../../Models/lbldis/out_single_water_cloud_high_opt_depth_2', skip_header=2, usecols=(0,1))
data_2 = np.genfromtxt('../../Models/lbldis/out_single_water_cloud_low_opt_depth', skip_header=2, usecols=(0,1))
#print(data)

#print(data[0,1])
data_1 = np.array([list(x) for i,x in enumerate(data_1) if data_1[i,1] > 0])
data_2 = np.array([list(x) for i,x in enumerate(data_2) if data_2[i,1] > 0])
#print(np.array(data))
wnum_1,rad_1 = data_1[:,0], data_1[:,1]
plt.plot(wnum_1,rad_1,label="high_opt")

#print(np.array(data))
wnum_2,rad_2 = data_2[:,0], data_2[:,1]
plt.plot(wnum_2,rad_2,label="low_opt")
plt.legend()
plt.show()
'''
data_1 = np.genfromtxt('../../Models/lbldis/out/water_7um/out_water_7um_495.5_498', skip_header=2, usecols=(0,1,2,3,4,5))

#data_1 = np.genfromtxt('../../Models/lbldis/out/water_7um/out_water_7um_495.5_498', skip_header=2, usecols=(0,1,2,3,4,5))
#print(data)

#print(data[0,1])
data_1 = np.array([list(x) for i,x in enumerate(data_1) if data_1[i,1] > 0])
#print(np.array(data))
wnum_1,rad_1 = data_1[:,0], data_1[:,1]
plt.plot(wnum_1,rad_1,alpha=0.5, label="0.2")
plt.plot(wnum_1,data_1[:,2],alpha=0.5, label="0.5")
plt.plot(wnum_1,data_1[:,3],alpha=0.5, label="1.0")
plt.plot(wnum_1,data_1[:,4],alpha=0.5, label="3.0")
plt.plot(wnum_1,data_1[:,5],alpha=0.5, label="8.0")
plt.legend()
#print(np.array(data))
plt.show()
