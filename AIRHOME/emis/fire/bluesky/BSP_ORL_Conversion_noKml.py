#!/usr/bin/python
#
# this converts BlueSky Pipeline info (fire_locations.csv) into ORL ptday SMOKE files for
# CMAQ inline fire plume rise
#
# This script uses lookups for most variables and calculates emissions based on lookup tables derived from BlueSky Legacy
# Docker script used to create fire_locations.csv pulls FCCS number, area, fire type, and coordinates.  
#
# This script expects a file_locations file that has persistence of many days for each fire.  Values for all dates are written to the ORL files while only current day is written to KML.

# Farren Herron-Thorpe 2020-08-29 Modified for BlueSky Pipeline
# Wei Zhang 2017-08-01 - used IEDQ method to calculate virtual heat and virtual area
# Farren Herron-Thorpe 2016-08-29
# Serena Chung 2016-03-18
# Rob Pinder 2013-06-24
# Note that this script divides heat by 3 to deal with the bug in SMOKE 3.5.1 which multiples heat x 3 when opening these ORL files for fire emissions.

import string
import csv
import math
import requests
import urllib
import operator
import os

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
ptinvfout = open('./ptinv.orl','w')
ptinvfout.write('#ORL FIRE\n')
ptinvfout.write('#TYPE Point Source Inventory for FIRES\n')
ptinvfout.write('#COUNTRY US\n')
ptinvfout.write('#YEAR 2020\n')
ptinvfout.write('#DATA ACRESBURNED HFLUX PM2_5 PM10 CO NH3 NOX SO2 VOC\n')
ptinvfout.write('#DESC FIPS,FIREID,LOCID,SCC,NAME,LAT,LON,NFDRSCODE,MATBURNED,HEATCONTENT\n')

#Create ptday file
ptdayfout = open('./ptday.orl','w')
ptdayfout.write('#ORL FIREEMIS\n')
ptdayfout.write('#TYPE    Day-specific Point Source Inventory for FIRES\n')
ptdayfout.write('#COUNTRY US\n')
ptdayfout.write('#YEAR 2020\n')
ptdayfout.write('#DATA ACRESBURNED HFLUX PM2_5 PM10 CO NH3 NOX SO2 VOC\n')
ptdayfout.write('#DESC FIPS,FIREID,LOCID,SCC,DATA,DATE,DATAVALUE,BEGHOUR,ENDHOUR\n')

