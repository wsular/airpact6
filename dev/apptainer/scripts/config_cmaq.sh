#!/bin/bash

# ================= CMAQv5.3.X Configuration Script ================= #
# Requirements: I/O API & netCDF libraries                            #
#               PGI, Intel, or Gnu Fortran compiler                   #
#               MPICH for multiprocessor computing                    #
# Optional:     Git for GitHub source code repository                 #
#                                                                     #
# Note that this script was configured/tested on Red Hat Linux O/S    #
#                                                                     #
# To report problems or request help with this script/program:        #
#             http://www.cmascenter.org/help-desk.cfm                 #
# =================================================================== #

#> Critical Folder Locations
 # CMAQ_HOME - this is where the config_cmaq.csh script is located. It
 # is also the root directory for all the executables. It may include 
 # the repository if the user is building CMAQ inside the repository. It
 # may, on the other hand, be outside the repository if the user has 
 # created a separate project directory where they wish to put build-
 # and run-scripts as well as executables.
 export CMAQ_HOME=$cwd

 # CMAQ_REPO - this is always the location of the CMAQ repository that
 # the user will pull from to create exectuables. If the user is building
 # CMAQ inside the repository then it will be equal to CMAQ_HOME. If not,
 # the user must supply an alternative folder locaiton.
 export CMAQ_REPO=/opt/share/CMAQ-5.3.3

 # CMAQ_DATA - this may be where the input data are located. It may be a 
 # symbolic link to another location on the system, but it should be
 # provided here
 export CMAQ_DATA=$CMAQ_HOME/data
 if ( ! -d $CMAQ_DATA ) then
     mkdir -p $CMAQ_DATA
 fi

 cd $CMAQ_HOME

#===============================================================================
#> architecture & compiler specific settings
#===============================================================================

