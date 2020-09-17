import os
import re
import subprocess

#For now
lbldis_dir = '/home/joseph/Documents/Atmosp/Ice/Models/lbldis/'
param_file_dir = 'param_files/'
output_file_dir = 'out/'

for file in os.listdir(lbldis_dir + param_file_dir):
    if re.search('^ice*', file):
        subprocess.call(lbldis_dir + 'lbldis false ' + lbldis_dir + param_file_dir + file + " false " + lbldis_dir + output_file_dir + 'out_' + file)
    
