# %%
YEAR  = '2024'
MONTH = '12'
DAY   = '15'

# run_emis_anthro.csh ###########################################
smoke = {}
smoke['AIRBASE']      = '/home/airpact/airpact6/amin_mirror/'
smoke['AIRHOME']      = smoke['AIRBASE'] + 'AIRHOME/'
smoke['AIRRUN']       = smoke['AIRBASE'] + 'AIRRUN/' + YEAR + '/'
smoke['AIROUT']       = smoke['AIRRUN'] + YEAR + MONTH + DAY + '/'
smoke['AIRLOGDIR']    = smoke['AIROUT'] + 'logs/'
smoke['MCIPROOT']     = smoke['AIROUT']
smoke['MCIPDIR']      = smoke['MCIPROOT'] + YEAR + MONTH + DAY + '00/mcip/'
smoke['EMIS_WORKDIR'] = smoke['AIRHOME'] + 'run_ap6_day1/emis/'

smoke['YYYYMMDD'] = YEAR + MONTH + DAY
smoke['RUN_SMKREPORT'] = 'Y'
smoke['IOAPI_LOG_WRITE'] = 'FALSE'
smoke['logdir'] = smoke['AIRLOGDIR'] + 'emis/anthro/'

# run_smk_temporal.csh ##########################################
smoke['SMK_HOME'] = '/home/airpact/models/SMOKE/V5.1/'
smoke['SMK_SUBSYS'] = smoke['SMK_HOME'] + 'subsys/'
smoke['SMK_ROOT'] = smoke['SMK_SUBSYS'] + 'smoke/'
smoke['SMKDAT'] = smoke['SMK_HOME'] + 'data/'
smoke['ASSIGNS'] = smoke['EMIS_WORKDIR'] + 'anthro/assigns/'
smoke['SMOKE_EXE'] = 'Linux2_x86_64ifx/'
smoke['SMK_BIN'] = smoke['SMK_ROOT'] + smoke['SMOKE_EXE']
smoke['MD_SRC'] = smoke['SMK_ROOT'] + 'src/emmod/'
smoke['SMKINC'] = smoke['SMK_ROOT'] + 'src/inc/'
smoke['GE_DAT'] = smoke['SMK_HOME'] + 'data/ge_dat/'

# smk_point.csh #################################################
## Set Assigns file name
smoke['ASSIGNS_FILE'] = smoke['ASSIGNS'] + 'ASSIGNS.AP6.cmaq.cb05_soa.csh'

## Set source category
smoke['SMK_SOURCE'] = 'P'
smoke['MRG_SOURCE'] = 'P'

## Time-independent programs
smoke['RUN_SMKINVEN'] = 'N'
smoke['RUN_SPCMAT'] = 'N'
smoke['RUN_GRDMAT'] = 'N'

## Time-dependent programs
smoke['RUN_TEMPORAL'] = 'Y'
smoke['RUN_ELEVPOINT'] = 'Y'
smoke['RUN_LAYPOINT'] = 'Y'
smoke['RUN_SMKMERGE'] = 'Y'
smoke['RUN_PING'] = 'Y'

## Quality assurance
smoke['RUN_SMKREPORT'] = 'N'

## Program-specific controls...

## For Smkinven
smoke['CHECK_STACKS_YN'] = 'Y'
smoke['FILL_ANNUAL'] = 'N'
smoke['FLOW_RATE_FACTOR'] = 15878
smoke['HOURLY_TO_DAILY'] = 'N'
smoke['HOURLY_TO_PROFILE'] = 'Y'
smoke['IMPORT_AVEINV_YN'] = 'N'
smoke['RAW_DUP_CHECK'] = 'N'
smoke['SMK_BASEYR_OVERRIDE'] = 0
smoke['SMK_DEFAULT_TZONE'] = 5
smoke['SMK_NHAPEXCLUDE_YN'] = 'N'
smoke['NONHAP_TYPE'] = 'TOG'
smoke['SMKINVEN_FORMULA'] = 'PMC=PM10-PM2_5'
smoke['WEST_HSPHERE'] = 'Y'
smoke['WKDAY_NORMALIZE'] = 'N'
smoke['WRITE_ANN_ZERO'] = 'N'
smoke['ALLOW_NEGATIVE'] = 'N'