#> Set the compiler option
 if ( $#argv == 1 ) then
    #> Use the user's input to set the compiler parameter
    export compiler=$1
    export compilerVrsn=Empty
 elif ( $#argv == 2 ) then
    #> Compiler Name and Version have been provided
    export compiler=$1
    export compilerVrsn=$2
 elif ( $#argv == 0 ) then
    #> If config.cmaq is called from Bldit.cctm or run.cctm, then this 
    #> variable is already defined
    if ( ! $?compiler ) then
      echo "Error: 'compiler' should be set either in the"
      echo "       environment or as input to config.cmaq"
      echo "       Example:> ./config.cmaq [compiler]"
      echo "       Options: intel | gcc | pgi"
      exit
    elif ( ! $?compilerVrsn ) then
      export compilerVrsn=Empty
    fi
 else
    #> More than two inputs were given. Exit this script just to
    #> be on the safe side.
    echo "Error: Too many inputs to config.cmaq. This script"
    echo "       is expecting one input (the name of the"
    echo "       desired compiler. In some installations, you "
    echo "       may also be able to specify the compiler version "
    echo "       as the second input, but this is not by default."
    exit
 fi
 echo "Compiler is set to $compiler"


#> Compiler flags and settings
 case $compiler in

#>  Intel fortran compiler......................................................
    intel)
       #> I/O API and netCDF root
       export NCDIR=netcdf_c_directory_path
       export NFDIR=netcdf_f_directory_path
       export NETCDF=netcdf_combined_directory_path # Note only for  WRF-CMAQ as it requires combining the netcdf C and netcdf F into a single directory. CMAQ users - don't change this setting
       export IOAPI=ioapi_root_intel
       export WRF_ARCH=15                           # [1-75] Optional, ONLY for WRF-CMAQ
       #> I/O API, netCDF, and MPI library locations
       export IOAPI_INCL_DIR   ${IOAPI}/ioapi_inc_intel    #> I/O API include header files
       export IOAPI_LIB_DIR    ${IOAPI}/ioapi_lib_intel    #> I/O API libraries

       if ( $NETCDF == "netcdf_combined_directory_path" ) then
           export NETCDF_LIB_DIR=${NCDIR}/lib                #> netCDF C directory path
           export NETCDF_INCL_DIR=${NCDIR}/include            #> netCDF C directory path
           export NETCDFF_LIB_DIR=${NFDIR}/lib                #> netCDF Fortran directory path
           export NETCDFF_INCL_DIR=${NFDIR}/include            #> netCDF Fortran directory path
       fi

       export MPI_INCL_DIR=mpi_incl_intel              #> MPI Include directory path
       export MPI_LIB_DIR=mpi_lib_intel               #> MPI Lib directory path

       #> Compiler Aliases and Flags
       #> set the compiler flag -qopt-report=5 to get a model optimization report in the build directory with the optrpt extension
       export myFC=mpiifort
       export myCC=icc
       export myFSTD="-O3 -fno-alias -mp1 -fp-model source -ftz -simd -align all -xHost -vec-guard-write -unroll-aggressive"
       export myDBG="-O0 -g -check bounds -check uninit -fpe0 -fno-alias -ftrapuv -traceback"
       export myLINK_FLAG=""     # -qopenmp # openMP may be required if I/O API was built using this link flag.
       export myFFLAGS="-fixed -132"
       export myFRFLAGS="-free"
       export myCFLAGS="-O2"
       export extra_lib=""
       ;;

#>  Portland Group fortran compiler.............................................
    pgi)

        #> I/O API and netCDF for WRF-CMAQ 
        export IOAPI=ioapi_root_pgi  
        export NCDIR=netcdf_c_directory_path
        export NFDIR=netcdf_f_directory_path
	export NETCDF=netcdf_combined_directory_path # Note only for  WRF-CMAQ as it requires combining the netcdf C and netcdf F into a single directory. CMAQ users - don't change this setting
        export WRF_ARCH=3                            # [1-75] Optional, ONLY for WRF-CMAQ  

        #> I/O API, netCDF, and MPI library locations
        export IOAPI_INCL_DIR=${IOAPI}/iopai_inc_pgi    #> I/O API include header files
        export IOAPI_LIB_DIR=${IOAPI}/ioapi_lib_pgi    #> I/O API libraries
	if ( $NETCDF == "netcdf_combined_directory_path" ) then
            export NETCDF_LIB_DIR=${NCDIR}/lib                      #> netCDF C directory path
            export NETCDF_INCL_DIR=${NCDIR}/include                      #> netCDF C directory path
            export NETCDFF_LIB_DIR=${NFDIR}/lib           #> netCDF Fortran directory path
            export NETCDFF_INCL_DIR=${NFDIR}/include           #> netCDF Fortran directory path
            export MPI_INCL_DIR=mpi_incl_pgi              #> MPI Include directory path
            export MPI_LIB_DIR=mpi_lib_pgi               #> MPI Lib directory path
        fi

        #> Compiler Aliases and Flags
        export myFC=mpifort
        export myCC=pgcc
        export myLINK_FLAG="" # "-mp"  openMP may be required if I/O API was built using this link flag.
        export myFSTD="-O3"
        export myDBG="-O0 -g -Mbounds -Mchkptr -traceback -Ktrap=fp"
        export myFFLAGS="-Mfixed -Mextend -mcmodel=medium -tp px"
        export myFRFLAGS="-Mfree -Mextend -mcmodel=medium -tp px"
        export myCFLAGS="-O2"
        export extra_lib=""
        ;;

#>  gfortran compiler............................................................
    gcc)

        #> I/O API and netCDF for WRF-CMAQ 
        export NCDIR=/usr/local                                        # C netCDF install path
        export NFDIR=/usr/local                                        # Fortran netCDF install path for CMAQ
	export NETCDF=netcdf_combined_directory_path                   # Note only for  WRF-CMAQ as it requires combining the netcdf C and netcdf F into a single directory. CMAQ users - don't change this setting
        export IOAPI=/opt/share/ioapi-3.2                              # I/O API 
        export WRF_ARCH=34                                             # [1-75] Optional, ONLY for WRF-CMAQ  

        #> I/O API, netCDF, and MPI library locations
        export IOAPI_INCL_DIR=${IOAPI}/ioapi                         #> I/O API include header files
        export IOAPI_LIB_DIR=${IOAPI}/Linux2_x86_64gfortmpi         #> I/O API libraries
	if ( $NETCDF == "netcdf_combined_directory_path" ) then
            export NETCDF_LIB_DIR=${NCDIR}/lib                       #> netCDF C directory path
            export NETCDF_INCL_DIR=${NCDIR}/include                   #> netCDF C directory path
            export NETCDFF_LIB_DIR=${NFDIR}/lib                       #> netCDF Fortran directory path
            export NETCDFF_INCL_DIR=${NFDIR}/include                   #> netCDF Fortran directory path
        fi

        export MPI_INCL_DIR=/usr/local                             #> MPI Include directory path
        export MPI_LIB_DIR=/usr/local                             #> MPI Lib directory path

        #> Compiler Aliases and Flags
        #> set the compiler flag -fopt-info-missed to generate a missed optimization report in the bldit logfile
        export myFC=mpifort
        export myCC=mpicc
        export myFSTD="-O3 -funroll-loops -finit-character=32 -Wtabs -Wsurprising -march=native -ftree-vectorize  -ftree-loop-if-convert -finline-limit=512"
        export myDBG="-Wall -O0 -g -fcheck=all -ffpe-trap=invalid,zero,overflow -fbacktrace"
        export myFFLAGS="-ffixed-form -ffixed-line-length-132 -funroll-loops -finit-character=32 -fallow-argument-mismatch"
        export myFRFLAGS="-ffree-form -ffree-line-length-none -funroll-loops -finit-character=32 -fallow-argument-mismatch"
        export myCFLAGS="-O2"
        export myLINK_FLAG="-fopenmp"  # openMP may be required if I/O API was built using this link flag. 
        export extra_lib=""
        ;;

    *)
        echo "*** Compiler $compiler not found"
        exit 2
        ;;

 esac

