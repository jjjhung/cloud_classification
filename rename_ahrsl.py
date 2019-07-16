'''
	Convenience script to rename ahrsl files to format YYMMDD.nc
'''

import os
from pathlib import Path

for filename in os.listdir('.'):
	if Path('./' + filename).suffix == '.nc': # Only convert nc filenames
		os.rename(filename, filename[8:14]) 

ahsrl_20090616T2155_20090716T2355_60s_45m.nc 