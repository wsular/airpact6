#!/bin/csh -f

  # ....Compile ioapi-3.2
  echo "Compiling IOAPI..."
  setenv NCDIR /usr/local
  setenv NFDIR /usr/local
  setenv HOME /opt/share
  setenv INSTALL $HOME/ioapi-3.2
  setenv BIN Linux2_x86_64gfort10
  setenv CPLMODE nocpl
  setenv LD_LIBRARY_PATH /usr/local/lib:/opt/share/ioapi-3.2/Linux2_x86_64gfort10:$LD_LIBRARY_PATH
  cd $INSTALL/ioapi
  git checkout -b 20200828
  sed -i 's/-fopenmp/# -fopenmp/g' Makeinclude.Linux2_x86_64gfort10
  cp Makefile.nocpl Makefile
  make

  # ....Compile m3tools
  echo "Compiling M3TOOLS..."
  cd $INSTALL/m3tools
  cp Makefile.nocpl Makefile
  sed -i 's\ LIBS = -L${OBJDIR} -lioapi -lnetcdff -lnetcdf $(OMPLIBS) $(ARCHLIB) $(ARCHLIBS)\ LIBS = -L${OBJDIR} -lioapi -L/usr/local/lib -lnetcdff -L/usr/local/lib -lnetcdf -lm -lnetcdf $(OMPLIBS) $(ARCHLIB) $(ARCHLIBS)\g' Makefile
  make

  # ....Compile mcip
  echo "Compiling MCIP..."
  cd $HOME
  mv CMAQ CMAQ-5.4
  setenv CMAQ_HOME $HOME/CMAQ-5.4
  cd $CMAQ_HOME/PREP/mcip/src
  cp $HOME/airpact6/dev/apptainer/scripts/Makefile.mcip Makefile
  make -f Makefile

  # ....Build-it for CMAQ routines (https://github.com/USEPA/CMAQ/blob/main/DOCS/Users_Guide/CMAQ_UG_ch05_running_a_simulation.md)
  echo "Building CMAQ..."
  cd $CMAQ_HOME
  cp /opt/share/airpact6/dev/apptainer/scripts/bldit_project.csh bldit_project.csh
  cp /opt/share/airpact6/dev/apptainer/scripts/config_cmaq.csh config_cmaq.csh
  chmod ugo+x bldit_project.csh
  ./bldit_project.csh
  ./config_cmaq.csh gcc 11.4.0

  # ....Compile icon
  echo "Compiling ICON..."
  cd $CMAQ_HOME/PREP/icon/scripts
  ./bldit_icon.csh gcc 11.4.0 > build_icon.log

  # ....Compile bcon
  echo "Compiling BCON..."
  cd $CMAQ_HOME/PREP/bcon/scripts
  ./bldit_bcon.csh gcc 11.4.0 > build_bcon.log

  # ....Compile jproc
  echo "Compiling JPROC..."
  cd $CMAQ_HOME/UTIL/jproc/scripts
  ./bldit_jproc.csh gcc 11.4.0 > build_jproc.log

  # ....Compile cctm
  echo "Compiling CCTM..."
  cd $CMAQ_HOME/CCTM/scripts
  ./bldit_cctm.csh gcc 11.4.0 > build_cctm.log
