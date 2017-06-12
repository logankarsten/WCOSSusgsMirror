#! /usr/bin/python

import os, sys, time, urllib, getopt
from string import *
import xml.etree.ElementTree as etree
from datetime import datetime, timedelta
from USGS_Observation import USGS_Observation, All_USGS_Observations
from TimeSlice import TimeSlice
#import Tracer

"""
   The driver to parse downloaded waterML 2.0 observations and 
   create time slices and write to NetCDF files
   Author: Zhengtao Cui (Zhengtao.Cui@noaa.gov)
   Date: Aug. 26, 2015
"""
def main(argv):
   """
     function to get input arguments
   """
   inputdir = ''
   try:
	   opts, args = getopt.getopt(argv,"hi:o:",["idir=", "odir="])
   except getopt.GetoptError:
      print 'make_time_slice_from_usgs_waterml.py -i <inputdir> -o <outputdir>' 
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print   \
           'make_time_slice_from_usgs_waterml.py -i <inputdir> -o <outputdir>' 
         sys.exit()
      elif opt in ('-i', "--idir"):
         inputdir = arg
         if not os.path.exists( inputdir ):
		 raise RuntimeError( 'FATAL Error: inputdir ' + \
				 inputdir + ' does not exist!' )
      elif opt in ('-o', "--odir" ):
         outputdir = arg
         if not os.path.exists( outputdir ):
		 raise RuntimeError( 'FATAL Error: outputdir ' + \
				 outputdir + ' does not exist!' )
  
   print 'input dir is "', inputdir, '"'
   print 'output dir is "', outputdir, '"'
   return (inputdir, outputdir)

if __name__ == "__main__":
   odir = main(sys.argv[1:])

indir = odir[0]
outdir = odir[1]

print sys.path
#
# Load USGS observed waterML 2.0 discharge data
#

#The trace module run function works for a function but doesn't
# in a class method.
#
#def foo():
#	print "inside foo"
#	x = 20 + 40
#	return 'Hello'
#
#Tracer.init()
#
#Tracer.theTracer.run( 'a = foo()' )

#print 'a = ', a

allobvs = All_USGS_Observations( indir )

print 'earlist time: ', allobvs.timePeriodForAll()[0].isoformat()
print 'latest time: ', allobvs.timePeriodForAll()[1].isoformat()

#
# Create time slices from loaded observations
#
# Set time resolution to 15 minutes
# and
# Write time slices to NetCDF files
#
timeslices = allobvs.makeAllTimeSlices( timedelta( minutes = 15 ), outdir )

print "totol number of timeslices: ", timeslices
