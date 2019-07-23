class Ahsrl: 
	'''
	Class detailing a single day of observation for the Arctic High Spectral Resolution Lidar

	
	'''

	# Data headers
	headers = ['radar_backscattercrosssection', 'radar_dopplervelocity','linear_depol']

	def __init__(self, dataframe):
		self.data = dataframe


	def return_classify_slice(self):
		'''
		This fuction returns a portion of the days' timeseries
		Will print the corresponding heatplots and allow user to classify the
			spectra as cloudy/not

		'''
		df2 = self.data.reset_index().pivot_table(columns='time', index='altitude',values=header)
		df2 = df2[::-1] # Columns are in reverse order by default.
		#df2 = dataframes['']
		#print(header)
		print(df2)
		sns.heatmap(df2)
		plt.savefig("./heatmaps/" + header + "_heatmap")
		plt.clf()

	def get_time_extract(self, datetime):
		'''
			Returns data corresponding to specified date 
		'''
		

