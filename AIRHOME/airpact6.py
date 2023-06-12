import os
import time
import subprocess
from datetime import datetime, timedelta
import logging

class AIRPACT6:

    def __init__(self):        
        # ....Forecast settings
        self.numberOfForecastDays = 3
        self.forecastDays = range(self.numberOfForecastDays)
        
        # ....Current Forecast Day
#        dn = datetime(2023, 1, 7, 0, 0, 0)
        dn = datetime.utcnow().date()
        self.year    = dn.year
        self.month   = dn.month
        self.day     = dn.day
        self.datenum = datetime(dn.year, dn.month, dn.day)
        self.datestr = self.datenum.strftime('%Y%m%d')
        
        # ....Local Computer settings
        self.AIRHOME = '/home/airpact/airpact6/AIRHOME/'
        self.AIRRUN  = '/home/airpact/airpact6/AIRRUN/'
        self.AIRLOG  = '/home/airpact/airpact6/AIRRUN/logs/'
        self.WRF     = '/home/airpact/airpact6/AIRRUN/input/UW_WRF/'
        self.domain  = '/home/airpact/airpact6/AIRRUN/input/domain/'
        
        # ....UW WRF settings
        self.wrf_user = 'empact'
        self.wrf_host = 'rainier.atmos.washington.edu'
        self.wrf_data = '/home/disk/rainier_mm5rt/data/'
        #    Hours of UW WRF forecasts that are stored for WSU AIRPACT
        self.wrf_beghour  = 7
        self.wrf_endhour  = 82
        #    Forecast start hour; STTIME (start time)
        self.wrf_fcsthour = 8
        #    Forecast length in hours
        self.wrf_fcstlen  = 24

        # ....AIRPACT6 Log File
        logging.basicConfig(filename=self.AIRLOG + 'AIRPACT6_' + self.datestr + '.log', 
                            format='%(asctime)s, %(levelname)s, %(funcName)s, %(message)s', 
                            datefmt='%Y-%m-%d %H:%M:%S', 
                            encoding='utf-8', 
                            level=logging.DEBUG
                            )
        logging.info(f'Initialized AIRPACT6 forecast for {self.datestr}')
        return

    def readLog(self):
        """
        Simple function to store (and display) AIRPACT6 log file.
        """
        import pandas as pd
        log = pd.read_csv(f'{self.AIRLOG}AIRPACT6_{self.datestr}.log', names=['Local time', 'Level', 'Function', 'Message'], parse_dates=[0], header=None, index_col='Local time')
        return log

    def mcip(self):
        logging.info('Start')
        # ....Copy recent forecasts from UW WRF archive
        
        #    Check to see if all of the WRF files are available. Otherwise, log and wait...
        wrf_files = []
        while len(wrf_files) < 76:
            cmd = f'ls -1 /home/disk/rainier_mm5rt/data/{self.datestr}00'
            ls = subprocess.Popen(f"ssh {self.wrf_user}@{self.wrf_host} {cmd}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            wrf_files = ls[0].decode().split('\n')
            logging.warning(f'Waiting for UW WRF files... Currently {len(wrf_files)-1} available.')
            if len(wrf_files) < 76:
                time.sleep(5*60)   # Wait 5 minutes
        logging.info(f'UW WRF files are now available at {self.wrf_user}@{self.wrf_host}:{self.wrf_data}')

        downloadWRFfiles = f"scp -r {self.wrf_user}@{self.wrf_host}:{self.wrf_data}{self.datestr}00 {self.WRF}."
        os.system(downloadWRFfiles)
        logging.info('UW WRF files have been downloaded successfully.')

        # ....Run MCIP in CMAQ apptainer for each forecast day
        for forecastDay in self.forecastDays:
            
            # Determine the start and end times for MCIP conversion
            mcipStart = (self.datenum + timedelta(hours=(forecastDay*24)+self.wrf_fcsthour)).strftime('%Y%m%d%H')
            mcipEnd   = (self.datenum + timedelta(hours=((forecastDay+1)*24)+self.wrf_fcsthour)).strftime('%Y%m%d%H')
            
            # Determine the indices into the list of WRF files.
            offset = self.wrf_beghour - 1
            wrfStart = ((forecastDay * self.wrf_fcstlen) + self.wrf_fcsthour - 1) - offset
            wrfEnd  = ((forecastDay * self.wrf_fcstlen) + self.wrf_fcsthour + self.wrf_fcstlen + 1) - offset
            
            # Run MCIP in the apptainer
            runMCIP = f'apptainer exec --env-file {self.AIRHOME}AIRPACT6_env_vars /apptainer/cmaq/cmaq-5.3.3_ubuntu-22.04.sif {self.AIRHOME}mcip/run_mcip.csh {self.datestr} {mcipStart} {mcipEnd} {wrfStart} {wrfEnd}'
            os.system(runMCIP)
            logging.info(f'UW WRF files for {mcipStart} to {mcipEnd} have been converted to MCIP files.')

        logging.info('End')        
        return
    
    def bcon(self):
        logging.info('Start')
        
        # ....Download WACCM files from UCAR ACM
        for forecastDay in self.forecastDays:   # TODO: Download a 4th day of WACCM data for AIRPACT6 3rd day forecast
            waccm = f'wget -N --no-check-certificate https://www.acom.ucar.edu/waccm/DATA/f.e22.beta02.FWSD.f09_f09_mg17.cesm2_2_beta02.forecast.001.cam.h3.{self.year}-{self.month:02}-{self.day:02}-00000.nc'
            os.system(waccm)
            #ncks -d lat,39.,51. -d lon,233.,251.25   $waccmfile1  temp_waccm_1a.nc
            #ncks -F -d time,2,4                      temp_waccm_1a.nc temp_waccm_1.nc 
            #ncks -d lat,39.,51. -d lon,233.,251.25   $waccmfile2  temp_waccm_2.nc
            #ncks -d lat,39.,51. -d lon,233.,251.25   $waccmfile3  temp_waccm_3.nc
            #ncrcat  temp_waccm_1.nc temp_waccm_2.nc temp_waccm_3.nc $waccmfile
        # Run m3tshift; this might be a very simple step of changing STIME !!
        # Run Python script to convert variables from WACCM to CMAQ
        
        # ....
        logging.info('End')
        return

    def icon(self):
        logging.info('Start')
        logging.info('End')
        return

    def jproc(self):
        logging.info('Start')
        logging.info('End')
        return
    
    def anthro(self):
        logging.info('Start')
        # Get emissions inventories
        # Run SMOKE
        logging.info('End')
        return
        
    def megan(self):
        logging.info('Start')
        logging.info('End')
        return
    
    def bluesky(self):
        logging.info('Start')
        yesterday = (self.datenum - timedelta(days=1)).strftime('%Y-%m-%d')
        runBlueSky = """apptainer exec /apptainer/bluesky/bluesky_v4.3.56.sif bsp -n -J load.sources='[{"name": "firespider", "format": "JSON","type": "API", "endpoint":  "https://airfire-data-exports.s3-us-west-2.amazonaws.com/fire-spider/v3/fireinfosystem-v4-dropouts-persisted-mean-area/""" + yesterday + """.json"}]' -B skip_failed_fires=true -B fuelbeds.skip_failures=true -o """ + self.AIRHOME + """emis/fire/bluesky/output.json -C extrafiles.dest_dir=""" + self.AIRHOME + """emis/fire/bluesky/ -J extrafiles.sets='["firescsvs"]' load fuelbeds extrafiles"""
        os.system(runBlueSky)
        
        '''
                if ( ! -e $AIROUT/EMISSION/fire/bluesky/fire_locations.csv ) then
          echo "No Fires From BlueSky Pipeline Found"
          echo "How do we arrive here?"
                 exit(0)
        else
          echo "BlueSky Pipeline Fire Locations Found"
          cp $AIROUT/EMISSION/fire/bluesky/fire_locations.csv ~airpact5/AIRHOME/run_ap5_day1/emis/fire_new/fire_locations.csv
 
          python3.8 BSP_ORL_Conversion.py

          mv fire_locations.kml $TARGET_DIR/fire_locations_${YMD}.kml
          mv ptday.orl $TARGET_DIR/ptday-${YMD}00.orl
          mv ptinv.orl $TARGET_DIR/ptinv-${YMD}00.orl
          rm -f fire_locations.csv fire_locations_fips.csv
        '''
        
        logging.info('End')
        return
    
    def emis_merge(self):
        logging.info('Start')
        # TODO: Temporarily just copy the merged files from aeolus (for CCTM testing!!)
        logging.info('End')
        return
         
        return    

    def cctm(self):
        logging.info('Start')
        logging.info('End')
        return

    def plotting(self):
        logging.info('Start')
        # TODO: This might include plot_noncctm, plot_bcon, plot_cctm
        logging.info('End')
        return