#JKV_#Create the kml file.
#JKV_kmlf = open('fire_locations.kml', 'w')
#JKV_kmlf.write("<?xml version='1.0' encoding='UTF-8'?>\n")
#JKV_kmlf.write("<kml xmlns='http://earth.google.com/kml/2.1'>\n")
#JKV_kmlf.write("<Document>\n")
#JKV_kmlf.write('<Style id="pilefire">\n')
#JKV_kmlf.write("<BalloonStyle>\n")
#JKV_kmlf.write("    <text>$[description]</text>\n")
#JKV_kmlf.write("</BalloonStyle>\n")
#JKV_kmlf.write("<IconStyle>\n")
#JKV_kmlf.write("   <scale>0.5</scale>\n")
#JKV_kmlf.write("   <Icon>\n")
#JKV_kmlf.write("      <href>http://www.clker.com/cliparts/u/q/Y/q/p/9/saddleyerhorse-hi.png</href>\n")
#JKV_kmlf.write("   </Icon>\n")
#JKV_kmlf.write("</IconStyle>\n")
#JKV_kmlf.write("</Style>\n")
#JKV_kmlf.write('<Style id="agfire">\n')
#JKV_kmlf.write("<BalloonStyle>\n")
#JKV_kmlf.write("    <text>$[description]</text>\n")
#JKV_kmlf.write("</BalloonStyle>\n")
#JKV_kmlf.write("<IconStyle>\n")
#JKV_kmlf.write("   <scale>0.5</scale>\n")
#JKV_kmlf.write("   <Icon>\n")
#JKV_kmlf.write("      <href>http://www.clker.com/cliparts/v/t/e/M/1/Q/green-fire-hi.png</href>\n")
#JKV_kmlf.write("   </Icon>\n")
#JKV_kmlf.write("</IconStyle>\n")
#JKV_kmlf.write("</Style>\n")
#JKV_kmlf.write('<Style id="airfire">\n')
#JKV_kmlf.write("<BalloonStyle>\n")
#JKV_kmlf.write("    <text>$[description]</text>\n")
#JKV_kmlf.write("</BalloonStyle>\n")
#JKV_kmlf.write("<IconStyle>\n")
#JKV_kmlf.write("   <scale>0.5</scale>\n")
#JKV_kmlf.write("   <Icon>\n")
#JKV_kmlf.write("      <href>http://satepsanone.nesdis.noaa.gov/pub/FIRE/HMS/png_logo/FireIcon.png</href>\n")
#JKV_kmlf.write("   </Icon>\n")
#JKV_kmlf.write("</IconStyle>\n")
#JKV_kmlf.write("</Style>\n")
#JKV_kmlf.write('<Style id="rxfire">\n')
#JKV_kmlf.write("<BalloonStyle>\n")
#JKV_kmlf.write("    <text>$[description]</text>\n")
#JKV_kmlf.write("</BalloonStyle>\n")
#JKV_kmlf.write("<IconStyle>\n")
#JKV_kmlf.write("   <scale>0.5</scale>\n")
#JKV_kmlf.write("   <Icon>\n")
#JKV_kmlf.write("      <href>http://www.clker.com/cliparts/u/T/e/i/e/G/blue-flame-hi.png</href>\n")
#JKV_kmlf.write("   </Icon>\n")
#JKV_kmlf.write("</IconStyle>\n")
#JKV_kmlf.write("</Style>\n")
#JKV_kmlf.write("<name>" + 'fire_locations.kml' +"</name>\n")


#Emissions Lookfup for FCCS
WF_PM25dict = eval(open('./lookups/xwalk_WF_PM25_adduff.csv').read())
RX_PM25dict = eval(open('./lookups/xwalk_RX_PM25_adduff.csv').read())
WF_PM10dict = eval(open('./lookups/xwalk_WF_PM10_adduff.csv').read())
RX_PM10dict = eval(open('./lookups/xwalk_RX_PM10_adduff.csv').read())
WF_COdict   = eval(open('./lookups/xwalk_WF_CO_adduff.csv').read())
RX_COdict   = eval(open('./lookups/xwalk_RX_CO_adduff.csv').read())
WF_NOxdict = eval(open('./lookups/xwalk_WF_NOx_adduff.csv').read())
RX_NOxdict = eval(open('./lookups/xwalk_RX_NOx_adduff.csv').read())
WF_NH3dict = eval(open('./lookups/xwalk_WF_NH3_adduff.csv').read())
RX_NH3dict = eval(open('./lookups/xwalk_RX_NH3_adduff.csv').read())
WF_SO2dict = eval(open('./lookups/xwalk_WF_SO2_adduff.csv').read())
RX_SO2dict = eval(open('./lookups/xwalk_RX_SO2_adduff.csv').read())
WF_VOCdict = eval(open('./lookups/xwalk_WF_VOC_adduff.csv').read())
RX_VOCdict = eval(open('./lookups/xwalk_RX_VOC_adduff.csv').read())

WF_HEATdict = eval(open('./lookups/xwalk_WF_HEAT_adduff.csv').read())
RX_HEATdict = eval(open('./lookups/xwalk_RX_HEAT_adduff.csv').read())

#Using flaming consumption lookups
WF_CONSFdict = eval(open('./lookups/xwalk_WF_cons_flam.csv').read())
RX_CONSFdict = eval(open('./lookups/xwalk_RX_cons_flam.csv').read())

