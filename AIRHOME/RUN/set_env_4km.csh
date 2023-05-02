#! /bin/csh -f

# Commands necessary for singularity container
setenv PATH /usr/lib64/mpich-3.2/bin:$PATH
source /usr/share/Modules/init/csh
module use /opt/intel/oneapi/modulefiles
module load mpi
module load icc
setenv LD_LIBRARY_PATH /usr/local/lib:$LD_LIBRARY_PATH

# This script sets up common environment variables used by AIRPACT5 processes
#
#  April 29, 2015     JKV modified for running for AIRPACT5
#  February 14, 2013  JKV modified for running a second 24-hr MCIP 
#  December 24, 2008  JKV modified for 4-km nested airpact mcip 
#  April 09 2008   JKV modified for clearsky use.
#  Jan  2007  Joe Vaughan modified for testing on replacement rainier system
#  Created by Jack Chen 11/04
#

# Initialize exit status
set exitstat = 0

# Set common variables
setenv AIRTOOL      /opt/ioapi-3.2/Linux2_x86_64ifort
#setenv AIRRUN	    /home/airpact/AIRRUN/output/day1
# set and check $RUNROOT DIR
setenv RUNROOT $AIRRUN/output/${SRTYR}${SRTMN}${SRTDT}${SRTHR}/${MCIP_START}
if ( ! -d $RUNROOT ) then
  echo "Directory: $RUNROOT does not exist, create new."
  mkdir -p $RUNROOT
endif

# set runtime directories
setenv LOGDIR $RUNROOT/LOGS
if ( ! -d $LOGDIR ) mkdir -p $LOGDIR

# set run time variables
@ RUNLEN = ${RNLEN} / 10000
setenv SDATE `python -c "import datetime;  datenum = datetime.datetime(${SRTYR}, ${SRTMN}, ${SRTDT}); print(datenum.strftime('%Y%j'))"`
setenv EDATE `python -c "import datetime;  datenum = datetime.datetime(${SRTYR}, ${SRTMN}, ${SRTDT}) + datetime.timedelta(hours=${RUNLEN}); print(datenum.strftime('%Y%j'))"`
@ NUMHRS = ${STIME} / 10000
echo $NUMHRS
setenv ETIME `python -c "import datetime;  datenum = datetime.datetime(${SRTYR}, ${SRTMN}, ${SRTDT}) + datetime.timedelta(hours=${NUMHRS}); print(datenum.strftime('%H').zfill(2).ljust(6,'0'))"`
setenv ENDYR `python -c "import datetime;  datenum = datetime.datetime(${SRTYR}, ${SRTMN}, ${SRTDT}) + datetime.timedelta(hours=${RUNLEN}); print(datenum.strftime('%Y'))"`
setenv ENDMN `python -c "import datetime;  datenum = datetime.datetime(${SRTYR}, ${SRTMN}, ${SRTDT}) + datetime.timedelta(hours=${RUNLEN}); print(datenum.strftime('%m').zfill(2))"`
setenv ENDDT `python -c "import datetime;  datenum = datetime.datetime(${SRTYR}, ${SRTMN}, ${SRTDT}) + datetime.timedelta(hours=${RUNLEN}); print(datenum.strftime('%d').zfill(2))"`
echo "start date / time: $SDATE / $STIME : $SRTMN $SRTDT "
echo "  end date / time: $EDATE / $ETIME : $ENDMN $ENDDT "

