#!/bin/bash

source $HOME/.bashrc
# added by Anaconda2 4.3.1 installer
export PATH="/raid5/karsten/python_install/anaconda2/bin:$PATH"

python /raid5/karsten/USGS_TIMESLICES/programs/usgs_download/analysis/make_time_slice_from_usgs_waterml.py -i /raid5/karsten/USGS_TIMESLICES/data/usgs_streamflow -o /raid5/karsten/USGS_TIMESLICES/data/netcdf_timeslices > /raid5/karsten/USGS_TIMESLICES/data/logs/time_slices.log
