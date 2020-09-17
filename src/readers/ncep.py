import numpy as np

def read_ncep(filename, date):
'''
Loads ncep temperature / pressure profiles for provided date
date form is "YYYYMMDD"
'''
data_temps = {}

raw_data = np.loadtxt(filename, skiprows=20)
for i in raw_data:
    data_temps[i[0]] = i[1:]


return data_temps[date]