# This is so that whether running 24 or 64 hrs, the icon for the next day is +24 hrs th (HHMMSS)
setenv NXDATE `python -c "import datetime;  datenum = datetime.datetime(${SRTYR}, ${SRTMN}, ${SRTDT}) + datetime.timedelta(days=1);                                       print(datenum.strftime('%Y%j'))"`
setenv NXTIME `python -c "import datetime;  datenum = datetime.datetime(${SRTYR}, ${SRTMN}, ${SRTDT}) + datetime.timedelta(days=1) + datetime.timedelta(hours=${NUMHRS}); print(datenum.strftime('%H').zfill(2).ljust(6,'0'))"`
setenv NXNDYR `python -c "import datetime;  datenum = datetime.datetime(${SRTYR}, ${SRTMN}, ${SRTDT}) + datetime.timedelta(days=1);                                       print(datenum.strftime('%Y'))"`
setenv NXNDMN `python -c "import datetime;  datenum = datetime.datetime(${SRTYR}, ${SRTMN}, ${SRTDT}) + datetime.timedelta(days=1);                                       print(datenum.strftime('%m').zfill(2))"`
setenv NXNDDT `python -c "import datetime;  datenum = datetime.datetime(${SRTYR}, ${SRTMN}, ${SRTDT}) + datetime.timedelta(days=1);                                       print(datenum.strftime('%d').zfill(2))"`
echo " next date / time: $NXDATE / $NXTIME : $NXNDMN $NXNDDT "

# Modification for running a second 24-hr MCIP from the same set of input WRF files 021413 JKV
# Need a new ending date, year, month, day for the new ending time. 
setenv EDATE2 `python -c "import datetime;  datenum = datetime.datetime(${ENDYR}, ${ENDMN}, ${ENDDT}) + datetime.timedelta(days=1);          print(datenum.strftime('%Y%j'))"`
setenv ETIME2 `python -c "import datetime;  datenum = datetime.datetime(${ENDYR}, ${ENDMN}, ${ENDDT}) + datetime.timedelta(hours=${NUMHRS}); print(datenum.strftime('%H').zfill(2).ljust(6,'0'))"`
setenv ENDYR2 `python -c "import datetime;  datenum = datetime.datetime(${ENDYR}, ${ENDMN}, ${ENDDT}) + datetime.timedelta(hours=${RUNLEN}); print(datenum.strftime('%Y'))"`
setenv ENDMN2 `python -c "import datetime;  datenum = datetime.datetime(${ENDYR}, ${ENDMN}, ${ENDDT}) + datetime.timedelta(hours=${RUNLEN}); print(datenum.strftime('%m').zfill(2))"`
setenv ENDDT2 `python -c "import datetime;  datenum = datetime.datetime(${ENDYR}, ${ENDMN}, ${ENDDT}) + datetime.timedelta(hours=${RUNLEN}); print(datenum.strftime('%d').zfill(2))"`
echo " next-next date / time: $EDATE2 / $ETIME2 : $ENDMN2 $ENDDT2 "

# Modification for identifying previous day date.  032613 JKV
setenv PDATE `python -c "import datetime;  datenum = datetime.datetime(${SRTYR}, ${SRTMN}, ${SRTDT}) + datetime.timedelta(days=-1);                                       print(datenum.strftime('%Y%j'))"`
setenv PTIME `python -c "import datetime;  datenum = datetime.datetime(${SRTYR}, ${SRTMN}, ${SRTDT}) + datetime.timedelta(days=-1) + datetime.timedelta(hours=${NUMHRS}); print(datenum.strftime('%H').zfill(2).ljust(6,'0'))"`
echo previous julian day PDATE: PTIME  $PDATE : $PTIME
setenv PRVYR `python -c "import datetime;  datenum = datetime.datetime(${SRTYR}, ${SRTMN}, ${SRTDT}) + datetime.timedelta(days=-1);                                       print(datenum.strftime('%Y'))"`
setenv PRVMN `python -c "import datetime;  datenum = datetime.datetime(${SRTYR}, ${SRTMN}, ${SRTDT}) + datetime.timedelta(days=-1);                                       print(datenum.strftime('%Y'))"`
setenv PRVDT `python -c "import datetime;  datenum = datetime.datetime(${SRTYR}, ${SRTMN}, ${SRTDT}) + datetime.timedelta(days=-1);                                       print(datenum.strftime('%Y'))"`
setenv PGDATE `python -c "import datetime;  datenum = datetime.datetime(${SRTYR}, ${SRTMN}, ${SRTDT}) + datetime.timedelta(days=-1);                                       print(datenum.strftime('%Y%m%d%H'))"`
echo "  previous gregorian day PGDATE: PTIME $PGDATE : $PTIME "
exit ( $exitstat )