#Vegataion Names for FFCS
VEG_dict = eval(open('./lookups/fccs2_lookup.csv').read())

#locations = csv.DictReader(open('./fire_locations.csv'))
#Sorting the list puts in order of ID (not unique to location),latitude,longitude,date_time
locations_list = open('fire_locations.csv', 'r')
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
	FCCS_ID = row['fccs_number']
	type = row['type']

	VEG = VEG_dict[FCCS_ID]
	if int(month)>9:
		type = 'RX'
	if int(month)<5:
		type = 'RX'

	if location_id != previous_location:
		#Need to calculate FIPS
		params = urllib.parse.urlencode({'latitude': latitude, 'longitude': longitude, 'format':'json'})
		url = 'https://geo.fcc.gov/api/census/block/find?' + params
		response = requests.get(url)
		census_data = response.json()
		fips = census_data['County']['FIPS']
		print('FIPS query to geo.fcc.gov for ',latitude,longitude,' yielded ',fips)
		tmptype = type

		#Write out KML File
		if VEG == 'Agriculture or Developed':
			tmptype = 'Ag'

		fire_name = tmptype + ' Event'

#JKV_		if tmptype == 'Ag':
#JKV_			kmlf.write("   <Placemark>\n")
#JKV_			kmlf.write("       <name>" + fire_name + "</name>\n")
#JKV_			kmlf.write('           <description><![CDATA[<html lang="en"><b>Fire Assumptions:</b><br><br> ' + id + '<br><br>' + str(area) + ' acres <br><br>' + 'Fuel: ' + VEG + ' (possible Ag. burn)</html>]]></description>\n')
#JKV_			kmlf.write("           <styleUrl>#agfire</styleUrl>\n")  
#JKV_			kmlf.write("       <Point>\n")
#JKV_			kmlf.write("           <coordinates>" + str(longitude) + "," + str(latitude) + "," + str() + "</coordinates>\n")
#JKV_			kmlf.write("       </Point>\n")
#JKV_			kmlf.write("   </Placemark>\n")
#JKV_		if tmptype == 'WF':
#JKV_			kmlf.write("   <Placemark>\n")
#JKV_			kmlf.write("       <name>" + fire_name + "</name>\n")
#JKV_			kmlf.write('           <description><![CDATA[<html lang="en"><b>Fire Assumptions:</b><br><br> ' + id + '<br><br>' + str(area) + ' acres<br><br>' + 'Fuel: ' + VEG + '</html>]]></description>\n')
#JKV_			kmlf.write("           <styleUrl>#airfire</styleUrl>\n")  
#JKV_			kmlf.write("       <Point>\n")
#JKV_			kmlf.write("           <coordinates>" + str(longitude) + "," + str(latitude) + "," + str() + "</coordinates>\n")
#JKV_			kmlf.write("       </Point>\n")
#JKV_			kmlf.write("   </Placemark>\n")
#JKV_		if tmptype == 'RX':
#JKV_			kmlf.write("   <Placemark>\n")
#JKV_			kmlf.write("       <name>" + fire_name + "</name>\n")
#JKV_			kmlf.write('           <description><![CDATA[<html lang="en"><b>Fire Assumptions:</b><br><br> ' + id + '<br><br>' + str(area) + ' acres<br><br>' + 'Fuel: ' + VEG + '</html>]]></description>\n')
#JKV_			kmlf.write("           <styleUrl>#rxfire</styleUrl>\n")
#JKV_			kmlf.write("       <Point>\n")
#JKV_			kmlf.write("           <coordinates>" + str(longitude) + "," + str(latitude) + "," + str() + "</coordinates>\n")
#JKV_			kmlf.write("       </Point>\n")
#JKV_			kmlf.write("   </Placemark>\n")
           

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

#JKV_ kmlf.write("</Document>\n")
#JKV_ kmlf.write("</kml>\n")
#JKV_ kmlf.close()
ptinvfout.close()
ptdayfout.close()