#> Apply Specific Module and Library Location Settings for those working inside EPA
 # source /work/MOD3DEV/cmaq_common/cmaq_env.csh  #>>> UNCOMMENT if at EPA

#> Add The Complier Version Number to the Compiler String if it's not empty
 export compilerString=${compiler}
 if ( $compilerVrsn != "Empty" ) then
    export compilerString=${compiler}${compilerVrsn}
 fi

#===============================================================================
 
#> I/O API, netCDF, and MPI libraries
 export netcdf_lib="-lnetcdf"  #> -lnetcdff -lnetcdf for netCDF v4.2.0 and later
 export netcdff_lib="-lnetcdff"
 export ioapi_lib="-lioapi"
 export pnetcdf_lib="-lpnetcdf"
 export mpi_lib="-lmpi" #> -lmpich or -lmvapich 

#> Query System Info and Current Working Directory
 export system="`uname -m`"
 export bld_os="`uname -s``uname -r | cut -d. -f1`"
 export lib_basedir=$CMAQ_HOME/lib

#> Generate Library Locations
 export CMAQ_LIB=${lib_basedir}/${system}/${compilerString}
 export MPI_DIR=$CMAQ_LIB/mpi
 export NETCDF_DIR=$CMAQ_LIB/netcdf
 export NETCDFF_DIR=$CMAQ_LIB/netcdff
 export PNETCDF_DIR=$CMAQ_LIB/pnetcdf
 export IOAPI_DIR=$CMAQ_LIB/ioapi

#> Create Symbolic Links to Libraries
 if ( ! -d $CMAQ_LIB ) then
     mkdir -p $CMAQ_LIB
 fi
 if (   -e $MPI_DIR  ) then
     rm -rf $MPI_DIR
 dfi
 mkdir $MPI_DIR
 ln -s $MPI_LIB_DIR $MPI_DIR/lib
 ln -s $MPI_INCL_DIR $MPI_DIR/include
 if ( ! -d $NETCDF_DIR ) then
     mkdir $NETCDF_DIR
 fi
 if ( ! -e $NETCDF_DIR/lib ) then
     ln -sfn $NETCDF_LIB_DIR $NETCDF_DIR/lib
 fi
 if ( ! -e $NETCDF_DIR/include ) then
     ln -sfn $NETCDF_INCL_DIR $NETCDF_DIR/include
 fi
 if ( ! -d $NETCDFF_DIR ) then
     mkdir $NETCDFF_DIR
 fi
 if ( ! -e $NETCDFF_DIR/lib ) then
     ln -sfn $NETCDFF_LIB_DIR $NETCDFF_DIR/lib
 fi
 if ( ! -e $NETCDFF_DIR/include ) then
     ln -sfn $NETCDFF_INCL_DIR $NETCDFF_DIR/include
 fi
 if ( ! -d $IOAPI_DIR ) then
    mkdir $IOAPI_DIR
    ln -sfn $IOAPI_INCL_DIR $IOAPI_DIR/include_files
    ln -sfn $IOAPI_LIB_DIR  $IOAPI_DIR/lib
 fi

#> Check for netcdf and I/O API libs/includes, error if they don't exist
 if ( ! -e $NETCDF_DIR/lib/libnetcdf.a ) then
    echo "ERROR: $NETCDF_DIR/lib/libnetcdf.a does not exist in your CMAQ_LIB directory!!! Check your installation before proceeding with CMAQ build."
    exit
 fi
 if ( ! -e $NETCDFF_DIR/lib/libnetcdff.a ) then
    echo "ERROR: $NETCDFF_DIR/lib/libnetcdff.a does not exist in your CMAQ_LIB directory!!! Check your installation before proceeding with CMAQ build."
    exit
 fi
 if ( ! -e $IOAPI_DIR/lib/libioapi.a ) then 
    echo "ERROR: $IOAPI_DIR/lib/libioapi.a does not exist in your CMAQ_LIB directory!!! Check your installation before proceeding with CMAQ build."
    exit
 fi
 if ( ! -e $IOAPI_DIR/lib/m3utilio.mod ) then 
    echo "ERROR: $IOAPI_MOD_DIR/m3utilio.mod does not exist in your CMAQ_LIB directory!!! Check your installation before proceeding with CMAQ build."
    exit
 fi

#> Set executable id
 export EXEC_ID=${bld_os}_${system}${compilerString}

