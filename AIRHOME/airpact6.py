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

    def read_log(self):
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
        
        def BSP_ORL_Conversion():
            '''
            # this converts BlueSky Pipeline info (fire_locations.csv) into ORL ptday SMOKE files for
            # CMAQ inline fire plume rise
            #
            # This script uses lookups for most variables and calculates emissions based on lookup tables derived from BlueSky Legacy.

            # Docker script used to create fire_locations.csv pulls FCCS number, area, fire type, and coordinates.  

            # This script expects a file_locations file that has persistence of many days for each fire.  Values for all dates are written to the ORL files while only current day is written to KML.

            # Farren Herron-Thorpe 2020-08-29 Modified for BlueSky Pipeline
            # Wei Zhang 2017-08-01 - used IEDQ method to calculate virtual heat and virtual area
            # Farren Herron-Thorpe 2016-08-29
            # Serena Chung 2016-03-18
            # Rob Pinder 2013-06-24
            # Note that this script divides heat by 3 to deal with the bug in SMOKE 3.5.1 which multiples heat x 3 when opening these ORL files for fire emissions.
            '''
            import string
            import csv
            import math
            import operator
            import os
            import pandas
            import geopandas
            from geopandas import GeoDataFrame
            from shapely.geometry import Point

            counties = geopandas.read_file(self.AIRHOME + "emis/fire/bluesky/counties.shp")
            locations_temp = pandas.read_csv(self.AIRHOME + "emis/fire/bluesky/fire_locations.csv")
            locations_gdf = GeoDataFrame(locations_temp,crs='EPSG:4269',geometry=[Point(xy) for xy in zip(locations_temp.longitude, locations_temp.latitude)])
            joined = geopandas.sjoin(locations_gdf,counties,how="inner",op='intersects')
            joined.to_csv(self.AIRHOME + 'emis/fire/bluesky/fire_locations_fips.csv')


            # calculate plume class based on DEASCO3
            def getPlumeClass(flame_consumption, area):
                fpci = flame_consumption / math.sqrt(area)
                if fpci <= 75:
                    return 1
                elif fpci <= 300:
                    return 2
                elif fpci <= 675:
                    return 3
                elif fpci <= 1250:
                    return 4
                else:
                    return 5
                
            #Start Main Body     
            layer1Fracts = { }
            layer1Fracts[1] = 0.711
            layer1Fracts[2] = 0.572
            layer1Fracts[3] = 0.467
            layer1Fracts[4] = 0.467
            layer1Fracts[5] = 0.467

            # Create ptinv file
            ptinvfout = open(self.AIRHOME+'emis/fire/bluesky/ptinv.orl','w')
            ptinvfout.write('#ORL FIRE\n')
            ptinvfout.write('#TYPE Point Source Inventory for FIRES\n')
            ptinvfout.write('#COUNTRY US\n')
            ptinvfout.write('#YEAR 2020\n')
            ptinvfout.write('#DATA ACRESBURNED HFLUX PM2_5 PM10 CO NH3 NOX SO2 VOC\n')
            ptinvfout.write('#DESC FIPS,FIREID,LOCID,SCC,NAME,LAT,LON,NFDRSCODE,MATBURNED,HEATCONTENT\n')

            #Create ptday file
            ptdayfout = open(self.AIRHOME+'emis/fire/bluesky/ptday.orl','w')
            ptdayfout.write('#ORL FIREEMIS\n')
            ptdayfout.write('#TYPE    Day-specific Point Source Inventory for FIRES\n')
            ptdayfout.write('#COUNTRY US\n')
            ptdayfout.write('#YEAR 2020\n')
            ptdayfout.write('#DATA ACRESBURNED HFLUX PM2_5 PM10 CO NH3 NOX SO2 VOC\n')
            ptdayfout.write('#DESC FIPS,FIREID,LOCID,SCC,DATA,DATE,DATAVALUE,BEGHOUR,ENDHOUR\n')

            #Create the kml file.
            kmlf = open(self.AIRHOME+'emis/fire/bluesky/fire_locations.kml', 'w')
            kmlf.write("<?xml version='1.0' encoding='UTF-8'?>\n")
            kmlf.write("<kml xmlns='http://earth.google.com/kml/2.1'>\n")
            kmlf.write("<Document>\n")
            kmlf.write('<Style id="pilefire">\n')
            kmlf.write("<BalloonStyle>\n")
            kmlf.write("    <text>$[description]</text>\n")
            kmlf.write("</BalloonStyle>\n")
            kmlf.write("<IconStyle>\n")
            kmlf.write("   <scale>0.5</scale>\n")
            kmlf.write("   <Icon>\n")
            kmlf.write("      <href>http://www.clker.com/cliparts/u/q/Y/q/p/9/saddleyerhorse-hi.png</href>\n")
            kmlf.write("   </Icon>\n")
            kmlf.write("</IconStyle>\n")
            kmlf.write("</Style>\n")
            kmlf.write('<Style id="agfire">\n')
            kmlf.write("<BalloonStyle>\n")
            kmlf.write("    <text>$[description]</text>\n")
            kmlf.write("</BalloonStyle>\n")
            kmlf.write("<IconStyle>\n")
            kmlf.write("   <scale>0.5</scale>\n")
            kmlf.write("   <Icon>\n")
            kmlf.write("      <href>http://www.clker.com/cliparts/v/t/e/M/1/Q/green-fire-hi.png</href>\n")
            kmlf.write("   </Icon>\n")
            kmlf.write("</IconStyle>\n")
            kmlf.write("</Style>\n")
            kmlf.write('<Style id="airfire">\n')
            kmlf.write("<BalloonStyle>\n")
            kmlf.write("    <text>$[description]</text>\n")
            kmlf.write("</BalloonStyle>\n")
            kmlf.write("<IconStyle>\n")
            kmlf.write("   <scale>0.5</scale>\n")
            kmlf.write("   <Icon>\n")
            kmlf.write("      <href>http://satepsanone.nesdis.noaa.gov/pub/FIRE/HMS/png_logo/FireIcon.png</href>\n")
            kmlf.write("   </Icon>\n")
            kmlf.write("</IconStyle>\n")
            kmlf.write("</Style>\n")
            kmlf.write('<Style id="rxfire">\n')
            kmlf.write("<BalloonStyle>\n")
            kmlf.write("    <text>$[description]</text>\n")
            kmlf.write("</BalloonStyle>\n")
            kmlf.write("<IconStyle>\n")
            kmlf.write("   <scale>0.5</scale>\n")
            kmlf.write("   <Icon>\n")
            kmlf.write("      <href>http://www.clker.com/cliparts/u/T/e/i/e/G/blue-flame-hi.png</href>\n")
            kmlf.write("   </Icon>\n")
            kmlf.write("</IconStyle>\n")
            kmlf.write("</Style>\n")
            kmlf.write("<name>" + 'fire_locations.kml' +"</name>\n")


            #Emissions Lookfup for FCCS
            WF_PM25dict = eval(open(self.AIRHOME+'emis/fire/bluesky/lookups/xwalk_WF_PM25_adduff.csv').read())
            RX_PM25dict = eval(open(self.AIRHOME+'emis/fire/bluesky/lookups/xwalk_RX_PM25_adduff.csv').read())
            WF_PM10dict = eval(open(self.AIRHOME+'emis/fire/bluesky/lookups/xwalk_WF_PM10_adduff.csv').read())
            RX_PM10dict = eval(open(self.AIRHOME+'emis/fire/bluesky/lookups/xwalk_RX_PM10_adduff.csv').read())
            WF_COdict   = eval(open(self.AIRHOME+'emis/fire/bluesky/lookups/xwalk_WF_CO_adduff.csv').read())
            RX_COdict   = eval(open(self.AIRHOME+'emis/fire/bluesky/lookups/xwalk_RX_CO_adduff.csv').read())
            WF_NOxdict  = eval(open(self.AIRHOME+'emis/fire/bluesky/lookups/xwalk_WF_NOx_adduff.csv').read())
            RX_NOxdict  = eval(open(self.AIRHOME+'emis/fire/bluesky/lookups/xwalk_RX_NOx_adduff.csv').read())
            WF_NH3dict  = eval(open(self.AIRHOME+'emis/fire/bluesky/lookups/xwalk_WF_NH3_adduff.csv').read())
            RX_NH3dict  = eval(open(self.AIRHOME+'emis/fire/bluesky/lookups/xwalk_RX_NH3_adduff.csv').read())
            WF_SO2dict  = eval(open(self.AIRHOME+'emis/fire/bluesky/lookups/xwalk_WF_SO2_adduff.csv').read())
            RX_SO2dict  = eval(open(self.AIRHOME+'emis/fire/bluesky/lookups/xwalk_RX_SO2_adduff.csv').read())
            WF_VOCdict  = eval(open(self.AIRHOME+'emis/fire/bluesky/lookups/xwalk_WF_VOC_adduff.csv').read())
            RX_VOCdict  = eval(open(self.AIRHOME+'emis/fire/bluesky/lookups/xwalk_RX_VOC_adduff.csv').read())

            WF_HEATdict = eval(open(self.AIRHOME+'emis/fire/bluesky/lookups/xwalk_WF_HEAT_adduff.csv').read())
            RX_HEATdict = eval(open(self.AIRHOME+'emis/fire/bluesky/lookups/xwalk_RX_HEAT_adduff.csv').read())

            #Using flaming consumption lookups
            WF_CONSFdict = eval(open(self.AIRHOME+'emis/fire/bluesky/lookups/xwalk_WF_cons_flam.csv').read())
            RX_CONSFdict = eval(open(self.AIRHOME+'emis/fire/bluesky/lookups/xwalk_RX_cons_flam.csv').read())

            #Vegataion Names for FFCS
            VEG_dict = eval(open(self.AIRHOME+'emis/fire/bluesky/lookups/fccs2_lookup.csv').read())

            #locations = csv.DictReader(open('./fire_locations.csv'))
            #Sorting the list puts in order of ID (not unique to location),latitude,longitude,date_time
            locations_list = open(self.AIRHOME+'emis/fire/bluesky/fire_locations_fips.csv', 'r')
            locations_unsorted = csv.DictReader(locations_list)
            locations = sorted(locations_unsorted, key=operator.itemgetter('id', 'latitude'))

            previous_location = 'none'

            for row in locations:

                date_time = row['date_time']
                year = date_time[2:4]
                month = date_time[4:6]
                day = date_time[6:8]
                fire_date = month + '/' + day + '/' + year
                latitude = row['latitude']
                longitude = row['longitude']       
                location_id = latitude + longitude
                SFid = row['id']
                id = SFid[31:62]
                area = round(float(row['area'])/3)
                NFDRSCODE = '-9'
                FCCS_ID = str(int(float(row['fccs_number'])))
                type = row['type']
                fips = row['GEOID']
                VEG = VEG_dict[FCCS_ID]
                if int(month)>9:
                    type = 'RX'
                if int(month)<5:
                    type = 'RX'

                if location_id != previous_location:
                    tmptype = type
                    #Write out KML File
                    if VEG == 'Agriculture or Developed':
                        tmptype = 'Ag'

                    fire_name = tmptype + ' Event'

                    if tmptype == 'Ag':
                        kmlf.write("   <Placemark>\n")
                        kmlf.write("       <name>" + fire_name + "</name>\n")
                        kmlf.write('           <description><![CDATA[<html lang="en"><b>Fire Assumptions:</b><br><br> ' + id + '<br><br>' + str(area) + ' acres <br><br>' + 'Fuel: ' + VEG + ' (possible Ag. burn)</html>]]></description>\n')
                        kmlf.write("           <styleUrl>#agfire</styleUrl>\n")  
                        kmlf.write("       <Point>\n")
                        kmlf.write("           <coordinates>" + str(longitude) + "," + str(latitude) + "," + str() + "</coordinates>\n")
                        kmlf.write("       </Point>\n")
                        kmlf.write("   </Placemark>\n")
                    if tmptype == 'WF':
                        kmlf.write("   <Placemark>\n")
                        kmlf.write("       <name>" + fire_name + "</name>\n")
                        kmlf.write('           <description><![CDATA[<html lang="en"><b>Fire Assumptions:</b><br><br> ' + id + '<br><br>' + str(area) + ' acres<br><br>' + 'Fuel: ' + VEG + '</html>]]></description>\n')
                        kmlf.write("           <styleUrl>#airfire</styleUrl>\n")  
                        kmlf.write("       <Point>\n")
                        kmlf.write("           <coordinates>" + str(longitude) + "," + str(latitude) + "," + str() + "</coordinates>\n")
                        kmlf.write("       </Point>\n")
                        kmlf.write("   </Placemark>\n")
                    if tmptype == 'RX':
                        kmlf.write("   <Placemark>\n")
                        kmlf.write("       <name>" + fire_name + "</name>\n")
                        kmlf.write('           <description><![CDATA[<html lang="en"><b>Fire Assumptions:</b><br><br> ' + id + '<br><br>' + str(area) + ' acres<br><br>' + 'Fuel: ' + VEG + '</html>]]></description>\n')
                        kmlf.write("           <styleUrl>#rxfire</styleUrl>\n")
                        kmlf.write("       <Point>\n")
                        kmlf.write("           <coordinates>" + str(longitude) + "," + str(latitude) + "," + str() + "</coordinates>\n")
                        kmlf.write("       </Point>\n")
                        kmlf.write("   </Placemark>\n")
                    

                previous_location = location_id

                    #The WF and RX heat scale is non-linear, so the derived lookups are given below (within +/- 10% of BlueSky)
                if area >= 1001:
                        WFhs = 149
                        RXhs = 145
                if area < 1001:
                        WFhs = 129
                        RXhs = 145
                if area < 801:
                        WFhs = 120
                        RXhs = 123
                if area < 601:
                        WFhs = 99
                        RXhs = 96
                if area < 451:
                        WFhs = 74
                        RXhs = 77
                if area < 301:
                        WFhs = 56
                        RXhs = 64
                if area < 201:
                        WFhs = 45
                        RXhs = 56
                if area < 81:
                        WFhs = 40
                        RXhs = 48
                    #Lookup flaming consumption and heat
                if type == 'WF':
                            conf = float(WF_CONSFdict[FCCS_ID])
                            heat = area * WFhs * float(WF_HEATdict[FCCS_ID])
                    
                if type == 'RX':          
                            conf = float(RX_CONSFdict[FCCS_ID])
                            heat = area * RXhs * float(RX_HEATdict[FCCS_ID])
                    # generate virtual area and virtual heat
                    # virtual area is based on layer 1 fraction from WRAP/DEASCO3 and smoldering fraction formula in SMOKE
                flame_consumption = conf * area
                plume_class = getPlumeClass(flame_consumption, area)
                s_fract = layer1Fracts[plume_class]     
                virtual_area_layer1Fract = math.exp((1 - 0.3 - s_fract) / 0.0703)
                ## virtual_heat_layer1Fract_3 : 
                ## inspired by DEASCO3 Flaming Phase Consumption Index equation
                ## [virtual heat content] = [maximum flaming phase heat] / [square root of area]
                ## [maximum flaming phase heat] = consumption (tons/acre) * Area(Acres) * 16,000,000 (BTU/Ton)
                maximum_heat = conf  * area * 16000000
                virtual_heat_layer1Fract_3 = maximum_heat / math.sqrt(area)

                ## virtual_heat_layer1Fract_4 : 
                ## produce virtual heat content as follows 
                ## 1. area >=1001,  [Maximum flaming phase Heat] / [Square root of area]
                ## 2. area <= 1, [Maximum flaming Heat]
                ## 3. area between 1 and 1001, linear scale gradually from ([Maximum flaming phase Heat] / [Square root of area]) to ([Maximum flaming Heat])
                virtual_heat_layer1Fract_4 = 0
                if area < 1001:
                    virtual_heat_layer1Fract_4 = virtual_heat_layer1Fract_3 + (maximum_heat - virtual_heat_layer1Fract_3) * (1001.0 - area) / 1000.0
                else:
                    virtual_heat_layer1Fract_4 = virtual_heat_layer1Fract_3

                ## reduce heat by 3 times to compensate a bug in SMOKE (smkinven) process for SMOKE 3.5.1 (confirmed by SMOKE developer)
                virtual_heat = virtual_heat_layer1Fract_4 / 3.0
                virtual_area = virtual_area_layer1Fract	
                    
                material_burned = 0

                if type == 'WF':
                        scc = '2810001000'
                        PM25_emis = str(format(area * float(WF_PM25dict[FCCS_ID]),'.3f'))
                        PM10_emis = str(format(area * float(WF_PM10dict[FCCS_ID]),'.3f'))
                        CO_emis   = str(format(area * float(WF_COdict[FCCS_ID]),'.3f'))
                        NOx_emis  = str(format(area * float(WF_NOxdict[FCCS_ID]),'.3f'))
                        NH3_emis  = str(format(area * float(WF_NH3dict[FCCS_ID]),'.3f'))
                        SO2_emis  = str(format(area * float(WF_SO2dict[FCCS_ID]),'.3f'))
                        VOC_emis  = str(format(area * float(WF_VOCdict[FCCS_ID]),'.3f'))
                        area = virtual_area #Doing this after emissions are calculated so only plume rise is affected
                        heat = virtual_heat
                        area_str  = str(format(virtual_area,'.3f'))
                        heat_str  = str(format(virtual_heat,'.3f'))        
                if type == 'RX':
                        scc = '2810015000'
                    #   Un-comment out this section to use BlueSky emissions
                    #   PM25_emis = str(format(area * float(RX_PM25dict[FCCS_ID]),'.3f'))
                    #   PM10_emis = str(format(area * float(RX_PM10dict[FCCS_ID]),'.3f'))
                    #   CO_emis   = str(format(area * float(RX_COdict[FCCS_ID]),'.3f'))
                    #   NOx_emis  = str(format(area * float(RX_NOxdict[FCCS_ID]),'.3f'))
                    #   NH3_emis  = str(format(area * float(RX_NH3dict[FCCS_ID]),'.3f'))
                    #   SO2_emis  = str(format(area * float(RX_SO2dict[FCCS_ID]),'.3f'))
                    #   VOC_emis  = str(format(area * float(RX_VOCdict[FCCS_ID]),'.3f'))
                    #   area = virtual_area #Doing this after emissions are calculated so only plume rise is affected
                    #   heat = virtual_heat
                    #   area_str  = str(format(virtual_area,'.3f'))
                    #   heat_str  = str(format(virtual_heat,'.3f'))  
                    #Emission factors assume 200 tons of pile burning per 46 acres reported by SMARTFIRE
                        PM25_emis = str(format(area * 0.024,'.3f'))
                        PM10_emis = str(format(area * 0.028,'.3f'))
                        CO_emis   = str(format(area * 0.138,'.3f'))
                        NOx_emis  = str(format(area * 0.007,'.3f'))
                        NH3_emis  = str(format(area * 0.0001,'.3f'))
                        SO2_emis  = str(format(area * 0.0002,'.3f'))
                        VOC_emis  = str(format(area * 0.03,'.3f'))
                        area_str  = str(format(1,'.3f')) #setting pile burns to area of 1 acre so smoldering fraction is very low
                        heat_str  = str(format(maximum_heat,'.3f'))
                    
                beginHour = 0
                endHour = 23                

                lineOut = '"%s", "%s", "%s", "%s", "%s", %s, %s, "%s", %s, %s\n' % (fips, id, location_id, scc, VEG, latitude, longitude, NFDRSCODE, material_burned, virtual_heat)
                ptinvfout.write(lineOut)
                    
                lineOut = '"%s", "%s", "%s", "%s", "%s", "%s", %s, %s, %s\n' % (fips, id, location_id, scc, 'PM2_5', fire_date, PM25_emis, beginHour, endHour)
                ptdayfout.write(lineOut)
                lineOut = '"%s", "%s", "%s", "%s", "%s", "%s", %s, %s, %s\n' % (fips, id, location_id, scc, 'PM10', fire_date, PM10_emis, beginHour, endHour)
                ptdayfout.write(lineOut)
                lineOut = '"%s", "%s", "%s", "%s", "%s", "%s", %s, %s, %s\n' % (fips, id, location_id, scc, 'CO', fire_date, CO_emis, beginHour, endHour)
                ptdayfout.write(lineOut)
                lineOut = '"%s", "%s", "%s", "%s", "%s", "%s", %s, %s, %s\n' % (fips, id, location_id, scc, 'NH3', fire_date, NH3_emis, beginHour, endHour)
                ptdayfout.write(lineOut)
                lineOut = '"%s", "%s", "%s", "%s", "%s", "%s", %s, %s, %s\n' % (fips, id, location_id, scc, 'NOX', fire_date, NOx_emis, beginHour, endHour)
                ptdayfout.write(lineOut)
                lineOut = '"%s", "%s", "%s", "%s", "%s", "%s", %s, %s, %s\n' % (fips, id, location_id, scc, 'SO2', fire_date, SO2_emis, beginHour, endHour)
                ptdayfout.write(lineOut)
                lineOut = '"%s", "%s", "%s", "%s", "%s", "%s", %s, %s, %s\n' % (fips, id, location_id, scc, 'VOC', fire_date, VOC_emis, beginHour, endHour)
                ptdayfout.write(lineOut)
                lineOut = '"%s", "%s", "%s", "%s", "%s", "%s", %s, %s, %s\n' % (fips, id, location_id, scc, 'HFLUX', fire_date, heat_str, beginHour, endHour)
                ptdayfout.write(lineOut)
                lineOut = '"%s", "%s", "%s", "%s", "%s", "%s", %s, %s, %s\n' % (fips, id, location_id, scc, 'ACRESBURNED', fire_date, area_str, beginHour, endHour)
                ptdayfout.write(lineOut)

            kmlf.write("</Document>\n")
            kmlf.write("</kml>\n")
            kmlf.close()
            ptinvfout.close()
            ptdayfout.close()
            
            return
       
        logging.info('Start')
        yesterday = (self.datenum - timedelta(days=1)).strftime('%Y-%m-%d')
        runBlueSky = """apptainer exec /apptainer/bluesky/bluesky_v4.3.56.sif bsp -n -J load.sources='[{"name": "firespider", "format": "JSON","type": "API", "endpoint":  "https://airfire-data-exports.s3-us-west-2.amazonaws.com/fire-spider/v3/fireinfosystem-v4-dropouts-persisted-mean-area/""" + yesterday + """.json"}]' -B skip_failed_fires=true -B fuelbeds.skip_failures=true -o """ + self.AIRHOME + """emis/fire/bluesky/output.json -C extrafiles.dest_dir=""" + self.AIRHOME + """emis/fire/bluesky/ -J extrafiles.sets='["firescsvs"]' load fuelbeds extrafiles"""
        os.system(runBlueSky)
        
        # ....Log status of bluesky run
        from glob import glob
        if not glob(self.AIRHOME+'emis/fire/bluesky/fire_locations.csv'):
            logging.info('NO fires From BlueSky Pipeline found.')
        else:
            logging.info('Fires From BlueSky Pipeline found.')
        
        '''
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
