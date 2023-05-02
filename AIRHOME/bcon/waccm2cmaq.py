#/usr/bin/python

# coding: utf-8

# # PYTHON CODE FOR EXTRACTING AIRPACT5 BCON FROM WACCM FILES

# # SECTION 1 set up modules

# SET UP MODULES

# I want true division in python 2.* so I added this.
from __future__ import division # tested by # testx = 1/2 ; print testx # got: 0.5 # OK

import sys
import netCDF4
from netCDF4 import Dataset
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
from mpl_toolkits.basemap import Basemap
import cartopy.crs as crs
import cartopy.feature as cfeature
from glob import glob
import numpy as np
import pandas as pd
import scipy as sc
#from scipy.stats.stats import pearsonr 
#from scipy import constants
from scipy.constants import *
# print "The molar gas constant R:", R
import xarray as xr
import matplotlib as mpl
import os.path 
#from time import time
import time

mpl.rcParams['xtick.labelsize'] = 15 #seems like this would go in plotting SECTION
mpl.rcParams['ytick.labelsize'] = 15

# FOR ZERO-PADDING NUMBERS
# a lambda function to convert month/day/hour to a string of length 2
len2char = lambda x:('0'+str(x) if len(str(x))<2 else str(x))


#CONSTANTS
print sc.pi  
print "The molar gas constant R:", R, "(m3 Pa)/(mol K)"
print "Avagodro's Number:", N_A
amm = air_molar_mass = 28.966
print "Air Molar Mass:", amm, " g"
n = moles_air_in_kg = 1000.0 / amm
print "Moles per Kg air:", n
NH4_mol_wt = 18.039
print "NH4 mol. wt.:",NH4_mol_wt

FALSE = 0
TRUE = 1

dir(Dataset.sync)

print "SECTION 1 COMPLETED SET UP "

# # SECTION 2 fake in command line inputs

print "SECTION 2 DATE READ AND INTERPRETED "

YYYYMMDD = sys.argv[1]
print "DATE READ FROM sys.argv[1]:", YYYYMMDD

### FAKING COMMAND LINE INPUTS TO SCRIPT HERE for now...
# user input could come from command line or qsub arguments but can test by setting here
# access arguments as sys.argv[1]
year  = YYYYMMDD[0:4]
month = YYYYMMDD[4:6]
day   = YYYYMMDD[6:8]
#year  = 2018
#month = 7
#day   = 25
#time_units_long = 'days since 2018-07-23 00:00:00' # WACCM
#time_units_short = '2018-07-23 00:00:00'
# and string forms needed
y = str(year)
m = len2char(month)
d = len2char(day)
#m = str(month).zfill(2)
#d = str(day).zfill(2)
#print (time_units_long)
print " YEAR: ", y
print " MONTH: ", m
print " DAY:  ", d

# EXAMPLE of method call for method listed by last cell execution of dir(waccm_file)
#WHY is captialize a method for the full path that begins with a '/'?  
#Because it is a string.
a='alpha'
print a.isalpha()
#help mcip_bdyfile.capitalize()


# # SECTION 3 READ IN AND CHECK MCIP FOR BCON
print "SECTION 3 READ IN AND CHECK MCIP FOR BCON"

# MCIP FILES WITH DATA LOCATING AND DECRIBING THE AIRPACT5 DOMAIN BOUNDARY ARE NEEDED
# MCIP boundary files set up
# file locations: AIRPACT5 MCIP37 files for boundary
runroot = "/data/lar/projects/airpact5/AIRRUN/{y}/{y}{m}{d}00".format(m=m, y=y, d=d)
mcip_dir = runroot + "/MCIP37/"
print (mcip_dir)
mcip_bdyfile = mcip_dir + "GRIDBDY2D"
mcip_metfile = mcip_dir + "METBDY3D"
print (mcip_bdyfile)
print (mcip_metfile)

#read in BCON grid file for boundary
bcongrid = Dataset(mcip_bdyfile) 
dir(bcongrid)
print bcongrid.file_format 
print bcongrid.dimensions.keys() 
print bcongrid.dimensions['TSTEP']
print bcongrid.dimensions['DATE-TIME'] 
print bcongrid.dimensions['LAY'] 
print bcongrid.dimensions['VAR']
print bcongrid.dimensions['PERIM'] 
perim_size = bcongrid.dimensions['PERIM'].size 
perim_max = bcongrid.dimensions['PERIM'].size - 1
print( 'Perim max =', perim_max) 
#print attr, '=', getattr(bcongrid, attr)
bcon_lat = bcongrid.variables['LAT'][0,0,:] # float LAT(TSTEP, LAY, PERIM) in GRIDBDY2D
bcon_lon = bcongrid.variables['LON'][0,0,:]
bcon_ht = bcongrid.variables['HT'][0,0,:]


#read in BCON MET file for boundary cell pressures PRES(TSTEP, LAY, PERIM)
bconmet = Dataset(mcip_metfile) 
#dir(bconmet)
print bconmet.file_format 
bconmet_vars = ["JACOBF","JACOBM","DENSA_J","WHAT_JD","TA","QV","PRES","DENS","ZH","ZF","QC","QR","QI","QS","QG","WWIND","CFRAC_3D"]  
bconmet_pres = bconmet.variables['PRES'][:,:,:] # float PRES(TSTEP, LAY, PERIM) in mcip file
print "bconmet_pres:", bconmet_pres[0,:,0]
bconmet_ntime = 25  # hours in METBDY3D
bconmet_nlev = 37


#PRINT BCON boundary bcon_lon and bcon_lat
print bcon_lat
print bcon_lon


#plt.plot(bcon_lon, bcon_lat, marker='X', color='red')
#_plt.show()
#plt.savefig('/data/lar/projects/airpact5/misc/WACCM_for_BCON/BCON_PLOTS/bcon_boundary_{y}{m}{d}00'.format(m=m, y=y, d=d)+'.png')
#print "BCON perimiter"


# 
#_plt.plot(bcon_lon[1:285], bcon_ht[1:285], marker='X', color='red')
#_plt.show()
#print "BCON ht along southern boundary [m]"


# 
#_plt.plot(bcon_lon[1:285], bconmet_pres[0,0,1:285], marker='X', color='blue')
#_plt.show()
#print "BCON Pressure along southern boundary [Pa]"


# 
#_plt.plot(bcon_lat[287:544], bcon_ht[287:544], marker='X', color='red')
#_plt.show()
#print "BCON ht along eastern boundary"


# 
#_plt.plot(bcon_lon[287:544], bconmet_pres[0,0,287:544], marker='X', color='blue')
#_plt.show()
#print "BCON Pressure along eastern boundary [Pa]"


# 
#_plt.plot(bcon_lon[546:830], bcon_ht[546:830], marker='X', color='red')
#_plt.show()
#print "BCON ht along northern boundary"


# 
#_plt.plot(bcon_lat[832:1089], bcon_ht[832:1089], marker='X', color='red')
#_plt.show()
#print "BCON ht along western boundary"


# # SECTION 4 READ IN AND REPORT ON WACCM DATA
print "SECTION 4 READ IN AND REPORT ON WACCM DATA "

# WACCM FILES FROM NCAR ARE SOURCE OF NEW GAS AND AEROSOL BOUNDARY CONDITIONS
# WACCM files are grabbed and prepared by cshell scripting.
# WACCM files set up file locations: WACCM files for boundary conditions input
waccm_file_dir = "/data/lar/projects/airpact5/misc/WACCM_for_BCON/"
waccm_file_name = 'waccm_forecast_{y}-{m}-{d}.nc'.format(m=m, y=y, d=d)
waccm_file = waccm_file_dir + waccm_file_name
print (waccm_file)
#dir(waccm_file) #dir gives __special methods__ and std methods for objects of this class


# 


# # Read in WACCM

#read in WACCM file for inputs for BCON
waccmgrid = Dataset(waccm_file) 
#print(waccmgrid)
#dir(waccmgrid)
#print waccmgrid.file_format 
#print waccmgrid.dimensions.keys() 
#print waccmgrid.dimensions['time'] 

waccmgrid.dimensions['time']
waccm_P0 = waccmgrid.variables['P0'][:]       # Reference Pressure, a single value, [Pa]
waccm_PS = np.float64(waccmgrid.variables['PS'][:,:,:]) # Surface Pressure (time, lat, lon) [Pa]
waccm_T = np.float64(waccmgrid.variables['T'][:,:,:,:]) # Temperature (time, lev, lat, lon) [K]
waccm_hyam = waccmgrid.variables['hyam'][:] # hybrid A coeff at layer midpoints (lev)
waccm_hybm = waccmgrid.variables['hybm'][:] # hybrid B coeff at layer midpoints (lev)
waccm_time = waccmgrid.variables['time'][:]
waccm_lev = waccmgrid.variables['lev'][:]
#print waccm_P0 
#print waccm_PS 
#print waccm_T  
#print waccm_hyam 
#print waccm_hybm
#print time
waccm_ntime = 10 # Timnes steps to process from WACCM
waccm_nlev = 88
waccm_nlat = 13
waccm_nlon = 15
waccm_nchars = 8
waccm_nilev = 89
waccm_nnbnd = 2
waccm_time
#dir(waccmgrid)


# WACCM numbers variable names
waccm_numbers = ['num_a1', 'num_a2', 'num_a3']  # WACCM file contains no 'num_a4'
for number in waccm_numbers:
    print number # this lists each aerosol name
#waccm_(aerosol) = np.float64(waccmgrid.variables[aerosol][:,:,:,:])


# WACCM aerosols variable names
waccm_aerosols = ['bc_a1', 'bc_a4', 'dst_a1', 'dst_a2', 'dst_a3', 'ncl_a1', 'ncl_a2', 'ncl_a3', 'pom_a1', 'pom_a4', 
    'so4_a1', 'so4_a2', 'so4_a3', 'soa1_a1', 'soa1_a2', 'soa2_a1', 'soa2_a2', 'soa3_a1', 'soa3_a2', 'soa4_a1', 
    'soa4_a2', 'soa5_a1', 'soa5_a2']
for aerosol in waccm_aerosols:
    print aerosol # this lists each aerosol name
