#! /usr/bin/python

import os, sys, time, urllib, getopt, copy
from string import *
import find_changed_site_for_huc


#
# Function to get input directory
#
def main(argv):
   outputdir = ''
   try:
      opts, args = getopt.getopt(argv,"h:o:",["odir="])
   except getopt.GetoptError:
      print 'usgs_iv_retrieval.py -o <outputdir>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'usgs_iv_retrieval.py -o <outputdir>'
         sys.exit()
      elif opt in ("-o", "--odir"):
         outputdir = arg
         if not os.path.exists( outputdir ):
             os.makedirs( arg )
  
   print 'Output dir is "', outputdir
   return outputdir

#
# delete files older than number of days in a given directory
#
def cleanup_dir( path, numberofdays ):
   if not os.path.isdir(path ):
	   return

   now = time.time()
   cutoff = now - ( numberofdays * 86400 )
   files = os.listdir( path )
   for onefile in files:
	   if os.path.isfile( path + '/' + onefile ):
		   t = os.stat( path + '/' + onefile )
		   c = t.st_mtime
		   if c < cutoff :
			   os.remove( path + '/' + onefile )
   return

#
# The main function to download real time stream flow
#
def usgs_iv_retrieval( odir, download_id, hucs ):

#
# For the first loop, get all stations that have data upated in the last 15 minutes.
# In the following loops, use the actual time interval between the loops
#
  timeSinceLast = 15
#
# Time stamp when the process starts
#
  URL_start = [ time.time()] * len( hucs )

  firstloop = True
#
# Got to the infinite loop
#
  while True:

     #
     # touch a file and update the time stamp to indicate it is alive 
     #
     with open( odir + '/usgs_iv_retrieval_' + download_id, 'a'):
	     os.utime( odir + '/usgs_iv_retrieval_' + download_id, None )
#
# remove files older than two days in the output directory
#
#  NCO is using a cron job to remove old files. So don't delete old file here
#     print 'cleaning up ...'
#     cleanup_dir( odir, 2 )
#

# Initialize the lists for time tracking
#
     counter_start = time.time()
     total_sites = 0

     huc_seq = 0

#
#    Loop through each HUC
#
     for huc in hucs:
        site_noL = []
	if not firstloop:
           timeSinceLast = ( time.time() - URL_start[ huc_seq ] ) / 60
           #
           #If two queries are less than 2 minutes apart, wait
           # two minutes before the next query.
           #
           if timeSinceLast < 2:
                time.sleep( 120 )
		timeSinceLast = ( time.time() - URL_start[ huc_seq ] ) / 60
            
        URL_start[ huc_seq ] = time.time()

        no_of_sites = []
        #
        # Query the USGS server to find the stations that have updated their 
        # real time data.
        #
        find_changed_site_for_huc.find_changed_sites_for_huc( huc, timeSinceLast, odir, site_noL, no_of_sites )

	print download_id, ': looptime = ', counter_start, 'num. of sites = ', len(site_noL)

        #
        # Count the total number of sites that have been updated
        #
        if no_of_sites:
          total_sites += no_of_sites[ 0 ] 

        #
        # If there are any stations that are failed during the query such as
        # no responding from the server, wait for 10 seconds and  try again.
        #
	if not site_noL:
  	  print ( download_id + ": wait 10 seconds and try again!" )
          time.sleep( 10 )
          no_of_sites = []
          find_changed_site_for_huc.find_changed_sites_for_huc( huc, timeSinceLast, odir, site_noL, no_of_sites )


          #
          # The failed sites need to be counted too.
          #
          if no_of_sites:
            total_sites += no_of_sites[ 0 ] 

        #
        # increment the sequence number
        #
        huc_seq += 1

     URL_end = time.time()
     #
     # print total time spent on this loop
     #
     print download_id, ': looptime = ', counter_start, round( ( URL_end - counter_start ) / 60, 2)

     #
     # not the first loop
     #
     firstloop = False

def download_for_hucs( odir, hucs, download_id  ):

    #
    # call the real time retrieval function
    # 
    usgs_iv_retrieval( odir, download_id, hucs )
