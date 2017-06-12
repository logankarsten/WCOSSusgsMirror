# Python program to loop through the previous 12 hours worth of USGS
# time slices being generated here on cospa-c1. There will be an ongoing
# text file that will contain each datetime of the file, along with a last
# modified. If the file gets updated, it will be copied over to a temporary
# directory on Yellowstone. The updated file modified time will be updated 
# into the CSV file accordiingly. Once the loop is finished, a final 
# progress file will note the time at which the files were finished copying 
# over. This file will then be pushed to Yellowstone as well. A 
# cron job on Yellowstone will check the temporary directory for the progress
# file, and perform an atomic move to the final directory where the files 
# will reside. 

# Logan Karsten
# National Center for Atmospheric Research
# Research Applications Laboratory

import pandas as pd
import datetime
import math
import os
import numpy as np

numHoursBack = 18
ysDir = '/glade/scratch/karsten/USGS_TIMESLICES_MIRROR/STAGING'
cosDir = '/raid5/karsten/USGS_TIMESLICES/data/netcdf_timeslices'
csvStatusPath = cosDir + '/fileList.csv'

dNow = datetime.datetime.utcnow()
minQuarter = int(math.floor(dNow.minute/15.0))*15
eDate = datetime.datetime(dNow.year,dNow.month,dNow.day,dNow.hour,minQuarter)
bDate = eDate - datetime.timedelta(seconds=numHoursBack*3600)
nSteps = numHoursBack*4 # Data produced every 15 minutes. 

# Create array of seconds since epoch representing the timestep for each file we will be checking for.
fileSteps = np.empty([nSteps],np.int32)
fileMods = np.empty([nSteps],np.int32)
updateFlags = np.empty([nSteps],np.int)
updateFlags[:] = 0
fileMods[:] = -99
for i in range(0,nSteps):
	dCurrent = bDate + datetime.timedelta(seconds=900*i)
	fileSteps[i] = int(dCurrent.strftime('%s'))

# Open existing CSV file. If it's not present, create one.
progressUpdate = 0 # Flag indicating if ANY files have been updated since last check.
if os.path.isfile(csvStatusPath):
	dataMods = pd.read_csv(csvStatusPath)
else:
	# Create empty data frame to hold datetime information
	dTmp = {'fileMod':fileMods,'fileStep':fileSteps,'update':updateFlags}
	dataMods = pd.DataFrame(dTmp)
	progressUpdate = 1

# filter out values that are now outside the time window of checking and update the 
# data frame to include new time steps.
stepsCheck = dataMods.fileStep
modsCheck = dataMods.fileMod
stepsNew = np.empty([nSteps],np.int32)
modsNew = np.empty([nSteps],np.int32)
stepsNew[:] = fileSteps
modsNew[:] = -99

for i in range(0,nSteps):
	indChk = np.where(stepsCheck == stepsNew[i])
	if len(indChk[0]) != 0:
		modsNew[i] = modsCheck[indChk[0][0]]
	else:
		modsNew[i] = -99
		progressUpdate = 1

# Now, loop through each time step again, compose the file path to the USGS time slice on 
for i in range(0,nSteps):
	dCurrentStep = datetime.datetime.utcfromtimestamp(stepsNew[i])
	cosPath = cosDir + "/" + dCurrentStep.strftime('%Y-%m-%d_%H:%M') + ':00.15min.usgsTimeSlice.ncdf'
	
	if os.path.isfile(cosPath):
		modTimeTmp = int(os.path.getmtime(cosPath))
		# We need to make a fair assumption about the size of the 
		# file. The USGS timeslice files are approximately 13638000 bytes. Only
		# update things if the file size is > 12000000 bytes to be sure things are 
		# either updated, or about to be udated. 
		sizeTmp = os.path.getsize(cosPath)
	if modTimeTmp != modsNew[i] and sizeTmp >= 12000000:
		# File was updated.
		progressUpdate = 1
		updateFlags[i] = 1
		modsNew[i] = modTimeTmp

# Re-Compose the data frame, which will be written out to a CSV file and swept up by Yellowstone.
dTmp = {'fileMod':modsNew,'fileStep':stepsNew,'update':updateFlags}
dataMods = pd.DataFrame(dTmp)	
dataMods.to_csv(csvStatusPath)	