#waccm_(aerosol) = np.float64(waccmgrid.variables[aerosol][:,:,:,:])


#  WACCM gas phase species variable names
#  WACCM gas phase species are in moles/mole air, so straight conversion to ppbv is just multiplication by 10^6.

waccm_gases = ['ALKNIT', 'BENZENE', 'BIGALK', 'BIGENE', 'C2H2', 'C2H4', 'C2H5OH', 'C2H6', 'C3H6', 'C3H8', 'CH3COCH3', 
               'CH3OH', 'CH3OOH', 'CH4', 'CO', 'CO01', 'CO02', 'CO03', 'CO04', 'CO05', 'CO06', 'CO07', 'CO08', 'CO09',
               'CRESOL', 'DMS', 'H2O2', 'HNO3', 'HO2NO2', 'HONITR', 'HYAC', 'MACR', 'MEK', 'MPAN', 'MVK', 'N2O', 'N2O5',
               'NH3', 'NH4', 'NO', 'NO2', 'NOA', 'O3', 'O3S', 'ONITR', 'PAN', 'PBZNIT', 'PHENOL', 'SO2', 'TERPNIT', 
               'TOLUENE', 'XYLENES']
# create empty dictionary structures for WACCM gases, aerosols, and number variables.
waccm_data_gas = {} 
waccm_data_aerosol = {} 
waccm_data_number = {} 

    
# then loop over data and read those data, storing in that dictionary, APPLYING CONVERION from moles/mole to PPMV.
for gas in waccm_gases:
    print 'GAS is:', gas
    waccm_data_gas['waccm_{}'.format(gas)] = 10**6 * np.float64(waccmgrid.variables[gas][:,:,:,:])
    #print (waccmgrid.variables[gas][7,87,0,0])
    print 'AT 0,0:', waccm_data_gas['waccm_{}'.format(gas)][7,87,0,0]
    

# # SECTION 5 CALCULATE PRESSURE THROUGHOUT WACCM SPACE 
# # note that level index runs from top-of_atmosphere to surface.
print "SECTION 5 CALCULATE PRESSURE THROUGHOUT WACCM SPACE "

# WACCM -- calculation of Pressure at layer midpoints [Pa] 
# create array for calculation of Pressure at layer midpoints [Pa]
P_in_Z = np.empty_like(waccm_T) # # create array for calculation of Pressure at layer midpoints [Pa]
P_in_Z[:,:,:,:] = 0.0 # zero out
#P_in_Z[7,87,12,14]
#print "P_in_Z.shape:", P_in_Z.shape
# P_in_Z[0,0,0,0]
for tdx in range(waccm_ntime):
    print "tdx:", tdx
    #print P_in_Z[tdx,0,0,0]
    for levdx in range(waccm_nlev):
        #print "levdx:", levdx
        for latdx in range(waccm_nlat):
            #print "latdx:", latdx
            for londx in range(waccm_nlon):
                #print "londx:", londx
                P_in_Z[tdx, levdx, latdx, londx] = waccm_hyam[levdx] * waccm_P0 + waccm_hybm[levdx] * waccm_PS[tdx, latdx, londx] 
#P_in_Z[7,87,12,14]
for levdx in range(waccm_nlev):
    print "levdx:", levdx, "P_in_Z[0,levdx,0,0]: ", P_in_Z[0,levdx,0,0]
    # print "levdx:", levdx, "P_in_Z[last,levdx,0,0]: ", P_in_Z[(waccm_ntime -1 ),levdx,0,0]
# waccm_PS[0,:,:]   

# ## SECTION 5.1 
print "SECTION 5.1  CALCULATE C_in_Z, N_in_Z and UGPM3_of_GMR"
# ## COMPUTE: C_in_Z array for conversion of WACCM  AEROSOL
# ## 		from Kg/Kg to micrograms/meter-cubed,
# ## and COMPUTE N_in_Z array for conversion of WACCM numbers from #/Kg to #/m3
# ## and COMPUTE UGPM3_of_GMR (meaning ug/m3 for Gas Mixing Ratio), to convert NH4 from [ppmv] to [ug/m3] for ANH4J.
# ## N.B. While NH4 is [mol/mol] in the WACCM file, it was converted to [ppbv] when it was read in.
# ## N.B. WACCM level index runs from top-of_atmosphere to surface.

# Compute conversion factor C_in_Z for converting WACCM aerosol in Kg/Kg to micrograms/cubic-meter, a.k.a. ug/m3.
# Compute conversion factor N_in_Z for converting WACCN numbers in #/Kg to #/cubic-meter, a.k.a. u#/m3.

# constants from scipy
# n has been defined as moles per Kg air for these computations.
# Create array C_in_Z of conversion factors from [Kg/Kg] to [micrograms/cubic-meter] and
# Create array N_in_Z of conversion factors from [#/Kg] to [#/cubic-meter].
C_in_Z = np.empty_like(waccm_T)
N_in_Z = np.empty_like(waccm_T)
UGPM3_of_GMR = np.empty_like(waccm_T)
C_in_Z[:,:,:,:] = 0.0 # zero out
N_in_Z[:,:,:,:] = 0.0 # zero out
UGPM3_of_GMR[:,:,:,:] = 0.0 # zero out

for tdx in range(waccm_ntime):
    print "tdx:", tdx
    for levdx in range(waccm_nlev):
        #print "levdx:", levdx
        for latdx in range(waccm_nlat):
            #print "latdx:", latdx
            for londx in range(waccm_nlon):
                #print "londx:", londx
                #print P_in_Z[tdx, levdx, latdx, londx]
                Vol_of_Kg = ( n * R * waccm_T[tdx, levdx, latdx, londx] ) / P_in_Z[tdx, levdx, latdx, londx]
                if ( levdx  == 87 and latdx == 0 and londx == 0):
                    print "Vol_of_Kg at", tdx, levdx, latdx, londx, "is ", Vol_of_Kg
                C_in_Z[tdx, levdx, latdx, londx] = 3.484e+06 * P_in_Z[tdx, levdx, latdx, londx] / waccm_T[tdx, levdx, latdx, londx]
                N_in_Z[tdx, levdx, latdx, londx] = ( P_in_Z[tdx, levdx, latdx, londx])/( n * R * waccm_T[tdx, levdx, latdx, londx])
                UGPM3_of_GMR[tdx, levdx, latdx, londx] = ( ( NH4_mol_wt * P_in_Z[tdx, levdx, latdx, londx] ) /
							( R * waccm_T[tdx, levdx, latdx, londx]) )
print "C_in_Z check:",C_in_Z[7,(0, 10, 20, 30, 40, 50, 60, 70, 87),0,0]  
print "N_in_Z check:",N_in_Z[7,(0, 10, 20, 30, 40, 50, 60, 70, 87),0,0] 
print "UGPM3_of_GMR:",UGPM3_of_GMR[7,(0, 10, 20, 30, 40, 50, 60, 70, 87),0,0] 

# PLOT conversion factors over levels
tdx  = 0
#_plt.plot(range(waccm_nlev), (C_in_Z[tdx, :, 12,14]/10**9), marker='*', color='green')
#_plt.plot(range(waccm_nlev), (N_in_Z[tdx, :, 12,14]), marker='*', color='yellow')
#_plt.show()
#print "Conversion factors plotted over WACCM layers at a corner. On X-axis, ToA is far left, Sea Level on far right."
#print "GREEN:  N_in_Z(Z)/10**9 at a corner"
#print "YELLOW:  N_in_Z(Z) at a corner"


# # SECTION 6 READ THE WACCM AEROSOLS
print "SECTION 6 READ THE WACCM AEROSOLS  "

# Load the WACCM aerosol species into a dctionary structure
#compute the AIRPACT-units version of the WACCM aerosol species 
 
# then loop over aerosol data and read the data, storing in that dictionary
for aerosol in waccm_aerosols:
    print aerosol # this lists each aerosol name
    #waccm_data_aerosol['waccm_{}'.format(aerosol)] = waccmgrid.variables[aerosol][:,:,:,:]
    waccm_data_aerosol['waccm_{}'.format(aerosol)] = np.float64(waccmgrid.variables[aerosol][:,:,:,:]) 
    print waccm_data_aerosol['waccm_{}'.format(aerosol)][7,87,12,14]

# # SECTION 7 PLOT WACCM AEROSOLS as read
print "SECTION 7 DO NOT PLOT THE WACCM AEROSOLS  "

# PLOT waccm aerosols as read in kg/kg
tdx  = 0

#_plt.plot(range(waccm_nlev), waccm_data_aerosol['waccm_so4_a1'][0, :, 0,0], marker='.', color='blue')
#_plt.plot(range(waccm_nlev), waccm_data_aerosol['waccm_so4_a2'][0, :, 0,0], marker='x', color='blue')
#_plt.plot(range(waccm_nlev), waccm_data_aerosol['waccm_so4_a3'][0, :, 0,0], marker='*', color='blue')
#_plt.plot(range(waccm_nlev), waccm_data_aerosol['waccm_ncl_a1'][0, :, 0,0], marker='.', color='yellow')
#_plt.plot(range(waccm_nlev), waccm_data_aerosol['waccm_ncl_a2'][0, :, 0,0], marker='x', color='yellow')
#_plt.plot(range(waccm_nlev), (waccm_data_aerosol['waccm_ncl_a3'][0, :, 0,0]/10.0), marker='*', color='yellow')
#_plt.plot(range(waccm_nlev), (waccm_data_aerosol['waccm_soa1_a1'][0, :, 0,0] + waccm_data_aerosol['waccm_soa2_a1'][0, :, 0,0] +
                             #waccm_data_aerosol['waccm_soa3_a1'][0, :, 0,0] + waccm_data_aerosol['waccm_soa4_a1'][0, :, 0,0] + 
                             #waccm_data_aerosol['waccm_soa5_a1'][0, :, 0,0]), marker='.', color='brown')
