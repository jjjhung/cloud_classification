'''
Code for reading and parsing downwelling radiance simulated by the lbldis 

'''


import numpy as np

def read_lbldis(file_loc, num_cols):
	return np.genfromtxt(file_loc, skip_header=2, usecols=list(range(num_cols)))
