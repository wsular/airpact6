  !#/bin/tcsh

  # ....Compile ioapi-3.2
  echo "Compiling IOAPI..."
  setenv HOME /opt/share
  setenv INSTALL /opt/share/ioapi-3.2
  setenv BIN Linux2_x86_64gfortmpi
  setenv LD_LIBRARY_PATH /usr/lib:/usr/local/lib:/opt/share/Pnetcdf/lib:$LD_LIBRARY_PATH
  cd /opt/share/ioapi-3.2/ioapi
  cp /opt/share/airpact6/dev/apptainer/scripts/Makefile.ioapi Makefile
  cp /opt/share/airpact6/dev/apptainer/scripts/Makeinclude.Linux2_x86_64gfortmpi Makeinclude.Linux2_x86_64gfortmpi
  make -f Makefile

  # ....Compile m3tools
  echo "Compiling M3TOOLS..."
  cd /opt/share/ioapi-3.2/m3tools
  cp /opt/share/airpact6/dev/apptainer/scripts/Makefile.m3tools Makefile
  make -f Makefile

  # ....Compile mcip
  echo "Compiling MCIP..."
  cd /opt/share
  mv CMAQ CMAQ-5.3.3
  cd CMAQ-5.3.3/PREP/mcip/src
  cp /opt/share/airpact6/dev/apptainer/scripts/Makefile.mcip Makefile
  make -f Makefile

  # ....Build-it for CMAQ routines (https://github.com/USEPA/CMAQ/blob/main/DOCS/Users_Guide/CMAQ_UG_ch05_running_a_simulation.md)
  echo "Building CMAQ..."
  cd /opt/share/CMAQ-5.3.3
  cp /opt/share/airpact6/dev/apptainer/scripts/bldit_project.csh bldit_project.csh
  cp /opt/share/airpact6/dev/apptainer/scripts/config_cmaq.csh config_cmaq.csh
  setenv CMAQ_HOME /opt/share/CMAQ-5.3.3
  chmod ugo+x bldit_project.csh
  ./bldit_project.csh
  ./config_cmaq.csh gcc

  # ....Compile icon
  echo "Compiling ICON..."
  cd $CMAQ_HOME/PREP/icon/scripts
  ./bldit_icon.csh gcc 11.3.0 > build_icon.log

  # ....Compile bcon
  echo "Compiling BCON..."
  cd $CMAQ_HOME/PREP/bcon/scripts
  ./bldit_bcon.csh gcc 11.3.0 > build_bcon.log

  # ....Compile jproc
  echo "Compiling JPROC..."
  cd $CMAQ_HOME/UTIL/jproc/scripts
  ./bldit_jproc.csh gcc 11.3.0 > build_jproc.log

  # ....Compile cctm
  echo "Compiling CCTM..."
  cd $CMAQ_HOME/CCTM/scripts
  ./bldit_cctm.csh gcc 11.3.0 > build_cctm.log
