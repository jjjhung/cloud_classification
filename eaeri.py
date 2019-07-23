import helpers
import itertools # Combinations

class EAERI:
    '''
    Class detailing one day of eaeri observations
    '''

    microwindows = [(410.4, 7.6),(438.4,2.8),(449.6,3.2),(464.4,3.6),
            (478.8,6.8),(497.2,6.8),(522.4,3.2),(531.2,3.2), 
            (559.2,6.4),(573.2,3.2),(680,9.2),(840,10),
            (870,10),(900,10)]


    def __init__(self, dataframe):
        '''
        Converts a dataframe from a netcdf file of EAERI data to a slimmed
            down version for easier processing

        '''
        temp = dataframe.reset_index()
        time_values = temp['time'].unique()
        g = temp.groupby(['time'])

        self.data = temp

    def retrieve_microwindow_averages(self, datetime):
        '''
        Calculates microwindow average features for the provided datetime

        datetime: Pandas datetime object notation (can be a string)
            Example: "2009-02-04 12:00:00"

        Returns dict[CentralWaveNumber] -> average Brightess Temperature for microwindow
        '''

        BT_features = {}
        for mw in self.microwindows:
            slice_start = mw[0] - mw[1]
            slice_end = mw[0] + mw[1]
            truncated = self.data.loc[(self.data['wnum1'] >= slice_start) & (self.data['wnum1'] <= slice_end) & (self.data['time_offset'] == '2008-11-10 00:08:30')]

#            small_frame = helpers.read_wavenumber_slice(self.data, (slice_start, slice_end))
            
            # Convert radiance W to mW
            truncated.mean_rad /= 1000
            averaged = truncated['mean_rad'].mean()


            BT_features[mw[0]] = helpers.brightness_temp(averaged, mw[0])

        return BT_features


    @staticmethod
    def retrieve_microwindow_differences(BT_features):
        '''
        Static function
        Computes differences between each microwindow. Returns a 91 element feature array
        
        BT_features: dict[CentralWaveNumber] -> average Brightess Temperature for microwindow
        
        Returns BT_differences: dict[tuple(a,b)] -> Brightness Temperature difference in microwindows centered around a and b

        '''

        # Need ordered list since BT_features is a hashtable
        features = list(BT_features)
        BT_differences = {}

        for i,comb in enumerate(itertools.combinations(features, 2)):

            #print(i,comb)
            BT_differences[comb] = abs(BT_features[comb[0]] - BT_features[comb[1]])

        return BT_differences


