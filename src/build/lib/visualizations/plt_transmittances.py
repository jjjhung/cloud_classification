'''
Read calculated transmittance from TAPE28 file from lblrtm
'''

import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
sfile2 = "../../Models/aer_lblrtm_v12.9_lnfl_v3.2/lblrtm_v12.9/TAPE28"


with open(sfile2,"r") as ff:
	content=ff.readlines()[28:]

content_holder = np.zeros((len(content),2))
for i,line in enumerate(content):
	content[i] = line.split('       ')
	content_holder[i][0] = float(content[i][0])	
	content_holder[i][1] = float(content[i][1])

microwindow_val = [496.75, 530.7, 560.25, 832.25, 845.25, 874.35, 901.6, 1096.6, 1114.8, 1231.75]

# for i,j in enumerate(microwindow_val):
# 	print(i)
# 	print(content_holder[:,0][np.argmin(np.abs(content_holder[:,0] - microwindow_val[i]))])

#print((content_holder[:,0][39] - microwindow_val[0]))
plt.plot(content_holder[:,0], content_holder[:,1])
plt.show()