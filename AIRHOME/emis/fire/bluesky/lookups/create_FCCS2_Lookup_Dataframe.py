#%%
#Emissions Lookfup for FCCS
WF_PM25dict = eval(open('/home/airpact/AIRHOME/emis/fire/bluesky/lookups/WF_PM25.csv').read())
RX_PM25dict = eval(open('/home/airpact/AIRHOME/emis/fire/bluesky/lookups/RX_PM25.csv').read())
WF_PM10dict = eval(open('/home/airpact/AIRHOME/emis/fire/bluesky/lookups/WF_PM10.csv').read())
RX_PM10dict = eval(open('/home/airpact/AIRHOME/emis/fire/bluesky/lookups/RX_PM10.csv').read())
WF_COdict   = eval(open('/home/airpact/AIRHOME/emis/fire/bluesky/lookups/WF_CO.csv').read())
RX_COdict   = eval(open('/home/airpact/AIRHOME/emis/fire/bluesky/lookups/RX_CO.csv').read())
WF_NOxdict = eval(open('/home/airpact/AIRHOME/emis/fire/bluesky/lookups/WF_NOx.csv').read())
RX_NOxdict = eval(open('/home/airpact/AIRHOME/emis/fire/bluesky/lookups/RX_NOx.csv').read())
WF_NH3dict = eval(open('/home/airpact/AIRHOME/emis/fire/bluesky/lookups/WF_NH3.csv').read())
RX_NH3dict = eval(open('/home/airpact/AIRHOME/emis/fire/bluesky/lookups/RX_NH3.csv').read())
WF_SO2dict = eval(open('/home/airpact/AIRHOME/emis/fire/bluesky/lookups/WF_SO2.csv').read())
RX_SO2dict = eval(open('/home/airpact/AIRHOME/emis/fire/bluesky/lookups/RX_SO2.csv').read())
WF_VOCdict = eval(open('/home/airpact/AIRHOME/emis/fire/bluesky/lookups/WF_VOC.csv').read())
RX_VOCdict = eval(open('/home/airpact/AIRHOME/emis/fire/bluesky/lookups/RX_VOC.csv').read())

WF_HEATdict = eval(open('/home/airpact/AIRHOME/emis/fire/bluesky/lookups/WF_HEAT.csv').read())
RX_HEATdict = eval(open('/home/airpact/AIRHOME/emis/fire/bluesky/lookups/RX_HEAT.csv').read())

#Using flaming consumption lookups
WF_CONSFdict = eval(open('/home/airpact/AIRHOME/emis/fire/bluesky/lookups/WF_cons_flam.csv').read())
RX_CONSFdict = eval(open('/home/airpact/AIRHOME/emis/fire/bluesky/lookups/RX_cons_flam.csv').read())

#Vegataion Names for FFCS
VEG_dict = eval(open('/home/airpact/AIRHOME/emis/fire/bluesky/lookups/fccs2_lookup.csv').read())

#%% convert dict to dataframe
WF_PM25 = pd.DataFrame.from_dict(WF_PM25dict, orient='index', columns=['WF_PM25'])
RX_PM25 = pd.DataFrame.from_dict(RX_PM25dict, orient='index', columns=['RX_PM25'])
WF_PM10 = pd.DataFrame.from_dict(WF_PM10dict, orient='index', columns=['WF_PM10'])
RX_PM10 = pd.DataFrame.from_dict(RX_PM10dict, orient='index', columns=['RX_PM10'])
WF_CO = pd.DataFrame.from_dict(WF_COdict, orient='index', columns=['WF_CO'])
RX_CO = pd.DataFrame.from_dict(RX_COdict, orient='index', columns=['RX_CO'])
WF_NOx = pd.DataFrame.from_dict(WF_NOxdict, orient='index', columns=['WF_NOx'])
RX_NOx = pd.DataFrame.from_dict(RX_NOxdict, orient='index', columns=['RX_NOx'])
WF_NH3 = pd.DataFrame.from_dict(WF_NH3dict, orient='index', columns=['WF_NH3'])
RX_NH3 = pd.DataFrame.from_dict(RX_NH3dict, orient='index', columns=['RX_NH3'])
WF_SO2 = pd.DataFrame.from_dict(WF_SO2dict, orient='index', columns=['WF_SO2'])
RX_SO2 = pd.DataFrame.from_dict(RX_SO2dict, orient='index', columns=['RX_SO2'])
WF_VOC = pd.DataFrame.from_dict(WF_VOCdict, orient='index', columns=['WF_VOC'])
RX_VOC = pd.DataFrame.from_dict(RX_VOCdict, orient='index', columns=['RX_VOC'])

WF_HEAT = pd.DataFrame.from_dict(WF_HEATdict, orient='index', columns=['WF_HEAT'])
RX_HEAT = pd.DataFrame.from_dict(WF_HEATdict, orient='index', columns=['RX_HEAT'])

WF_CONSF = pd.DataFrame.from_dict(WF_CONSFdict, orient='index', columns=['WF_CONSF'])
RX_CONSF = pd.DataFrame.from_dict(RX_CONSFdict, orient='index', columns=['RX_CONSF'])

VEG = pd.DataFrame.from_dict(VEG_dict, orient='index', columns=['Vegetation'])

#%% Merge dataframes
df = VEG
df = df.join(WF_PM25)
df = df.join(RX_PM25)
df = df.join(WF_PM10)
df = df.join(RX_PM10)
df = df.join(WF_CO)
df = df.join(RX_CO)
df = df.join(WF_NOx)
df = df.join(RX_NOx)
df = df.join(WF_NH3)
df = df.join(RX_NH3)
df = df.join(WF_SO2)
df = df.join(RX_SO2)
df = df.join(WF_VOC)
df = df.join(RX_VOC)

df = df.join(WF_HEAT)
df = df.join(RX_HEAT)
df = df.join(WF_CONSF)
df = df.join(RX_CONSF)

#%% Change column type
df.index = df.index.astype(int)
for key in df.keys():
    if key != 'Vegetation':
        df[key] = df[key].astype(float)

#%% Save dataframe as a csv
df.to_csv('/home/airpact/AIRHOME/emis/fire/bluesky/fccs2_lookup.csv')

#%%
