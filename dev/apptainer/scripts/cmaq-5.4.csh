#!/bin/csh -f

  # ....Consistent flags used to compile netcdf libraries
  #       without MPI
  setenv CFLAGS '-O3 -ffast-math -funroll-loops -m64'
  setenv FCFLAGS '-O3 -ffast-math -funroll-loops -m64 -fno-automatic -DAUTO_ARRAYS=1 -DF90=1 -DFLDMN=1 -DFSTR_L=int -DIOAPI_NO_STDOUT=1 -DNEED_ARGS=1'
  #       with MPI
  #setenv CFLAGS '-O3 -ffast-math -funroll-loops -m64 -fopenmp'
  #setenv FCFLAGS '-O3 -ffast-math -funroll-loops -m64 -fopenmp -DAUTO_ARRAYS=1 -DF90=1 -DFLDMN=1 -DFSTR_L=int -DIOAPI_NO_STDOUT=1 -DNEED_ARGS=1'

  # ....Compile ioapi-3.2
  echo "Compiling IOAPI..."
  setenv HOME /opt/share
  setenv INSTALL /opt/share/ioapi-3.2
  setenv BIN Linux2_x86_64gfort
  setenv LD_LIBRARY_PATH /usr/lib:/usr/local/lib:$LD_LIBRARY_PATH
  cd /opt/share/ioapi-3.2/ioapi
  #cp Makefile.pcdf Makefile 
  cp Makefile.nocpl Makefile 
  make

  # ....Compile m3tools
  echo "Compiling M3TOOLS..."
  cd /opt/share/ioapi-3.2/m3tools
  #cp /opt/share/airpact6/dev/apptainer/scripts/Makefile.m3tools Makefile
  #cp /opt/share/ioapi-3.2/m3tools/Makefile.pncf Makefile
  cp /opt/share/ioapi-3.2/m3tools/Makefile.nocpl Makefile
  make

  # ....Compile mcip
  echo "Compiling MCIP..."
  cd /opt/share/CMAQv54/PREP/mcip/src
  cp /opt/share/airpact6/dev/apptainer/scripts/Makefile.mcip Makefile
  make

  # ....Build-it for CMAQ routines (https://github.com/USEPA/CMAQ/blob/main/DOCS/Users_Guide/CMAQ_UG_ch05_running_a_simulation.md)
  echo "Building CMAQ..."
  cd /opt/share/CMAQv54
  cp /opt/share/airpact6/dev/apptainer/scripts/bldit_project.csh bldit_project.csh
  cp /opt/share/airpact6/dev/apptainer/scripts/config_cmaq.csh config_cmaq.csh
  setenv CMAQ_HOME /opt/share/CMAQv54
  chmod ugo+x bldit_project.csh
  ./bldit_project.csh
  ./config_cmaq.csh gcc 9.5.0

  # ....Compile icon
  echo "Compiling ICON..."
  cd $CMAQ_HOME/PREP/icon/scripts
  ./bldit_icon.csh gcc 9.5.0 > build_icon.log

  # ....Compile bcon
#  echo "Compiling BCON..."
#  cd $CMAQ_HOME/PREP/bcon/scripts
#  ./bldit_bcon.csh gcc 9.5.0 > build_bcon.log

  # ....Compile jproc
#  echo "Compiling JPROC..."
#  cd $CMAQ_HOME/UTIL/jproc/scripts
#  ./bldit_jproc.csh gcc 9.5.0 > build_jproc.log

  # ....Compile cctm
#  echo "Compiling CCTM..."
#  cd $CMAQ_HOME/CCTM/scripts
#  sed -i "s/ set shaID/# set shaID/g" bldit_cctm.csh
#  sed -i 's/echo "sha_ID/# echo "sha_ID/g' bldit_cctm.csh
#  ./bldit_cctm.csh gcc 9.5.0 > bldit_cctm.log
