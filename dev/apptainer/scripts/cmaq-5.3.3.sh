  !#/bin/bash

  # ....Compile ioapi-3.2
  #     Now must switch to csh; grrrr
  export HOME=/opt/share
  export INSTALL=/opt/share/ioapi-3.2
  export BIN=Linux2_x86_64gfortmpi
  export LD_LIBRARY_PATH=/usr/lib:/usr/local/lib:/opt/share/Pnetcdf/lib:$LD_LIBRARY_PATH
  cd /opt/share/ioapi-3.2/ioapi
  cp /opt/share/airpact6/dev/apptainer/scripts/Makefile.ioapi Makefile
  cp /opt/share/airpact6/dev/apptainer/scripts/Makeinclude.Linux2_x86_64gfortmpi Makeinclude.Linux2_x86_64gfortmpi
  make -f Makefile

  # ....Compile m3tools
  cd /opt/share/ioapi-3.2/m3tools
  cp /opt/share/airpact6/dev/apptainer/scripts/Makefile.m3tools Makefile
  make -f Makefile

  # ....Compile mcip
  cd /opt/share
  mv CMAQ CMAQ-5.3.3
  cd CMAQ-5.3.3/PREP/mcip/src
  cp /opt/share/airpact6/dev/apptainer/scripts/Makefile.mcip Makefile
  make -f Makefile

  # ....Build-it for CMAQ routines (https://github.com/USEPA/CMAQ/blob/main/DOCS/Users_Guide/CMAQ_UG_ch05_running_a_simulation.md)
  cd /opt/share/CMAQ-5.3.3
  cp /opt/share/airpact6/dev/apptainer/scripts/bldit_project.csh bldit_project.csh
  cp /opt/share/airpact6/dev/apptainer/scripts/config_cmaq.csh config_cmaq.csh
  export CMAQ_HOME=/opt/share/CMAQ-5.3.3
  chmod ugo+x bldit_project.csh
  ./bldit_project.csh
  ./config_cmaq.csh gcc

  # ....Compile icon
  cd $CMAQ_HOME/PREP/icon/scripts
  ./bldit_icon.csh gcc 533 |& tee build_icon.log

  # ....Compile bcon
  cd $CMAQ_HOME/PREP/bcon/scripts
  ./bldit_bcon.csh gcc 533 |& tee build_bcon.log

  # ....Compile jproc
  cd $CMAQ_HOME/UTIL/jproc/scripts
  ./bldit_jproc.csh gcc 533 |& tee build_jproc.log

  # ....Compile cctm
  cd $CMAQ_HOME/CCTM/scripts
  ./bldit_cctm.csh gcc 533 |& tee build_cctm.log