## For Grdmat
# ....set by Assigns file

## For Spcmat
smoke['POLLUTANT_CONVERSION'] = 'Y'

## For Spcmat
smoke['SMK_ELEV_METHOD'] = 1
smoke['PELVCONFIG'] = smoke['GE_DAT'] + 'pelvconfig_inline_20m_13nov2012_v0.txt'

## For Temporal
smoke['RENORM_TPROF'] = 'N'
smoke['UNIFORM_TPROF_YN'] = 'N'
smoke['ZONE4WM'] = 'Y'

## For Laypoint
smoke['FIRE_AREA'] = 0.
smoke['FIRE_HFLUX'] = 0.
smoke['FIRE_PLUME_YN'] = 'N'
smoke['HOUR_PLUMEDATA_YN'] = 'N'
smoke['HOURLY_FIRE_YN'] = 'N'
smoke['REP_LAYER_MAX'] = -1
smoke['SMK_SPECELEV_YN'] = 'Y'
smoke['VERTICAL_SPREAD'] = 0
smoke['USE_EDMS_DATA_YN'] = 'N'
smoke['PLUME_GTEMP_NAME'] = 'TEMPG' 

## For Smkmerge
smoke['MRG_LAYERS_YN'] = 'Y'
smoke['MRG_SPCMAT_YN'] = 'Y'
smoke['MRG_TEMPORAL_YN'] = 'Y'
smoke['MRG_GRDOUT_YN'] = 'Y'
smoke['MRG_REPCNY_YN'] = 'Y'
smoke['MRG_REPSTA_YN'] = 'N'
smoke['MRG_TOTOUT_UNIT'] = 'moles/s'
smoke['MRG_ASCIIELEV_UNIT'] = 'moles/day'
smoke['SMK_ASCIIELEV_YN'] = 'N'
smoke['SMK_REPORT_TIME'] = 230000

## For Smkreport
smoke['REPORT_ZERO_VALUES'] = 'N'

## Multiple-program controls
smoke['DAY_SPECIFIC_YN'] = 'N'
smoke['EXPLICIT_PLUME_YN'] = 'N'
smoke['HOUR_SPECIFIC_YN'] = 'N'
smoke['OUTZONE'] = 0
smoke['REPORT_DEFAULTS'] = 'N'
smoke['SMK_EMLAYS'] = 37
smoke['SMK_AVEDAY_YN'] = 'N'
smoke['SMK_MAXERROR'] = 100
smoke['SMK_MAXWARNING'] = 100
smoke['SMK_PING_METHOD'] = 1
smoke['VELOC_RECALC'] = 'N'

## Script settings
smoke['SRCABBR'] = 'point'
smoke['QA_TYPE'] = 'all'
smoke['PROMPTFLAG'] = 'N'
smoke['AUTO_DELETE'] = 'Y'
smoke['AUTO_DELETE_LOG'] = 'Y'
smoke['DEBUGMODE'] = 'N'
smoke['DEBUG_EXE'] = 'pgdbg'

## Runtime
#smoke['LOGDIR'] = smoke['AIRLOGDIR'] + 'emis/anthro/' + smoke['SRCABBR']
#smoke['RUN_PART1'] = 'Y'

# !!! source $ASSIGNS_FILE   # Invoke Assigns file

#smoke['NHAPEXCLUDE'] = smoke['INVDIR' + 'other/nhapexclude.all.txt'

# !!! source ${EMIS_WORKDIR}/anthro/temporal/smk_run_gaia.csh     # Run programs
# !!! source ${EMIS_WORKDIR}/anthro/temporal/qa_run.csh      # Run QA for part 1
#smoke['RUN_PART1'] = 'N'


# %%
