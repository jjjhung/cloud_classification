'''
    Some helper functions related to EAERI measurements

'''

def brightness_temp(radiance, wnum):
    '''
    Returns the brightness temperature given the radiance (radiance) and wavenumber of measured light
    radiance is mW/m^2 * sr * cm
    Wavenumber is 1/cm

    Limit brightness temperature to [0,1000]

    '''
    wavenum = wnum * 100 # Convert wavenumber to 1/m
    radiance /= 1000 # Convert mW to W
    radiance *= -0.01001

    #radiance /= (2*constants.pi**2)

    ln_elements = -2 * constants.Planck * (wavenum**3) * (constants.speed_of_light**2) / (radiance)
    #ln_elements += 1
    
    coeff = constants.Planck * constants.speed_of_light * wavenum / constants.Boltzmann 
    
    # Numerical stability - log1p(x) does log(x + 1) stably 
    divid = coeff / np.log1p(ln_elements)

    # Sometimes divid is complex, probably because conversion error from xarray -> dataframe?
    real = divid if not np.iscomplex(divid) else np.real(divid)  

    # Enforce boundary conditions
    real = 0 if real < 0 else real
    real = 1000 if real > 1000 else real

    return real


def avg_brightness_temp(df):
    '''
    Calculates the average brightness temperature at 10um wavelength, 
        averaged over each 7 minute measurement period
        Adds the additional values as a new column titled 'avg_brightness_temp'
        Also classifies period as sunny or not, in new column titled 'sunny'

    '''
    temp_df = df
    temp_df['avg_brightness_temp'] = temp_df.apply(lambda row: brightness_temp(row.mean_rad, row.wnum1), axis=1)
    temp_df['sunny'] = temp_df.apply(lambda row: row.avg_brightness_temp > 225, axis=1)

    return temp_df

def coefficient_calculate(wavenum, temp, intensity):
    '''
    Calcutes the solid angle adjustment factor for converting the field of view in radians
    to the steradians given in the provided radiances
    '''

    expon = constants.Planck * constants.speed_of_light * wavenum / (temp * constants.Boltzmann)
    expon = np.exp(expon)
    expon = 1 - expon

    expon = 1/expon

    return expon * 2 * constants.Planck * constants.speed_of_light**2 * wavenum ** 3 / intensity


def read_wavenumber_slice(df, slice_range):
    '''
    Returns a truncated dataframe with only datapoints contained within the provided wavenumber range
        Params
        ==============
        - df : Pandas dataframe
        - slice_range: tuple of wavenumber (low,high), inclusive

        Returns
        ==============
            Pandas dataframe
    '''
    truncated = df.loc[(df['wnum1'] >= slice_range[0]) & (df['wnum1'] <= slice_range[1])]

    return truncated


def det_season(date):
    month = int(date[0][5:7])

    if month >= 6 and month <= 8:
        season = "S"
    elif month == 5 or month == 9:
        season = "F/S"
    else:
        season = "W"

    return season

def winter_radiances(rad):
    #rad = rad / 1000

    #print(rad)
    if rad < 0.0015:
        return "Clear"
    elif rad <= 0.009:
        return "Thin"
    else:
        return "Thick"

def fallspr_radiances(rad):
    #rad = rad / 1000

    if rad < 0.007:
        return "Clear"
    elif rad <= 0.02:
        return "Thin"
    else:
        return "Thick"

def summer_radiances(rad):
    #radiance = rad / 1000

    if rad < 0.015:
        return "Clear"
    elif rad <= 0.045:
        return "Thin"
    else:
        return "Thick"

def cloudify(date, df):
    season = det_season(date)
    temp_df = df
    
    rad_mean = temp_df['mean_rad'].mean()

    if season == 'W': #Winter
        return winter_radiances(rad_mean), season
    elif season == 'F/S': #Fall / Spring
        return fallspr_radiances(rad_mean), season
    elif season == 'S': #Summer
        return summer_radiances(rad_mean), season

