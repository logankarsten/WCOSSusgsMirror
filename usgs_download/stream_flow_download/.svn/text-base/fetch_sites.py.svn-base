#!/usr/bin/python

import os, sys, time, urllib, getopt
from string import *

#
# Download real time stream flow data from the USGS server for 
# a given list of stations.
#
def fetch_sites( site_nos, odir, failed_sites ):

    #
    # Loop through each station
    #
    for site_no in site_nos:
          #
          # Construct the query URL
          # 
          #URL = ( 'https://staging.waterservices.usgs.gov/nwis/iv/?sites='+
          URL = ( 'https://waterservices.usgs.gov/nwis/iv/?sites='+
	        site_no+
		'&format=waterml,2.0&parameterCd=00060&period=PT6H' )
          #
          # Connect to the server
          # 
	  try:
            rno = urllib.urlopen(URL)
	  except IOError as e:
	    print 'WARN: site : ', site_no, ' skipped - ' #, e.reason 
            #
            # If failed, remember the station no and continue
            # 
	    failed_sites.append( site_no )
            continue

          #
          # Write the real time flow data to waterML files
          #
          wfo = open(odir+'/'+site_no+'.xml','w')

	  try:
             wfo.write(rno.read())
	  except IOError as e:
	    print 'WARN: site : ', site_no, ' skipped - ' #, e.reason 
	    failed_sites.append( site_no )
            continue

          #
          # Close the connection and WaterML files
          #
          rno.close()
          wfo.close()
    return
