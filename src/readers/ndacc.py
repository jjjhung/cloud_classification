from pyhdf import SD
import os
##################################################################################
import numpy as np
import pandas as pd
import datetime as dt
import sys 
##################################################################################

def read_ftir(FILE_NAME):
    """ Read NDACC HDF file. File and variable names to be specified by user
    when under name == main """

    hdf=SD.SD(FILE_NAME)

    # read attributes 
    lst = hdf.attributes()
    var = lst['DATA_VARIABLES'].split(';')
    data = [] 

    #----------------------------------------
    for v in var:
        #--------------------------------    
        try:
            sds = hdf.select(v)
            data.append(sds.get())     
        except:
            print ('No SDS found: '+v)
            var.pop(v)           
        #-------------------------------- 	    

    #----------------------------------------
    return var, data

def read_hdf(hdf_dir,spec):
    """ Read in all HDF files from specified directory for specified gas
    CO, O3, N2O, etc
    """ 

    files = [x for x in os.listdir(hdf_dir) if x.endswith('.hdf')]

    dataFTIR = pd.DataFrame()

    for f in files:
        gas = f.split('_')[1][5:].strip()
        GAS = ''.join(map(lambda x:x.upper(),gas)).replace('L','l')

        if GAS == spec:
            start_date = dt.datetime.strptime(f.split('_')[4][:8],'%Y%m%d').date()
            end_date = dt.datetime.strptime(f.split('_')[5][:8],'%Y%m%d').date()	    
	
            file_name = os.path.join(hdf_dir,f)
            var, temp = read_ftir(file_name)
            ftir_data = []

             #-------------------------------------------------------------------------
             #Convert FTIR Data to DataFrame
             #-------------------------------------------------------------------------    
            date = temp[0] 
            temp[0] = np.array([dt.datetime(2000,1,1,0,0,0)+dt.timedelta(days=np.float64(dtm_mjd2k_s)) for dtm_mjd2k_s in date])
            
            temp[1] = np.array([temp[1][0] for d in date])    # LATITUDE.INSTRUMENT
            temp[2] = np.array([temp[2][0] for d in date])    # LONGITUDE.INSTRUMENT
            temp[3] = np.array([temp[3][0] for d in date])    # ALTITUDE.INSTRUMENT
            temp[6] = [temp[6] for d in date]         # ALTITUDE
            temp[7] = [temp[7] for d in date]         # ALTITUDE.BOUNDARIES
            temp = list(zip(*temp)) # map(list, zip(*temp)), for python2
            dataFTIR = dataFTIR.append(pd.DataFrame(temp,columns=var))

    #dataFTIR = dataFTIR.sort_values('DATETIME') 
    dataFTIR.index = pd.to_datetime(dataFTIR['DATETIME'])
    del dataFTIR['DATETIME'] 
 

    return dataFTIR.sort_index()

def find_closest_retrival(data, datetime):
    '''
    Searches ftir retrivals for closest (temportal) profile
    Returns datetime of found spectra
    '''
    dt = pd.to_datetime(datetime)
    idx = data.index[data.index.get_loc(dt,method='nearest')]

    return idx