#_plt.plot(range(waccm_nlev), (waccm_data_aerosol['waccm_soa1_a2'][0, :, 0,0] + waccm_data_aerosol['waccm_soa2_a2'][0, :, 0,0] +
                             #waccm_data_aerosol['waccm_soa3_a2'][0, :, 0,0] + waccm_data_aerosol['waccm_soa4_a2'][0, :, 0,0] + 
                             #waccm_data_aerosol['waccm_soa5_a2'][0, :, 0,0]), marker='x', color='brown')

#plt.plot(range(waccm_nlev), waccm_data_aerosol['waccm_so4_a2'][0, :, 0,0], marker='x', color='brown')
#plt.plot(range(waccm_nlev), waccm_data_aerosol['waccm_so4_a3'][0, :, 0,0], marker='*', color='brown')
#_plt.show()

#print "Aerosols as kg/kg plotted over WACCM layers.  On X-axis, ToA is far left, Sea Level on far right."
#print "GRAY .: log 10 waccm_ncl_a1 at a corner"
#print "GRAY x: log 10 waccm_ncl_a2 at a corner"
#print "GRAY o: log 10 waccm_ncl_a3 at a corner"
#print "BLUE .: waccm_so4_a1 at a corner"
#print "BLUE x: waccm_so4_a2 at a corner"
#print "BLUE o: waccm_so4_a3 at a corner"
#print "YELLOW .: waccm_ncl_a1 at a corner"
#print "YELLOW x: waccm_ncl_a2 at a corner"
#print "YELLOW o: waccm_ncl_a3/10.0 at a corner"
#print "BROWN .: waccm_soa*_a1 at a corner"
#print "BROWN x: waccm_soa*_a1 at a corner"
#print "Same plot code as for ug/m3 converted aerosols, below."


# # SECTION 8 Convert the WACCM AEROSOLS in place.
print "SECTION 8 Convert the WACCM AEROSOLS IN PLACE"
print "SECTION 8.1 Convert the WACCM AEROSOLS IN PLACE"

# compute the AIRPACT version in units [ug/m3] for the WACCM aerosol species 

for aerosol in waccm_aerosols:
    print aerosol # this lists each aerosol name
    for tdx in range(waccm_ntime):
        #print "tdx:", tdx
        for levdx in range(waccm_nlev):
            #print "levdx:", levdx
            #print "input as Kg/Kg: ", waccm_data_aerosol['waccm_{}'.format(aerosol)][tdx,levdx,12,14] 
            for latdx in range(waccm_nlat):
                #print "latdx:", latdx
                for londx in range(waccm_nlon):
                    #print "londx:", londx
                    #print P_in_Z[tdx, levdx, latdx, londx]
                    waccm_data_aerosol['waccm_{}'.format(aerosol)][tdx, levdx, latdx, londx] = (
                        C_in_Z[tdx, levdx, latdx, londx] * 
                        waccm_data_aerosol['waccm_{}'.format(aerosol)][tdx, levdx, latdx, londx] )
#            print "Conversion factor: ", C_in_Z[tdx,levdx,12,14]
#            print "results as ug/m3: ", waccm_data_aerosol['waccm_{}'.format(aerosol)][tdx,levdx,12,14]
aer_sum_SW = 0.0
aer_sum_NE = 0.0
for aerosol in waccm_aerosols:
    print aerosol, "results at SW Corner as ug/m3: ", waccm_data_aerosol['waccm_{}'.format(aerosol)][0,87,0,0]
    print aerosol, "results at  NE Corner as ug/m3: ", waccm_data_aerosol['waccm_{}'.format(aerosol)][0,87,12,14]
    aer_sum_SW += waccm_data_aerosol['waccm_{}'.format(aerosol)][0,87,0,0]
    aer_sum_NE += waccm_data_aerosol['waccm_{}'.format(aerosol)][0,87,12,14]
print "Sum of Aerosols at SW surface corner", aer_sum_SW
print "Sum of Aerosols at NE surface corner", aer_sum_NE

print "SECTION 8.2 Convert the WACCM NH4 gas to BCON ANH4J aerosol, in place"
WACCM_NH4 = 'NH4'
aerosol = WACCM_NH4
BCON_NH4 = 'ANH4J'

# MH4_mol_wt = 18.039 # set with constants.
waccm_gas_nh4 = ['NH4'] # list of length 1.

print "Convert WACCM:", WACCM_NH4, " to BCON: ", BCON_NH4

for aerosol in waccm_gas_nh4:
    for tdx in range(waccm_ntime):
    #print "tdx:", tdx
        for levdx in range(waccm_nlev):
            #print "levdx:", levdx
            print "input as mol/mol", waccm_data_gas['waccm_{}'.format(aerosol)][tdx,levdx,12,14]
            for latdx in range(waccm_nlat):
                #print "latdx:", latdx
                for londx in range(waccm_nlon):
                    #print "londx:", londx
                    #print P_in_Z[tdx, levdx, latdx, londx]
                     waccm_data_gas['waccm_{}'.format(aerosol)][tdx, levdx, latdx, londx] = (
                         UGPM3_of_GMR[tdx, levdx, latdx, londx] *
                         waccm_data_gas['waccm_{}'.format(aerosol)][tdx, levdx, latdx, londx] )


# # SECTION 9 PLOT WACCM AEROSOLS after conversion
print " SECTION 9 PLOT WACCM AEROSOLS after conversion"

# PLOT waccm aerosols as computed for ug/m3.
tdx = 0
#_plt.plot(range(waccm_nlev), waccm_data_aerosol['waccm_so4_a1'][tdx, :, 0,0], marker='.', color='blue')
#_plt.plot(range(waccm_nlev), waccm_data_aerosol['waccm_so4_a2'][0, :, 0,0], marker='x', color='blue')
#_plt.plot(range(waccm_nlev), waccm_data_aerosol['waccm_so4_a3'][0, :, 0,0], marker='*', color='blue')
#_plt.plot(range(waccm_nlev), waccm_data_aerosol['waccm_ncl_a1'][0, :, 0,0], marker='.', color='yellow')
#_plt.plot(range(waccm_nlev), waccm_data_aerosol['waccm_ncl_a2'][0, :, 0,0], marker='x', color='yellow')
#_plt.plot(range(waccm_nlev), (waccm_data_aerosol['waccm_ncl_a3'][0, :, 0,0]/10.0), marker='*', color='yellow')
#_plt.plot(range(waccm_nlev), (waccm_data_aerosol['waccm_soa1_a1'][0, :, 0,0] + waccm_data_aerosol['waccm_soa2_a1'][0, :, 0,0] +
                             #waccm_data_aerosol['waccm_soa3_a1'][0, :, 0,0] + waccm_data_aerosol['waccm_soa4_a1'][0, :, 0,0] + 
                             #waccm_data_aerosol['waccm_soa5_a1'][0, :, 0,0]), marker='.', color='brown')
#_plt.plot(range(waccm_nlev), (waccm_data_aerosol['waccm_soa1_a2'][0, :, 0,0] + waccm_data_aerosol['waccm_soa2_a2'][0, :, 0,0] +
                             #waccm_data_aerosol['waccm_soa3_a2'][0, :, 0,0] + waccm_data_aerosol['waccm_soa4_a2'][0, :, 0,0] + 
                             #waccm_data_aerosol['waccm_soa5_a2'][0, :, 0,0]), marker='x', color='brown')

#_plt.show()

#print "Aerosols as ug/m3 plotted over WACCM layers.  On X-axis, ToA is far left, Sea Level on far right."

#print "BLUE .: waccm_so4_a1 at a corner"
#print "BLUE x: waccm_so4_a2 at a corner"
#print "BLUE o: waccm_so4_a3 at a corner"
#print "YELLOW .: waccm_ncl_a1 at a corner"
#print "YELLOW x: waccm_ncl_a2 at a corner"
#print "YELLOW o: waccm_ncl_a3/10.0 at a corner"
#print "BROWN .: waccm_soa*_a1 at a corner"
#print "BROWN x: waccm_soa*_a1 at a corner"
#print "Same plot code as for kg/kg aerosols, above."


# # SECTION 10 Load, plot, convert and replot WACCM number species
print " SECTION 10 Load, plot, convert and replot WACCM number species"

# Load the WACCM numbers into the dictionary structure
for number in waccm_numbers:
    print number # this lists each aerosol name
    waccm_data_aerosol['waccm_{}'.format(number)] = np.float64(waccmgrid.variables[number][:,:,:,:]) 
    print waccm_data_aerosol['waccm_{}'.format(number)][:,87,12,14]


# PLOT waccm numbers as read in as #/Kg
tdx  = 0
#_plt.plot(range(waccm_nlev), (waccm_data_aerosol['waccm_num_a1'][tdx, :, 12,14]), marker='*', color='black')
#_plt.plot(range(waccm_nlev), (waccm_data_aerosol['waccm_num_a2'][tdx, :, 12,14]), marker='*', color='green')
#_plt.plot(range(waccm_nlev), (100 * waccm_data_aerosol['waccm_num_a3'][tdx, :, 12,14]), marker='*', color='yellow')
#_plt.show()
#print "Numbers read in as #/Kg plotted over WACCM layers.  On X-axis, ToA is far left, Sea Level on far right."
#print "BLACK:  waccm_num_a1(Z) at a corner"
#print "GREEN:  waccm_num_a2(Z) at a corner"
#print "YELLOW:  100* waccm_num_a3(Z) at a corner"


# #COMPUTE the AIRPACT-units version of the WACCM number species, in place

# compute the AIRPACT version of the WACCM number species.
for species in waccm_numbers:
    print species # this lists each aerosol name
    for tdx in range(waccm_ntime):
        print "tdx:", tdx
        for levdx in range(waccm_nlev):
            #print "levdx:", levdx
            #print "Read in as #/Kg: ", waccm_data_aerosol['waccm_{}'.format(species)][tdx,levdx,12,14]
            for latdx in range(waccm_nlat):
                #print "latdx:", latdx
                for londx in range(waccm_nlon):
                    #print "londx:", londx
                    #print P_in_Z[tdx, levdx, latdx, londx]
                    waccm_data_aerosol['waccm_{}'.format(species)][tdx, levdx, latdx, londx] = (
                        N_in_Z[tdx, levdx, latdx, londx] * 
                        waccm_data_aerosol['waccm_{}'.format(species)][tdx, levdx, latdx, londx] )
            #print "P:",P_in_Z[tdx, levdx, 12,14],"T:",12,14
            #print "Conversion factor: ", N_in_Z[tdx,levdx,12,14]
            #print "resutls as #/m3: ", waccm_data_aerosol['waccm_{}'.format(species)][tdx,levdx,12,14]


