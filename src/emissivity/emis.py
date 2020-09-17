import numpy as np
#import readers
#print(readers)
import readers.eaeri as eaeri_reader
import readers.ndacc as ndacc_reader
import readers.tccon as tccon_reader
import readers.gruan as gruan_reader
import readers.ncep as ncep_reader


import processing.eaeri as eaeri_pro
import helpers.general as tools

#from readers import lbldis,tccon,eaeri,gruan
#from readers import eaeri


# =============== Retrieve closest (temporal) E-AERI spectra with clear skies
eaeri_dataframes = eaeri_reader.read_eaeri(["2009"])
eaeri_data = {}

for days in eaeri_dataframes:
    eaeri_data[days] = eaeri_pro.EAERI(eaeri_dataframes[days])

# Retrieve closest spectras to (returns datetime object)
cloudy_spectra_time = eaeri_data['090620'].find_closest_spectra('17:30:00')
clear_spectra_time = eaeri_data['090620'].find_closest_spectra('15:00:00')

print(clear_spectra)

# ================ Retrieve atmospheric profiles for particular day
# NDACC ch4 co n2o o3 altitude pressure

#All profiles go high to low
# ndacc_O3_all = ndacc_reader.read_hdf('ndacc/','O3')
# O3_retr_time = ndacc_reader.find_closest_retrival(ndac_O3, clear_spectra_time)
# ndacc_O3 = ndacc_O3_all['O3.MIXING.RATIO.VOLUME_ABSORPTION.SOLAR']['2009-06-20 15:08:00'].values[0]

# ndacc_CO_all = ndacc_reader.read_hdf('ndacc/','CO')
# CO_retr_time = ndacc_reader.find_closest_retrival(ndac_CO, clear_spectra_time)
# ndacc_CO = ndacc_CO_all['CO.MIXING.RATIO.VOLUME_ABSORPTION.SOLAR']['2009-06-20 15:08:00'].values[0]

# ndacc_N2O_all = ndacc_reader.read_hdf('ndacc/','N2O')
# N2O_retr_time = ndacc_reader.find_closest_retrival(ndac_N2O, clear_spectra_time)
# ndacc_N2O = ndacc_N2O_all['N2O.MIXING.RATIO.VOLUME_ABSORPTION.SOLAR']['2009-06-20 15:08:00'].values[0]

# ndacc_CH4_all = ndacc_reader.read_hdf('ndacc/','CH4')
# CH4_retr_time = ndacc_reader.find_closest_retrival(ndac_CH4, clear_spectra_time)
# ndacc_CH4 = ndacc_CH4_all['CH4.MIXING.RATIO.VOLUME_ABSORPTION.SOLAR']['2009-06-20 15:08:00'].values[0]

ndacc_O3 = tools.read_obj('O3')
ndacc_CO = tools.read_obj('CO')
ndacc_CH4 = tools.read_obj('CH4')
ndacc_N2O = tools.read_obj('N2O')

altitude = tools.read_obj('ALTITUDE') #ndacc_O3_all['ALTITUDE']['2009-06-20 15:08'].values[0] #High to low
pressure = tools.read_obj('PRESSURE') #ndacc_O3_all['PRESSURE_INDEPENDENT']['2009-06-20 15:08'].values[0]


# CO2 from TCCON
tccon_file = "eu20100724_20190815.public.nc"
tccon_co2 = tccon_reader.read_tccon(tccon_file,172) #Jun 20


#H2O from gruan
gruan_file = "ERK-RS-01_2_RS92-GDP_002_20090531T000000_1-000-001.nc"
gruan_h2o = gruan_reader.load_gruan_by_date(gruan_fname)

ncep_temp_file = "TempNMC_eur_2009.dat"
temperature = ncep_reader.read_ncep(ncep_temp_file, "20090620")



# ================ Run LBLRTM (And get atmospheric transmittances)



# ================ Run LBLDIS to simulate blackbody clouds


# ================ Calculate cloud emissivity and plot (overlaid on plots of cloud emissivity simulations to see where particular datapoint lies)

