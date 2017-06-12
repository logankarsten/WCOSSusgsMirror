#!/bin/bash
export PATH=/glade/apps/opt/ncview/2.1.1/gnu/4.4.6/bin:/glade/apps/opt/nco/4.5.5/gnu/4.8.2/bin:/glade/apps/opt/esmf/7.0.0-defio/intel/12.1.5/bin/binO/Linux.intel.64.mpich2.default:/glade/u/home/karsten/anaconda2/bin:/glade/u/home/karsten/lib/grib_api_1.14.2_intel/bin:/usr/lib64/qt-3.3/bin:/glade/apps/opt/netcdf/4.3.0/intel/12.1.5/bin:/glade/apps/opt/modulefiles/ys/cmpwrappers:/ncar/opt/intel/12.1.0.233/composer_xe_2011_sp1.11.339/bin/intel64:/glade/apps/opt/usr/bin:/ncar/opt/lsf/9.1/linux2.6-glibc2.3-x86_64/etc:/ncar/opt/lsf/9.1/linux2.6-glibc2.3-x86_64/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/openssh/5.7p1krb/bin:/usr/local/sbin:/opt/ibutils/bin:/ncar/opt/hpss:/glade/apps/opt/r/3.2.2/intel/16.0.0/bin:/glade/apps/opt/ncl/6.3.0/intel/12.1.5/bin

cd /glade/scratch/karsten/USGS_TIMESLICES_MIRROR/programs
python pull_cospa.py
