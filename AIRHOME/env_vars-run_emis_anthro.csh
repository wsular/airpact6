#!/bin/csh -f

set YEAR = 2024
set MONTH = 12
set DAY = 16
set currentday = $YEAR$MONTH$DAY
set previousday = `date -d "$currentday -1 days" '+%Y%m%d'`
set twodaysago  = `date -d "$currentday -2 days" '+%Y%m%d'`
set NHR   = 24

setenv AIRHOME   /mnt/disk2/airpact/airpact6/amin_mirror/AIRHOME
set AIRRUN = /mnt/disk2/airpact/airpact6/amin_mirror/AIRRUN/$YEAR
setenv AIROUT    $AIRRUN/${currentday}00
setenv AIRLOGDIR $AIROUT/logs
setenv MCIPROOT  $AIROUT
setenv MCIPDIR   $MCIPROOT/${currentday}00/MCIP37

setenv SMK_HOME /mnt/disk2/airpact/models/SMOKE/v5.1

setenv YYYYMMDD $currentday
setenv EMIS_WORKDIR $AIRHOME/run_ap6_day1/emis

set logdir = $AIRLOGDIR/emis/anthro
if ( ! -d $logdir ) mkdir -p $logdir

#${EMIS_WORKDIR}/anthro/temporal/run_smk_temporal_gaia.csh $currentday 24  >&! $logdir/run_emis_anthro.log
${EMIS_WORKDIR}/anthro/temporal/run_smk_temporal_gaia.csh $currentday 24
