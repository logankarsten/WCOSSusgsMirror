#!/usr/bin/python

import os, sys, time, urllib, getopt, copy
from string import *
import fetch_sites

#
# 1) Find the stations that have updated data for a given HUC and
#  time interval.
# 2) Download real time data for the list of stations found.
#

def find_changed_sites_for_huc( huc, timeSinceLast, odir, site_noL, \
                                 total_num_of_sites ):

        #
        # Consturct an url for the USGS server
        #
#        URL = ( 'https://staging.waterdata.usgs.gov/nwis/current?huc2_cd=' +
        URL = ( 'https://waterdata.usgs.gov/nwis/current?huc2_cd=' +
	      str(huc).zfill(2) +
	      '&result_md=1&result_md_minutes='+
	      str( int(round( timeSinceLast ) ) )+
	      '&index_pmcode_00060=3&format=rdb' )

        print 'HUC URL = ', URL

        #
        # Connect to the USGS server
        #
	try:
           rno    = urllib.urlopen(URL)
        except IOError as e:
		print ( 'Failed connecting to the server.' )
 #		print ( 'Reason: ', e.reason )
		return

        #
        # Download the station list 
        #
        try:
           linesL = rno.read().split('\n')
        except IOError as e:
		print ( 'Failed reading the server.' )
 #		print ( 'Reason: ', e.reason )
                return

        #
        # Close the connection
        #
        rno.close()
        #
        # Parse the webpage and get the station names.
        #
	if linesL[0] == 'No sites/data found using ' \
	                         'the selection criteria specified ':
            print('WARN: ', linesL[ 0 ], ' for huc ', huc )
	    site_noL = []
	    return

        del linesL[-1]
        while 1:
           if linesL[0][0] == '#':
              del linesL[0]
           else:
              del linesL[0]
              del linesL[0]
              break
        for line in linesL:
           site_noL.append(line.split('\t')[1])


        print  'num. of sites = ', len(site_noL)

        failed_sites = []

        #
        # Start download the real time stream flow data for the 
        #  list of stations that have updated data.
        #
        fetch_sites.fetch_sites( site_noL, odir, failed_sites )    
	#
        # Some stations may fail during the downloading, then wait for 10 seconds,
        # and try again
	#
	if len( failed_sites ) > 0:
	    print ('There are ', len(failed_sites), ' failed sites, try again ......')
	    #sleep 10 seconds
	    time.sleep( 10 )
            site_noL = copy.deepcopy( failed_sites )

            #
            # Re-do the downloading
            #
            fetch_sites.fetch_sites( site_noL, odir, failed_sites )    

	    print ('Done retry ', len(failed_sites), ' of failed sites.')
            

        return
