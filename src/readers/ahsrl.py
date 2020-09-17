def read_LIDAR_netcdf(years, columns_to_keep):
    '''
    Reads in nc files from LIDAR (ahrsl) data
    Returns a dictionary of dataframes with revelant columns (backscatter coefficient
        and depolarization ratios), used for determining cloudiness and cloud phase
        of the form dict[date] = dataframe
    

    Params 
    =============
    - years : Selected years to read in 
    - columns_to_keep : List[String] of datacolumns to keep
    '''
    dataframes = {}

    for year in years:
        prepended_dir = str(year)

        for file in os.listdir(prepended_dir):
            if Path('./' + file).suffix == '.nc': # Only read nc filename
                xar = xr.open_dataset(prepended_dir + '/' + file)

                date = Path(file).stem
                #print(date)
                dataframes[date] = xar[columns_to_keep].to_dataframe()

    return dataframes
