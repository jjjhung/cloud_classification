class EAERI:
	'''
	Class detailing one day of eaeri observations
	'''

	microwindows = [(410.4, 7.6),(438.4,2.8),(449.6,3.2),(464.4,3.6),
            (478.8,6.8),(497.2,6.8),(522.4,3.2),(531.2,3.2), 
            (559.2,6.4),(573.2,3.2),(680,9.2),(840,10),
            (870,10),(900,10)]


    def __init__(self, dataframe):
    	self.data = dataframe


    def retrieve_microwindow_averages(self):
    	
    	