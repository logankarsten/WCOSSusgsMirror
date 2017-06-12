#Program to pull realtime USGS time slice files being generated on cospa-c1.
#First step is to pull the latest file list that lists the last six hours
#of files, along with their modification dates. Next, the program
#will loop through each time step and cross check the modified times on the
#files here on Yellowstone. If they are different, we will pull the lates file
#from cospa-c1, double check the modified time. Lastly, an atomic move will take
#place from the staging directory to the final directory. Another final file
#will be created in the final output directory with a date/time stamp indicating
# when the final files (if updated) were re-pushed.

# Logan Karsten 
# National Center for Atmospheric Research
# Research Applications Laboratory

import subprocess
import numpy as np
import pandas as pd
import os
import datetime
import sys

stageDir = '/glade/scratch/karsten/USGS_TIMESLICES_MIRROR/STAGING'
finalDir = '/glade/scratch/karsten/USGS_TIMESLICES_MIRROR/NC_FILES'
cosList = '/raid5/karsten/USGS_TIMESLICES/data/netcdf_timeslices/fileList.csv'
fileList = stageDir + '/fileList.csv'
progressFile = finalDir + '/lastUpdated.txt'

if os.path.isfile(fileList):
	os.remove(fileList)

# Cleanout any remaining files that may exist in the directory
cmd = "rm -rf " + stageDir + "/*"
subprocess.call(cmd,shell=True)

# First, pull file list CSV from cospa-c1
cmd = "sshpass -p 'Purdy$1986_05' scp -rp karsten@cospa-c1.rap.ucar.edu:" + cosList + " " + fileList
subprocess.call(cmd,shell=True)

# Next, read in CSV file
dfList = pd.read_csv(fileList)
numSteps = len(dfList.fileStep)

count = 0
for i in range(0,numSteps):
	downloadFlag = 0
	dCurrentUtc = datetime.datetime.utcfromtimestamp(dfList.fileStep[i])
	dModUtcCheck = datetime.datetime.utcfromtimestamp(dfList.fileMod[i])
	fileCheckYS = finalDir + "/" + dCurrentUtc.strftime('%Y-%m-%d_%H:%M') + ":00.15min.usgsTimeSlice.ncdf"
	if os.path.isfile(fileCheckYS):
		# Get modified time in UTC
		modTime = os.path.getmtime(fileCheckYS)
		modStamp = datetime.datetime.fromtimestamp(modTime)
		modSeconds = int(modStamp.strftime('%s'))
		if float(modSeconds) < float(dfList.fileMod[i]):
			# This means the file on Yellowstone is older than what is on 
			# cospa-c1
			downloadFlag = 1
	else:
		# File doesn't yet exist on Yellowstone, we need to download for the first time
		downloadFlag = 1

	# Download files as necessary
	if downloadFlag == 1:
		dlPath = "/raid5/karsten/USGS_TIMESLICES/data/netcdf_timeslices/" + \
                         dCurrentUtc.strftime('%Y-%m-%d_%H:%M') + ":00.15min.usgsTimeSlice.ncdf"
		stagePath = stageDir + "/" + dCurrentUtc.strftime('%Y-%m-%d_%H:%M') + ":00.15min.usgsTimeSlice.ncdf"
		cmd = "sshpass -p 'Purdy$1986_05' scp -rp karsten@cospa-c1.rap.ucar.edu:" + \
                      dlPath + " " + stagePath
		subprocess.call(cmd,shell=True)
		count = count + 1
	
if count > 0:
	# Downloaded or updated files that need to be moved over to the final directory.
	# Move the files, create a new progress text file, then move everything over.
	fileP = open(progressFile,'w')
	dNow = datetime.datetime.utcnow()
	secNow = dNow.strftime('%Y-%m-%d_%H:%M:%S')
	fileP.write(secNow)
	fileP.close()
	
	# Move everything over to the final directory from the staging directory.
	cmd = "mv " + stageDir + "/* " + finalDir
	subprocess.call(cmd,shell=True)

