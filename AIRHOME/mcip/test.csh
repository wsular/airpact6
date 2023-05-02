#!/bin/csh

set SRTYR = 2022
set SRTMN = 10
set SRTDT = 12
set SRTHR = 00

set DATENUM = `python -c "import datetime; print(datetime.datetime(${SRTYR}, ${SRTMN}, ${SRTDT}, ${SRTHR}).strftime('%Y%j'))"`
echo ${DATENUM}