# PLOT waccm numbers as converted for AIRPACT as #/m3
tdx  = 0
#_plt.plot(range(waccm_nlev), (waccm_data_aerosol['waccm_num_a1'][tdx, :, 12,14]), marker='*', color='black')
#_plt.plot(range(waccm_nlev), (waccm_data_aerosol['waccm_num_a2'][tdx, :, 12,14]), marker='*', color='green')
#_plt.plot(range(waccm_nlev), (100 * waccm_data_aerosol['waccm_num_a3'][tdx, :, 12,14]), marker='*', color='yellow')
#_plt.show()
#print "Numbers as #/m3 plotted over WACCM layers.  On X-axis, ToA is far left, Sea Level on far right."
#print "BLACK:  waccm_num_a1(Z) at a corner"
#print "GREEN:  waccm_num_a2(Z) at a corner"
#print "YELLOW:  100* waccm_num_a3(Z) at a corner"


# # SECTION 11 (already Loaded) so plot, convert and replot WACCM Gas species
print "SECTION 11 (already Loaded) so plot, convert and replot WACCM Gas species"

# PLOT waccm numbers as converted for AIRPACT as moles/mole
waccm_ch4 =  np.float64(waccmgrid.variables['CH4'][0,:,12,14]) 
waccm_co  =  np.float64(waccmgrid.variables['CO'][0,:,12,14]) 
waccm_o3  =  np.float64(waccmgrid.variables['O3'][0,:,12,14]) 
print waccm_ch4

#_plt.plot(range(waccm_nlev), (100. * waccm_ch4), marker='*', color='black')
#_plt.plot(range(waccm_nlev), waccm_co, marker='*', color='green')
#_plt.plot(range(waccm_nlev), (100. * waccm_o3), marker='*', color='yellow')
#_plt.show()
#print "WACCM gases as moles/mole over WACCM layers.  On X-axis, ToA is far left, Sea Level on far right."
#print "BLACK:  waccm_CH4 * 100 at a corner"
#print "GREEN:  waccm_CO at a corner"
#print "YELLOW: waccm_O3 * 100 at a corner"


# # SECTION 11.5  does CONVERSION OF GAS PHASE SPECIES FROM WACCM UNITS OF MOLES/MOLE TO PPMV: read & convert in place.
print "SECTION 11.5  CONVERSION OF GAS PHASE SPECIES FROM WACCM UNITS OF MOLES/MOLE TO PPMV"

# create list of the WACCM gas phase species

waccm_gases = ['ALKNIT', 'BENZENE', 'BIGALK', 'BIGENE', 'C2H2', 'C2H4', 'C2H5OH', 'C2H6', 'C3H6', 'C3H8', 'CH3COCH3', 
               'CH3OH', 'CH3OOH', 'CH4', 'CO', 'CO01', 'CO02', 'CO03', 'CO04', 'CO05', 'CO06', 'CO07', 'CO08', 'CO09',
               'CRESOL', 'DMS', 'H2O2', 'HNO3', 'HO2NO2', 'HONITR', 'HYAC', 'MACR', 'MEK', 'MPAN', 'MVK', 'N2O', 'N2O5',
               'NH3', 'NH4', 'NO', 'NO2', 'NOA', 'O3', 'O3S', 'ONITR', 'PAN', 'PBZNIT', 'PHENOL', 'SO2', 'TERPNIT', 
               'TOLUENE', 'XYLENES']

#  WACCM gases' molecular weights
waccm_gas_molwt  = [133.141, 78.1104, 72.1438, 56.1032, 26.0368, 28.0516, 46.0658, 30.0664, 42.0774, 44.0922, 58.0768,
                    32.0400, 48.0394, 16.0406, 28.0104, 28.0104, 28.0104,  28.0104,  28.0104,  28.0104,  28.0104,  
                    28.0104,  28.0104,  28.0104, 108.136, 62.1324, 34.0136, 63.0123, 79.0117, 133.100, 74.0762, 
                    70.0878, 72.1026, 147.085, 70.0878, 44.0129, 108.010,  17.031, 18.039, 30.0061, 46.0055, 119.074, 
                    47.9982, 47.9982, 133.100, 121.048, 183.118, 94.1098, 64.0648, 215.240, 92.1362, 106.162]

 
# then loop over data and read those data, storing in that dictionary, APPLYING CONVERION from moles/mole to PPMV.
for gas in waccm_gases:
    print "Gas is: ", gas # this lists each gas name and structured as [tdx, levdx, latdx, londx]
    waccm_data_gas['waccm_{}'.format(gas)] = 10**6 * np.float64(waccmgrid.variables[gas][:,:,:,:]) 
    #print waccm_data_gas['waccm_{}'.format(gas)][7,87,12,14]

waccm_ch4 = 10**6 * np.float64(waccmgrid.variables['CH4'][0,:,12,14]) 
waccm_co = 10**6 * np.float64(waccmgrid.variables['CO'][0,:,12,14]) 
waccm_o3 = 10**6 * np.float64(waccmgrid.variables['O3'][0,:,12,14]) 
print waccm_ch4

# PLOT waccm gases after converted for AIRPACT to [ppm]
#_plt.plot(range(waccm_nlev), (100. * waccm_ch4), marker='*', color='black')
#_plt.plot(range(waccm_nlev),  waccm_co, marker='*', color='green')
#_plt.plot(range(waccm_nlev), (100. * waccm_o3), marker='*', color='yellow')
#_plt.show()
#print "WACCM gases as #/m3 plotted over WACCM layers.  On X-axis, ToA is far left, Sea Level on far right."
#print "BLACK:  waccm_CH4 * 100 at a corner"
#print "GREEN:  waccm_CO at a corner"
#print "YELLOW: waccm_O3 * 100 at a corner"


# # SECTION 12 Read BCON Template File.
print "SECTION 12 Read BCON Template File."

# SET UP TO READ IN THE BCON REDATED TEMPLATE FILE

# file locations: WACCM files for boundary conditions input
# (done above) waccm_file_dir = "/data/lar/projects/airpact5/misc/WACCM_for_BCON/"
#template_file_name = 'bcon_cb05_{y}{m}{d}_WACCM.ncf'.format(m=m, y=y, d=d)
template_file_name = 'bcon_cb05_{y}{m}{d}.ncf'.format(m=m, y=y, d=d)
bcon_file = waccm_file_dir + template_file_name
print (bcon_file)
dir(bcon_file) 

#READ IT
bcon_redated = Dataset(bcon_file,'r+')
#dir(bcon_redated)

# SET UP LIST OF BCON SPECIES
bcon_tsteps = ['TFLAG']

bcon_aerosols = ['ACLI', 'ACLJ', 'ACLK', 'AECJ', 'ANAI', 'ANAJ', 'ANAK', 'ANH4J', 'AOLGAJ', 
                 'AOLGBJ', 'APNCOMJ', 'APOCJ', 'ASO4I', 'ASO4J', 'ASO4K', 'ASOIL']

bcon_gases = ['NR','PAR','IOLE','TERP','ETH','ETOH','ROOH','ETHA','OLE','FORM','ALD2','MGLY','AACD',
              'MEOH','MEPX','CH4','CO','CRES','DMS','ALDX','H2O2','HNO3','PNA','HO2','ISPD','ISOP',
              'PANX','N2O5','NH3','NO2','NO','O3','NTR','PAN','SO2','TOL','NO3']

bcon_nums = ['NUMACC','NUMATKN','NUMCOR']

print bcon_nums


# ## SECTION 12.1 FAKE in BCON Tsteps -- how to get in via scripting...?
print "SECTION 12.1 FAKE in BCON Tsteps "

print  range(waccm_ntime) 
#BCON_TSTEP_DATES = (2018206, 2018206, 2018206, 2018207, 2018207, 2018207, 2018207, 2018208, 2018208, 2018208, 2018208)
#BCON_TSTEP_TIMES = (120000, 180000,  60000, 0, 120000, 180000, 60000, 0, 120000, 120000, 60000)
BCON_TSTEP_DATES = ( 2021026, 2021026, 2021026, 2021027, 2021027, 2021027, 2021027, 2021028, 2021028, 2021028)
BCON_TSTEP_TIMES = ( 060000, 120000,180000,000000,060000,120000,180000,000000,060000,120000 )
for bcts in range(waccm_ntime):
    print "TS:", bcts, BCON_TSTEP_DATES[bcts], BCON_TSTEP_TIMES[bcts]


# check values of time steps for WACCM and BCON
# can I iterate across time steps
for tdx in range(waccm_ntime):
    print waccm_time[tdx]

print  range(waccm_ntime)

for ts in bcon_tsteps:
    print "BCON tstep is: ", ts
    
#print range(bcon_tsteps)    
    


# PLOT waccm numbers as read in as #/Kg
tdx  = 0
#_plt.plot(range(waccm_nlev), (waccm_data_aerosol['waccm_num_a1'][tdx, :, 12,14]), marker='*', color='black')
#_plt.plot(range(waccm_nlev), (waccm_data_aerosol['waccm_num_a2'][tdx, :, 12,14]), marker='*', color='green')
#_plt.plot(range(waccm_nlev), (100 * waccm_data_aerosol['waccm_num_a3'][tdx, :, 12,14]), marker='*', color='yellow')
#_plt.show()
#print "Numbers read in as #/Kg plotted over WACCM layers.  Z on X-axis (abscissa) is inverted, so ToA is far left, Sea Level on far right "
#print "BLACK:  waccm_num_a1(Z) at a corner"
#print "GREEN:  waccm_num_a2(Z) at a corner"
#print "YELLOW:  100* waccm_num_a3(Z) at a corner"


# # SECTION 13 Find Indices for mapping WACCM Cells to BCON Perimeter Cells.
print "SECTION 13 Find Indices for mapping WACCM Cells to BCON Perimeter Cells."

