import xarray as xr
import netCDF4
import matplotlib.pyplot as plt

filename = "../../data/tccon/eu20100724_20190815.public.nc"
# cc = xr.open_dataset(filename, decode_times=False)

# df = cc.to_dataframe()
nc = netCDF4.Dataset(filename)

co2_priors = nc['prior_co2'] #Of dimenisons (366,71), ('prior_date', 'prior_Height')

#Want Mar 20, 80th day of the year
co2_profile = co2_priors[80,:]

plt.plot(co2_profile,nc['prior_Height'])
plt.show()
