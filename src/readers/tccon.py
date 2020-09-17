'''
	Module for code to read Eureka Radiosonde profiles into pandas dataframes

'''

import xarray as xr
import netCDF4
import matplotlib.pyplot as plt

# cc = xr.open_dataset(filename, decode_times=False)

# df = cc.to_dataframe()
def read_tccon(filename, date):

	'''
	filename: name of tccon data file
	date: day of year to retrieve co2 priors for

	'''

	nc = netCDF4.Dataset(filename)

	co2_priors = nc['prior_co2'] #Of dimenisons (366,71), ('prior_date', 'prior_Height')

	#Want Mar 20, 80th day of the year (on leap yrs)
	co2_profile = co2_priors[80,:]

	return co2_profile
	#plt.plot(co2_profile,nc['prior_Height'])
	#plt.show()


file = "../tccon/eu20100724_20190815.public.nc"