# ## SECTION 13.1 Read in WACCM LAT and LON
print "SECTION 13.1 Read in WACCM LAT and LON"

# READ WACCM file for lat and lon.
# read netCDF file using open_dataset method of xarray into an array.
waccm_lat = waccmgrid.variables['lat'][:]
print "Lat as read in:", waccm_lat

waccm_lon = waccmgrid.variables['lon'][:] 
print "Lon as read in:", waccm_lon

# Fix longitudes to range of -180 to +180.
for i_w_lon in range(waccm_nlon):
    if (waccm_lon[i_w_lon] > 180.0 ): 
        waccm_lon[i_w_lon] = waccm_lon[i_w_lon] - 360.0
        
print "Lon with W lons as Negative:", waccm_lon


# ## SECTION 13.2 Set up arrays for indices mapping WACCM to BCON
print "SECTION 13.2 Set up arrays for indices mapping WACCM to BCON"

# Set up arrays for storing indices for WACCM to BCON

for latdx in range(waccm_nlat):
    print "latdx:", latdx, waccm_lat[latdx]
for londx in range(waccm_nlon):
    print "          londx:", londx, waccm_lon[londx]
i_lon_w2b=[-9 for ib in range(perim_size)]
j_lat_w2b=[-9 for ib in range(perim_size)]
        


# ## SECTION 13.3 Find indices mapping WACCM to BCON
print "SECTION 13.3 Find indices mapping WACCM to BCON"

#FOR EACH BCON PERIM LAT AND LAN, FIND THE INDICES FOR MAPPING WACCM CELLS TO THAT BOUNDARY CELL.
for ib in range(perim_size):
    print "ib: ", ib
    min_delta_lat = 100
    for j_w_lat in range(waccm_nlat):
        #print "j_w_lat: ", j_w_lat 
        delta_lat = abs( bcon_lat[ib] - waccm_lat[j_w_lat])
        print "delta_lat:", delta_lat
        if ( delta_lat < min_delta_lat ):
            j_lat_w2b[ib] =  j_w_lat
            min_delta_lat = delta_lat
        elif (delta_lat == min_delta_lat):
            print "why does delta_lat == min_delta_lat?"
        elif (delta_lat > min_delta_lat):
            break
        #endif
    min_delta_lon = 100
    for i_w_lon in range(waccm_nlon):
        #print "i_w_lon: ", i_w_lon
        delta_lon = abs( bcon_lon[ib] - waccm_lon[i_w_lon])
        if ( delta_lon < min_delta_lon ):
            i_lon_w2b[ib] =  i_w_lon
            min_delta_lon = delta_lon
        elif (delta_lon == min_delta_lon):
            print "why does delta_lon == min_delta_lon?"
        elif (delta_lon > min_delta_lon):
            i_lon_w2b[ib] =  i_w_lon
            break
        #endif
    print "ib:", ib, "i_lon_w2b:",i_lon_w2b[ib], "j_lat_w2b:", j_lat_w2b[ib]
#@ DO A VERSION USING min of root of sum of squares of differences?  Cosine of Latitude applied to Long.   
    


# ## SECTION 13.4 Plot indices mapping WACCM Lat and Lon into BCON
print "SECTION 13.4 Plot indices mapping WACCM Lat and Lon into BCON"

# DRAW BOX SHOWING THE WACCM INDICES TO ALL BCON PERIMITER LAT/LON CELLS
#_plt.plot(i_lon_w2b, j_lat_w2b, marker='X', color='red')
#_plt.show()
print "WACCM to BCON indices"


for ib in range(perim_size):
    print "ib: ", ib, "i_lon_w2b:",i_lon_w2b[ib], "j_lat_w2b:", j_lat_w2b[ib]


# perim_size = 1089  WRONG?
for ib in range(perim_size):
    print "Lon-match at ib: ", ib, 'BCON:',bcon_lon[ib],  'WACCM', waccm_lon[i_lon_w2b[ib]]
    print "Lat-match at ib: ", ib, 'BCON:',bcon_lat[ib],  'WACCM', waccm_lat[j_lat_w2b[ib]]
    dist = ((bcon_lon[ib] - waccm_lon[i_lon_w2b[ib]])**2. + (bcon_lat[ib] - waccm_lat[j_lat_w2b[ib]])**2. )**0.5
    print "Distance in nominal degrees:", dist


# # SECTION 13.5 Plot .... 
print "SECTION 13.5 Plot .... "

# PLOT P_in_Z by waccm_level
tdx  = 0
ibdx = 0

#_plt.plot(range(waccm_nlev), P_in_Z[tdx, :, j_lat_w2b[ibdx], i_lon_w2b[ibdx]], marker='X', color='red')
#bconmet_pres = bconmet.variables['PRES'][:,:,:] # float PRES(TSTEP, LAY, PERIM) in mcip file
#_plt.plot(range(bconmet_nlev), bconmet_pres[tdx, range(bconmet_nlev), ibdx], marker='X', color='blue')
#_plt.plot(range(waccm_nlev), 100.0 * waccm_lev[:], marker='X', color='black')
#_plt.show()
#print "RED: WACCM P(Z) at SW corner, Z on X-axis (abscissa) is inverted, so ToA is far left, Sea Level on far right "
#print "BLUE: BCON P(Z) at SW corner, Z on X-axis (abscissa), so ToA is far right, Sea Level on far left "


# PLOT P_in_Z by waccm_level
tdx  = 0
ibdx = 285
#_plt.plot(range(waccm_nlev), P_in_Z[tdx, :, j_lat_w2b[ibdx], i_lon_w2b[ibdx]], marker='X', color='red')
#_plt.plot(range(bconmet_nlev), bconmet_pres[tdx, range(bconmet_nlev), ibdx], marker='X', color='blue')
#_plt.plot(range(waccm_nlev), 100.0 * waccm_lev[:], marker='X', color='black')
#_plt.show()
#print "RED: WACCM P(Z) at SE corner, Z on X-axis (abscissa) is inverted, so ToA is far left, surface layer on far right "
#print "BLUE: BCON P(Z) at SE corner, Z on X-axis (abscissa), so ToA is far right, surface layer on far left "


# PLOT P_of_Z by waccm_level
tdx  = 0
ibdx = 544
#_plt.plot(range(waccm_nlev), P_in_Z[tdx, :, j_lat_w2b[ibdx], i_lon_w2b[ibdx]], marker='X', color='red')
#_plt.plot(range(bconmet_nlev), bconmet_pres[tdx, range(bconmet_nlev), ibdx], marker='X', color='blue')
#_plt.plot(range(waccm_nlev), 100.0 * waccm_lev[:], marker='X', color='black')
#_plt.show()
#print "WACCM P(Z) at NE corner, Z on X-axis (abscissa) is inverted, so ToA is far left "


# PLOT P_of_Z by waccm_level
tdx  = 0
ibdx = 830
#_plt.plot(range(waccm_nlev), P_in_Z[tdx, :, j_lat_w2b[ibdx], i_lon_w2b[ibdx]], marker='X', color='red')
#_plt.plot(range(bconmet_nlev), bconmet_pres[tdx, range(bconmet_nlev), ibdx], marker='X', color='blue')
#_plt.plot(range(waccm_nlev), 100.0 * waccm_lev[:], marker='X', color='black')
#_plt.show()
#print "WACCM P(Z) at NW corner, Z on X-axis (abscissa) is inverted, so ToA is far left "


# # SECTION 14 Read BCON Template File, all species
print "SECTION 14 Read BCON Template File, all species"

# Load the BCON species into dictionary structures
bcon_data_tflag = {} 
bcon_data_gas = {} 
bcon_data_aerosol = {} 
bcon_data_number = {} 

bcon_zeroed = FALSE
 
# loop over all BCON gas species and read the data, storing in the dictionary, zeroing it!
print "PROBLEM:  BCON TFLAG is a duple but only read in here as an integer.  "
print "          May have to use STIME and SDATE and construct time steps?  Or just count them."

for ts in bcon_tsteps:
    print "BCON tstep is: ", ts
    bcon_data_tflag['bcon_{}'.format(ts)] = bcon_redated.variables[ts][:,:,:]
    print bcon_data_tflag['bcon_{}'.format(ts)][0,0,0]
    
# read in, maybe zeroing on read.

if ( bcon_zeroed ):
    # loop over all BCON gas species and read those data, storing in that dictionary, zeroing it!
    for zgas in bcon_gases:
        print "BCON Gas is: ", zgas # this lists each species name
        bcon_data_gas['bcon_{}'.format(zgas)] = 0.0 * np.float64(bcon_redated.variables[zgas][:,:,:])
        print bcon_data_gas['bcon_{}'.format(zgas)][7,0,1089] #[0,0,0]

    # loop over all BCON aerosol species and read those data, storing in that dictionary, zeroing it!
    for zaerosol in bcon_aerosols:
        print "BCON Aerosol is: ", zaerosol # this lists each aerosol name
        bcon_data_aerosol['bcon_{}'.format(zaerosol)] = 0.0 * np.float64(bcon_redated.variables[zaerosol][:,:,:]) 
        #print bcon_data_aerosol['bcon_{}'.format(zaerosol)[7,0,1089] 
    
    # loop over all BCON number species and read those data, storing in that dictionary!
    for znum in bcon_nums:
        print "BCON Number is: ", znum # this lists each number name
        bcon_data_number['bcon_{}'.format(znum)] = 0.0 * np.float64(bcon_redated.variables[znum][:,:,:])
        print bcon_data_number['bcon_{}'.format(znum)][7,0,1089] # [0,0,0]

else:
    for gas in bcon_gases:
        print "BCON Gas is: ", gas # this lists each species name
        bcon_data_gas['bcon_{}'.format(gas)] = np.float64(bcon_redated.variables[gas][:,:,:])
        print bcon_data_gas['bcon_{}'.format(gas)][7,0,1089] #[0,0,0]

    # loop over all BCON aerosol species and read those data, storing in that dictionary, zeroing it!
    for aerosol in bcon_aerosols:
        print "BCON Aerosol is: ", aerosol # this lists each aerosol name
        bcon_data_aerosol['bcon_{}'.format(aerosol)] = np.float64(bcon_redated.variables[aerosol][:,:,:])
        print bcon_data_aerosol['bcon_{}'.format(aerosol)][7,0,1089]
                                
    # loop over all BCON number species and read those data, storing in that dictionary!
    for num in bcon_nums:
        print "BCON Number is: ", num # this lists each number name
        bcon_data_number['bcon_{}'.format(num)] = np.float64(bcon_redated.variables[num][:,:,:])
        print bcon_data_number['bcon_{}'.format(num)][7,0,1089] #[0,0,0]   
                                
    for num in bcon_nums:
        print "BCON NUMBER is: ", num # this lists each aerosol name
        bcon_data_number['bcon_{}'.format(num)] = np.float64(bcon_redated.variables[num][:,:,:])
        print bcon_data_number['bcon_{}'.format(num)][7,0,1089]                                



# ## SECTION 14.1 PLOT BCON species by BCON levels
print "SECTION 14.1 PLOT BCON SPECIES BY BCON LEVELS"

## PLOT BCON species by BCON levels
if ( not bcon_zeroed ):
    tdx  = 0
    ibdx = 0
    print bconmet_nlev

#    plt.plot(range(bconmet_nlev),(bcon_data_gas['bcon_O3'][tdx,range(bconmet_nlev),ibdx]),marker='X',color='red')
#    plt.plot(range(bconmet_nlev),(bcon_data_gas['bcon_CO'][tdx,range(bconmet_nlev),ibdx]),marker='*',color='blue')
#    plt.plot(range(bconmet_nlev),(bcon_data_gas['bcon_NO2'][tdx,range(bconmet_nlev),ibdx]),marker='o',color='brown')
#    plt.show()
#    print "RED: bcon_O3 [ppm] at SW corner "
#    print "BLUE: bcon_CO [ppm] at SW corner "
#    print "BROWN: bcon_NO2 [ppm] at SW corner "
else:
    print 'BCON Zeroed'


# ## SECTION 14.1.5 zero out all bcon template fields
print "SECTION 14.1.5 ZERO OUT ALL BCON TEMPLATE FIELDS"



# ## SECTION 14.2 Explore BCON topo heights & pressure vs WACCM surface pressure and lowest level pressure.
print "SECTION 14.2 EXPLORE BCON TOPO HEIGHTS & PRESSURE vs WACCM SURFACE PRESSURE AND LOWEST LEVEL PRESSURE"

# Explore BCON topo heights & pressure vs WACCM surface pressure and lowest level pressure.
# Walk around BCON perimeter, and write the lowest level pressure from METBDY3D, & waccm_PS[tdx, latdx, londx] and
# P_in_Z(tdx, lvedx, j_lat_w2b, i_lon_w2b)
#print waccm_PS.min()
print waccm_PS.max()
#x print np.argmax(waccm_PS)
#x print waccm_PS[885]
#for ib in range(1090):
#    print ib, "B_HT:",bcon_ht[ib],"B_P:",bconmet_pres[0,0,ib],"  W_PS:", waccm_PS[0,j_lat_w2b[ib],i_lon_w2b[ib]], " W_PZ:",P_in_Z[0,87,j_lat_w2b[ib],i_lon_w2b[ib]]
 


# Correlation coefficient calculation.... BCON to P_in_Z

print "Correlation of BCON surface pressure to matching WACCM P_in_Z in bottom layer"
np.corrcoef((bconmet_pres[0,0,:]),(P_in_Z[0,87,j_lat_w2b[:],i_lon_w2b[:]]))



# Correlation coefficient calculation.... BCON to PS

print "Correlation of BCON surface pressure to matching WACCM PS in bottom layer"
np.corrcoef((bconmet_pres[0,0,:]),(waccm_PS[0,j_lat_w2b[:],i_lon_w2b[:]]))


# ## SECTION 14.3 Use pressure comparisons between BCON and P_of_Z to set indices for mapping WACCM level to BCON level.
print "SECTION 14.3 USE PRESSURE COMPARISONS BETWEEN BCON and P_of_Z TO SET INDICES FOR MAPPING WACCM LEVEL TO BCON LEVEL"

# USE PRESSURE COMPARISONS BETWEEN BCON and P_of_Z to set indices for mapping WACCM level to BCON level.
# TEST: perim_size = 1
# TEST: waccm_ntime = 1
# Create an empty array for indices into WACCM by BCON perimiter and BCON level.
time_begin = time.time()

# waccm_ntime = 1 # TEST
# perim_size = 1090 # TEST 

#set up verical array of depth of WACCM to hold pressure deltas.
# use scalar delta_P;  x delta_P = np.full((waccm_nlev),-10**6,float)
#print(dir(delta_P))

bc_lev_from_waccm_lev = np.full((waccm_ntime,perim_size,bconmet_nlev), (waccm_nlev - 1), int)

for tdx in range(waccm_ntime):
    #for tdx in range(waccm_ntime):
    print 'For WACCM Time index:', tdx
    for ib in range(perim_size):
        print "... For BCON perimiter index ib: ", ib, j_lat_w2b[ib], i_lon_w2b[ib]
        for ilev_up in range(bconmet_nlev):    #Vertical traverse bottom to top of BCON levels   
            ilev = bconmet_nlev - 1 - ilev_up
            # print "......For BCON downward level index:", ilev
#            min_delta_P = -10**6
            # print "...... BCON PRES to match", bconmet_pres[tdx,ilev,ib]  #intial version ignores variation of pressure in time
            last_delta_P = 10**6
            for top_down_levdx in range(waccm_nlev):
                #print "........WACCM top_down_levdx:", top_down_levdx
                delta_P = abs( bconmet_pres[0,ilev,ib] - P_in_Z[tdx, top_down_levdx, j_lat_w2b[ib], i_lon_w2b[ib]])
                #delta_P[bot_up_levdx] = abs( bconmet_pres[0,ilev,ib] - P_in_Z[tdx, top_down_levdx, j_lat_w2b[ib], i_lon_w2b[ib]])
                #print ".........delta_P calc:", delta_P # delta_P[bot_up_levdx]
                if ( delta_P > last_delta_P ):
                    # print "..........Last delta_P: ", last_delta_P
                    # print "..........WACCM top_down_levdx:", top_down_levdx
                    # print "..........WACCM pressure match of: ",last_P_of_Z 
                    # print "....??....USE bc_lev_from_waccm_lev[tdx,ib,ilev]:", bc_lev_from_waccm_lev[tdx,ib,ilev]
                    break
                else:
                    bc_lev_from_waccm_lev[tdx,ib,ilev] = top_down_levdx
                    last_delta_P = delta_P
                    last_P_of_Z = P_in_Z[tdx, top_down_levdx, j_lat_w2b[ib], i_lon_w2b[ib]]
                #endif    

print "final top-down_dx, ilev_up, ib, tdx:", top_down_levdx, ilev_up, ib, tdx
print "SW Corner bc_lev_from_waccm_lev[0,0,ilev]",    bc_lev_from_waccm_lev[0,0,:]
print "SE Corner bc_lev_from_waccm_lev[0,285,ilev]:", bc_lev_from_waccm_lev[0,285,:]
print "NE Corner bc_lev_from_waccm_lev[0,544,ilev]:", bc_lev_from_waccm_lev[0,544,:]
print "NW Corner bc_lev_from_waccm_lev[0,830,ilev]:", bc_lev_from_waccm_lev[0,830,:]
print "Last Point in bc_lev_from_waccm_lev[0,1089,ilev]:", bc_lev_from_waccm_lev[0,1089,:]
print "Timing: ",(time.time() - time_begin)


'''# PLOT waccm aerosols after conversion to ug/m3
tdx  = 0

#_plt.plot(range(waccm_nlev), waccm_data_aerosol['waccm_so4_a1'][0, :, 0,0], marker='.', color='blue')
#_plt.plot(range(waccm_nlev), waccm_data_aerosol['waccm_so4_a2'][0, :, 0,0], marker='x', color='blue')
#_plt.plot(range(waccm_nlev), waccm_data_aerosol['waccm_so4_a3'][0, :, 0,0], marker='*', color='blue')
#_plt.plot(range(waccm_nlev), waccm_data_aerosol['waccm_ncl_a1'][0, :, 0,0], marker='.', color='yellow')
#_plt.plot(range(waccm_nlev), waccm_data_aerosol['waccm_ncl_a2'][0, :, 0,0], marker='x', color='yellow')
#_plt.plot(range(waccm_nlev), (waccm_data_aerosol['waccm_ncl_a3'][0, :, 0,0]/10.0), marker='*', color='yellow')
#_plt.plot(range(waccm_nlev), (waccm_data_aerosol['waccm_soa1_a1'][0, :, 0,0] + waccm_data_aerosol['waccm_soa2_a1'][0, :, 0,0] +
                             waccm_data_aerosol['waccm_soa3_a1'][0, :, 0,0] + waccm_data_aerosol['waccm_soa4_a1'][0, :, 0,0] + 
                             waccm_data_aerosol['waccm_soa5_a1'][0, :, 0,0]), marker='.', color='brown')
#_plt.plot(range(waccm_nlev), (waccm_data_aerosol['waccm_soa1_a2'][0, :, 0,0] + waccm_data_aerosol['waccm_soa2_a2'][0, :, 0,0] +
                             waccm_data_aerosol['waccm_soa3_a2'][0, :, 0,0] + waccm_data_aerosol['waccm_soa4_a2'][0, :, 0,0] + 
                             waccm_data_aerosol['waccm_soa5_a2'][0, :, 0,0]), marker='x', color='brown')

#plt.plot(range(waccm_nlev), waccm_data_aerosol['waccm_so4_a2'][0, :, 0,0], marker='x', color='brown')
#plt.plot(range(waccm_nlev), waccm_data_aerosol['waccm_so4_a3'][0, :, 0,0], marker='*', color='brown')
#_plt.show()

print "Aerosols as ug/m3 plotted over WACCM layers.  On X-axis, ToA is far left, Sea Level on far right."
#print "GRAY .: log 10 waccm_ncl_a1 at a corner"
#print "GRAY x: log 10 waccm_ncl_a2 at a corner"
#print "GRAY o: log 10 waccm_ncl_a3 at a corner"
print "BLUE .: waccm_so4_a1 at a corner"
print "BLUE x: waccm_so4_a2 at a corner"
print "BLUE o: waccm_so4_a3 at a corner"
print "YELLOW .: waccm_ncl_a1 at a corner"
print "YELLOW x: waccm_ncl_a2 at a corner"
print "YELLOW o: waccm_ncl_a3/10.0 at a corner"
print "BROWN .: waccm_soa*_a1 at a corner"
print "BROWN x: waccm_soa*_a1 at a corner"
print "Same plot code as for ug/m3 converted aerosols, below."
'''


# # SECTION 15 Transfer Aerosols and Numbers from WACCM space to BCON space, using cross-walk by Yunha.
print "SECTION 15 TRANSFER AEROSOLS and NUMBERS FROM WACCM SPACE TO BCON SPACE"

# Convert WACCM MAM4 aerosol species (list is in aerosol) to AERO6 (list is in BCON_aerosol),
# while using indices for copying from WACCM vertical layers to 
#       BCON veritcal layers using bc_lev_from_waccm_lev[tdx,ib,ilev].
# TEST WITH ONE TIME STEP
time_begin = time.time()

# waccm_ntime = 1 # TEST
perim_size = 1090 # TEST 

if ( not bcon_zeroed ):
    for tdx in range(waccm_ntime):
        print 'For WACCM Time index:', tdx
        for ib in range(perim_size):
            #print "... For BCON perimiter index ib: ", ib, "WACCN indices:",j_lat_w2b[ib], i_lon_w2b[ib]
            for ilev in range(bconmet_nlev):    #Vertical traverse bottom to top of BCON levels   
                print "......For BCON level index:", ilev
                W_levdx = bc_lev_from_waccm_lev[tdx,ib,ilev]
                W_lat = j_lat_w2b[ib]
                W_lon = i_lon_w2b[ib]
                # species by species copy, splittng and combining
    #ANH4J  comes from WACCM gases and was converted in SECTION 8.2 to ug/m3
                bcon_data_aerosol['bcon_ANH4J'][tdx,ilev,ib] = ( waccm_data_gas['waccm_NH4'][tdx,W_levdx,W_lat,W_lon] )

    #AECJ
                bcon_data_aerosol['bcon_AECJ'][tdx,ilev,ib] = (waccm_data_aerosol['waccm_bc_a1'][tdx,W_levdx,W_lat,W_lon] +
                                                             waccm_data_aerosol['waccm_bc_a4'][tdx,W_levdx,W_lat,W_lon] )       

    #ASOIL
                bcon_data_aerosol['bcon_ASOIL'][tdx,ilev,ib] = (waccm_data_aerosol['waccm_dst_a1'][tdx,W_levdx,W_lat,W_lon] +
                                                              waccm_data_aerosol['waccm_dst_a2'][tdx,W_levdx,W_lat,W_lon] +
                                                              waccm_data_aerosol['waccm_dst_a3'][tdx,W_levdx,W_lat,W_lon] )
    #ACLJ
                bcon_data_aerosol['bcon_ACLJ'][tdx,ilev,ib] = (0.607 * waccm_data_aerosol['waccm_ncl_a1'][tdx,W_levdx,W_lat,W_lon])
    #ANAJ
                bcon_data_aerosol['bcon_ANAJ'][tdx,ilev,ib] = (0.393 * waccm_data_aerosol['waccm_ncl_a1'][tdx,W_levdx,W_lat,W_lon])
    #ACLI
                bcon_data_aerosol['bcon_ACLI'][tdx,ilev,ib] = (0.607 * waccm_data_aerosol['waccm_ncl_a2'][tdx,W_levdx,W_lat,W_lon])
    #ANAI
                bcon_data_aerosol['bcon_ANAI'][tdx,ilev,ib] = (0.393 * waccm_data_aerosol['waccm_ncl_a2'][tdx,W_levdx,W_lat,W_lon])
    #ACLK
                bcon_data_aerosol['bcon_ACLK'][tdx,ilev,ib] = (0.607 * waccm_data_aerosol['waccm_ncl_a3'][tdx,W_levdx,W_lat,W_lon])
    #ANAK
                bcon_data_aerosol['bcon_ANAK'][tdx,ilev,ib] = (0.393 * waccm_data_aerosol['waccm_ncl_a3'][tdx,W_levdx,W_lat,W_lon])
    #APOCJ
                bcon_data_aerosol['bcon_APOCJ'][tdx,ilev,ib] = (0.333333333 * waccm_data_aerosol['waccm_pom_a1'][tdx,W_levdx,W_lat,W_lon] +
                                                              0.333333333 * waccm_data_aerosol['waccm_pom_a4'][tdx,W_levdx,W_lat,W_lon] )
    #APNCOMJ
                bcon_data_aerosol['bcon_APNCOMJ'][tdx,ilev,ib] = (0.666666667 * waccm_data_aerosol['waccm_pom_a1'][tdx,W_levdx,W_lat,W_lon] +
                                                                0.666666667 * waccm_data_aerosol['waccm_pom_a4'][tdx,W_levdx,W_lat,W_lon] )
    #ASO4J
                bcon_data_aerosol['bcon_ASO4J'][tdx,ilev,ib] = (1.0 * waccm_data_aerosol['waccm_so4_a1'][tdx,W_levdx,W_lat,W_lon])
    #ASO4I
                bcon_data_aerosol['bcon_ASO4I'][tdx,ilev,ib] = (1.0 * waccm_data_aerosol['waccm_so4_a2'][tdx,W_levdx,W_lat,W_lon])
    #ASO4K
                bcon_data_aerosol['bcon_ASO4K'][tdx,ilev,ib] = (1.0 * waccm_data_aerosol['waccm_so4_a3'][tdx,W_levdx,W_lat,W_lon])
    #AOLGAJ
                bcon_data_aerosol['bcon_AOLGAJ'][tdx,ilev,ib] = (0.329545455 * waccm_data_aerosol['waccm_soa1_a1'][tdx,W_levdx,W_lat,W_lon] +
                                                               0.329545455 * waccm_data_aerosol['waccm_soa2_a1'][tdx,W_levdx,W_lat,W_lon] +
                                                               0.329545455 * waccm_data_aerosol['waccm_soa3_a1'][tdx,W_levdx,W_lat,W_lon] +
                                                               0.329545455 * waccm_data_aerosol['waccm_soa4_a1'][tdx,W_levdx,W_lat,W_lon] +
                                                               0.329545455 * waccm_data_aerosol['waccm_soa5_a1'][tdx,W_levdx,W_lat,W_lon] )
    #AOLGBJ
                bcon_data_aerosol['bcon_AOLGBJ'][tdx,ilev,ib] = (0.670454545 * waccm_data_aerosol['waccm_soa1_a1'][tdx,W_levdx,W_lat,W_lon] +
                                                               0.670454545 * waccm_data_aerosol['waccm_soa2_a1'][tdx,W_levdx,W_lat,W_lon] +
                                                               0.670454545 * waccm_data_aerosol['waccm_soa3_a1'][tdx,W_levdx,W_lat,W_lon] +
                                                               0.670454545 * waccm_data_aerosol['waccm_soa4_a1'][tdx,W_levdx,W_lat,W_lon] +
                                                               0.670454545 * waccm_data_aerosol['waccm_soa5_a1'][tdx,W_levdx,W_lat,W_lon] )

    #NUMACC     CONVERSION FROM units [#/kg] to [#/m3] for Accumulation Mode was done in sect. 10, above.
                bcon_data_number['bcon_NUMACC'][tdx,ilev,ib] = (1.0 * waccm_data_aerosol['waccm_num_a1'][tdx,W_levdx,W_lat,W_lon] )
                # num_a4 not on WACCM files                 + 1.0 * waccm_data_aerosol['waccm_num_a4'][tdx,W_levdx,W_lat,W_lon] )

    #NUMATKN    NEEDS CONVERSION FACTOR FROM units [#/kg] to [#/m3] for Aitkin Mode
                bcon_data_number['bcon_NUMATKN'][tdx,ilev,ib] = (1.0 * waccm_data_aerosol['waccm_num_a2'][tdx,W_levdx,W_lat,W_lon])

    #NUMCOR     NEEDS CONVERSION FACTOR FROM units [#/kg] to [#/m3] for Coarse Mode
                bcon_data_number['bcon_NUMCOR'][tdx,ilev,ib] = (1.0 * waccm_data_aerosol['waccm_num_a3'][tdx,W_levdx,W_lat,W_lon])
    
    print bcon_data_number['bcon_{}'.format(num)][7,0,1089] 

else:
    # species by species copy, splittng and combining
    #ANH4J is calculated from WACCM gas phase NH4.  See note relflecting emails with Louisa Emmons. 
    bcon_data_aerosol['bcon_ANH4J'] = 0.0
    #AECJ
    bcon_data_aerosol['bcon_AECJ'] = 0.0    
    #ASOIL
    bcon_data_aerosol['bcon_ASOIL'] = 0.0
    #ACLJ
    bcon_data_aerosol['bcon_ACLJ'] = 0.0
    #ANAJ
    bcon_data_aerosol['bcon_ANAJ'] = 0.0
    #ACLI
    bcon_data_aerosol['bcon_ACLI'] = 0.0
    #ANAI
    bcon_data_aerosol['bcon_ANAI'] = 0.0
    #ACLK
    bcon_data_aerosol['bcon_ACLK'] = 0.0
    #ANAK
    bcon_data_aerosol['bcon_ANAK'] = 0.0
    #APOCJ
    bcon_data_aerosol['bcon_APOCJ'] = 0.0
    #APNCOMJ
    bcon_data_aerosol['bcon_APNCOMJ'] = 0.0
    #ASO4J
    bcon_data_aerosol['bcon_ASO4J'] = 0.0
    #ASO4I
    bcon_data_aerosol['bcon_ASO4I'] = 0.0
    #ASO4K
    bcon_data_aerosol['bcon_ASO4K'] = 0.0
    #AOLGAJ
    bcon_data_aerosol['bcon_AOLGAJ'] = 0.0
    #AOLGBJ
    bcon_data_aerosol['bcon_AOLGBJ'] = 0.0
    #NUMACC     
    bcon_data_number['bcon_NUMACC'] = 0.0               
    #NUMATKN    
    bcon_data_number['bcon_NUMATKN'] = 0.0
    #NUMCOR     
    bcon_data_number['bcon_NUMCOR'] = 0.0
    
    print bcon_data_number['bcon_{}'.format(num)][7,0,1089] 

            
print "Timing: ",(time.time() - time_begin)
    


# # SECTION 16  Transfer & Translate WACCM gas phase species from WACCM space to BCON  space.
print "SECTION 16  TRANSFER & TRANSLATE WACCM GAS PHASE SPECIES FROM WACCM SPACE TO BCON SPACE"

# Convert WACCM gas species (list is in WACCM_gases) to CB06 (list is in BCON_aerosol),
# while using indices for copying from WACCM vertical layers to 
#       BCON vertical layers using bc_lev_from_waccm_lev[tdx,ib,ilev].
# TEST WITH ONE TIME STEP
time_begin = time.time()

# waccm_ntime = 1 # TEST
# perim_size = 1090 # TEST 

if ( not bcon_zeroed ):
    
    for tdx in range(waccm_ntime):
        print 'For WACCM Time index:', tdx
        for ib in range(perim_size):
            #print "... For BCON perimiter index ib: ", ib, "WACCN indices:",j_lat_w2b[ib], i_lon_w2b[ib]
            for ilev in range(bconmet_nlev):    #Vertical traverse bottom to top of BCON levels   
                #print "......For BCON level index:", ilev
                # bc_lev_from_waccm_lev[ib,ilev], j_lat_w2b[ib], i_lon_w2b[ib] maps perimeter and level from WACCM to BCON.
                W_levdx = bc_lev_from_waccm_lev[tdx,ib,ilev]
                W_lat = j_lat_w2b[ib]
                W_lon = i_lon_w2b[ib]
                # species by species copy, splittng(?) and combining.
                #for itest in ( ("CO", "O3" ....) ): 
                #CH4
                bcon_data_gas['bcon_CH4'][tdx,ilev,ib] = (waccm_data_gas['waccm_CH4'][tdx,W_levdx,W_lat,W_lon])
                #CO
                bcon_data_gas['bcon_CO'][tdx,ilev,ib] = (waccm_data_gas['waccm_CO'][tdx,W_levdx,W_lat,W_lon])
                #CRES = f(CRESOL)
                bcon_data_gas['bcon_CRES'][tdx,ilev,ib] = (waccm_data_gas['waccm_CRESOL'][tdx,W_levdx,W_lat,W_lon] +
                                                         waccm_data_gas['waccm_PHENOL'][tdx,W_levdx,W_lat,W_lon] )
                #DMS
                bcon_data_gas['bcon_DMS'][tdx,ilev,ib] = (waccm_data_gas['waccm_DMS'][tdx,W_levdx,W_lat,W_lon])
                #ETH = f(C2H4)
                bcon_data_gas['bcon_ETH'][tdx,ilev,ib] = (waccm_data_gas['waccm_C2H4'][tdx,W_levdx,W_lat,W_lon])
                #ETHA = f(C2H6)
                bcon_data_gas['bcon_ETHA'][tdx,ilev,ib] = (waccm_data_gas['waccm_C2H6'][tdx,W_levdx,W_lat,W_lon])
                #ETOH = f(C2H5OH)
                bcon_data_gas['bcon_ETOH'][tdx,ilev,ib] = (waccm_data_gas['waccm_C2H5OH'][tdx,W_levdx,W_lat,W_lon])
                #H2O2
                bcon_data_gas['bcon_H2O2'][tdx,ilev,ib] = (waccm_data_gas['waccm_H2O2'][tdx,W_levdx,W_lat,W_lon])
                #HNO3
                bcon_data_gas['bcon_HNO3'][tdx,ilev,ib] = (waccm_data_gas['waccm_HNO3'][tdx,W_levdx,W_lat,W_lon])
                #ISPD = f( MVK + MACR, etc? )
                bcon_data_gas['bcon_ISPD'][tdx,ilev,ib] = (waccm_data_gas['waccm_MVK'][tdx,W_levdx,W_lat,W_lon] +
                                                         waccm_data_gas['waccm_MACR'][tdx,W_levdx,W_lat,W_lon])
                #MEOH
                bcon_data_gas['bcon_MEOH'][tdx,ilev,ib] = (waccm_data_gas['waccm_CH3OH'][tdx,W_levdx,W_lat,W_lon])
                #MEPX
                bcon_data_gas['bcon_MEPX'][tdx,ilev,ib] = (waccm_data_gas['waccm_CH3OOH'][tdx,W_levdx,W_lat,W_lon])

                #N2O5
                bcon_data_gas['bcon_N2O5'][tdx,ilev,ib] = (waccm_data_gas['waccm_N2O5'][tdx,W_levdx,W_lat,W_lon])
                #NH3
                bcon_data_gas['bcon_NH3'][tdx,ilev,ib] = (waccm_data_gas['waccm_NH3'][tdx,W_levdx,W_lat,W_lon])
                #NO
                bcon_data_gas['bcon_NO'][tdx,ilev,ib] = (waccm_data_gas['waccm_NO'][tdx,W_levdx,W_lat,W_lon])
                #NO2
                bcon_data_gas['bcon_NO2'][tdx,ilev,ib] = (waccm_data_gas['waccm_NO2'][tdx,W_levdx,W_lat,W_lon])
                #O3
                bcon_data_gas['bcon_O3'][tdx,ilev,ib] = (waccm_data_gas['waccm_O3'][tdx,W_levdx,W_lat,W_lon])
                #PAN
                bcon_data_gas['bcon_PAN'][tdx,ilev,ib] = (waccm_data_gas['waccm_PAN'][tdx,W_levdx,W_lat,W_lon])
                #SO2
                bcon_data_gas['bcon_SO2'][tdx,ilev,ib] = (waccm_data_gas['waccm_SO2'][tdx,W_levdx,W_lat,W_lon]) 
                #TOL
                bcon_data_gas['bcon_TOL'][tdx,ilev,ib] = (waccm_data_gas['waccm_TOLUENE'][tdx,W_levdx,W_lat,W_lon])
else:
    #CH4
    bcon_data_gas['bcon_CH4'] = 0.0
    #CO
    bcon_data_gas['bcon_CO'] = 0.0
    #CRES = f(CRESOL)
    bcon_data_gas['bcon_CRES'] = 0.0
    #DMS
    bcon_data_gas['bcon_DMS'] = 0.0
    #ETH = f(C2H4)
    bcon_data_gas['bcon_ETH'] = 0.0
    #ETHA = f(C2H6)
    bcon_data_gas['bcon_ETHA'] = 0.0
    #ETOH = f(C2H5OH)
    bcon_data_gas['bcon_ETOH'] = 0.0
    #H2O2
    bcon_data_gas['bcon_H2O2'] = 0.0
    #HNO3
    bcon_data_gas['bcon_HNO3'] = 0.0
    #ISPD = f( MVK + MACR, etc? )
    bcon_data_gas['bcon_ISPD'] = 0.0
    #MEOH
    bcon_data_gas['bcon_MEOH'] = 0.0
    #MEPX
    bcon_data_gas['bcon_MEPX'] = 0.0
    #N2O5
    bcon_data_gas['bcon_N2O5'] = 0.0
    #NH3
    bcon_data_gas['bcon_NH3'] = 0.0
    #NO
    bcon_data_gas['bcon_NO'] = 0.0
    #NO2
    bcon_data_gas['bcon_NO2'] = 0.0
    #O3
    bcon_data_gas['bcon_O3'] = 0.0
    #PAN
    bcon_data_gas['bcon_PAN'] = 0.0           
    #SO2
    bcon_data_gas['bcon_SO2'] = 0.0
    #TOL
    bcon_data_gas['bcon_TOL'] = 0.0

print "Timing: ", (time.time() -  time_begin)    


'''bcon_aerosols = ['ANH4J','AECJ','ASOIL','ACLJ','ANAJ','ACLI','ANAI','ANAJ','ACLK','ANAK',
                 'APOCJ','APNCOMJ','APOCJ','APNCOMJ','ASO4J','ASO4I','ASO4K','AOLGAJ',
                 'AOLGBJ','AOLGAJ','AOLGBJ','AOLGAJ','AOLGBJ','AOLGAJ','AOLGBJ','AOLGAJ','AOLGBJ']'''


# # SECTION 17 Transfer BCON space species to file and close file.
print "SECTION 17 TRANSFER BCON SPACE SPECIES TO FILE AND CLOSE FILE"

# write into file object for all species gas species and read the data, storing in the dictionary, zeroing it!

# loop over all BCON gas species and read those data, storing in that dictionary, zeroing it!

for gas in bcon_gases:
    print "BCON Gas is: ", gas # this lists each species name
    #bcon_redated.variables[gas] = bcon_data_gas[gas] 
    bcon_redated.variables[gas][:,:,:] = bcon_data_gas['bcon_{}'.format(gas)][:,:,:] 
    
# loop over all BCON aerosol species and read those data, storing in that dictionary, zeroing it!
for aerosol in bcon_aerosols:
    print "BCON Aerosol is: ", aerosol # this lists each aerosol name
    #bcon_redated.variables[aerosol] = bcon_data_aerosol[aerosol]
    bcon_redated.variables[aerosol][:,:,:] = bcon_data_aerosol['bcon_{}'.format(aerosol)][:,:,:]
        
# loop over all BCON number species and read those data, storing in that dictionary!
for num in bcon_nums:
    print "BCON Number is: ", num # this lists each number name
    #bcon_redated.variables[num] = bcon_data_number[num]
    bcon_redated.variables[num][:,:,:] = bcon_data_number['bcon_{}'.format(num)][:,:,:]
    
#bcon_redated.flush() 
dir(bcon_redated)
bcon_redated.sync()
bcon_redated.close()


print "END END END"

