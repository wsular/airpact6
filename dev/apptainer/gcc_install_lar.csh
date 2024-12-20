#!/bin/csh -f
set echo

#
#  Set HOME directory (which is the base directory for entire installation)
#
setenv HOME /opt/share

#
#  Install used tcsh and gcc/gfortran version 9.1.0 and openmpi
#

   /bin/tcsh --version
   gcc --version
   gfortran --version
#   module list | grep openmpi
   which mpirun

#
#  unset envioronment variables that would conflict with this installation
#

   unsetenv LDFLAGS
   unsetenv CPPFLAGS

#  --------------------------------------
# ....BUILD LIBRARIES
#  --------------------------------------

#  --------------------
#  Set directory for CMAQ Libraries 
#  -------------------

   mkdir -p $HOME/CMAQv5.5/LIBRARIES
   setenv INSTDIR $HOME/CMAQv5.5/LIBRARIES

# ----------------------
# Build and install curl
# ---------------------

 cd ${INSTDIR}
 wget https://curl.se/download/curl-8.10.1.tar.gz
 tar -xzvf curl-8.10.1.tar.gz
 cd curl-8.10.1
 ./configure --prefix=${INSTDIR} --without-ssl
 make |& tee make.curl.log
 make install |& tee make.install.curl.log

#  ----------------------
# Build and install zlib
#  ---------------------

  cd ${INSTDIR}
  wget https://sourceforge.net/projects/libpng/files/zlib/1.2.11/zlib-1.2.11.tar.gz
  tar -xzvf zlib-1.2.11.tar.gz
  cd zlib-1.2.11
  ./configure --prefix=${INSTDIR}
  make test |& tee make.test.log
  make install |& tee make.install.log

#  -----------------------
#  Download and build HDF5
#  -----------------------
   cd ${INSTDIR}
   wget https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.10/hdf5-1.10.5/src/hdf5-1.10.5.tar.gz
   tar xvf hdf5-1.10.5.tar.gz
#   rm -f hdf5-1.10.5.tar.gz
   cd hdf5-1.10.5
   setenv CFLAGS "-O3"
   setenv FFLAGS "-O3"
   setenv CXXFLAGS "-O3"
   setenv FCFLAGS "-O3"
   ./configure --prefix=${INSTDIR} --with-zlib=${INSTDIR}/include,${INSTDIR}/lib --enable-hl
   make |& tee make.gcc9.log 
#  make check > make.gcc9.check
   make install
#  ---------------------------
#  Download and build netCDF-C
#  ---------------------------
   cd  ${INSTDIR}
   wget https://github.com/Unidata/netcdf-c/archive/refs/tags/v4.8.0.tar.gz
   tar xvf v4.8.0.tar.gz
   cd netcdf-c-4.8.0
   setenv CPPFLAGS -I${INSTDIR}/include
   setenv LDFLAGS -L${INSTDIR}/lib
   ./configure --with-pic --enable-netcdf-4 --enable-shared --prefix=${INSTDIR}
   make |& tee  make.gcc9.log
   make install
#  ---------------------------------
#  Download and build netCDF-Fortran
#  ---------------------------------
   cd ${INSTDIR}
   wget https://github.com/Unidata/netcdf-fortran/archive/refs/tags/v4.5.3.tar.gz
   tar xvf v4.5.3.tar.gz
   cd netcdf-fortran-4.5.3
   ## Note, if non-standard locaions are used for the following compilers, you may need to specify their locations here: 
   setenv FC gfortran
   setenv F90 gfortran
   setenv F77 gfortran
   setenv CC gcc
   setenv CXX g++
   #setenv LIBS " -lnetcdf -lhdf5_hl -lhdf5 -lm -ldl -lz -lcurl "
   setenv NCDIR ${INSTDIR}
   setenv LIBS "-lnetcdf"
#   setenv CPPFLAGS -I${INSTDIR}/include
#   setenv LDFLAGS -L${INSTDIR}/lib
   setenv LD_LIBRARY_PATH ${INSTDIR}/lib:${LD_LIBRARY_PATH}
   ./configure --with-pic  --enable-shared --prefix=${INSTDIR}
   make |& tee make.gcc9.log 
   make install
#  -----------------------------
#  Download and build netCDF-CXX
#  -----------------------------
   cd  $INSTDIR
   wget https://github.com/Unidata/netcdf-cxx4/archive/refs/tags/v4.3.1.tar.gz
   tar xvf v4.3.1.tar.gz
   cd netcdf-cxx4-4.3.1
   ./configure --with-pic --enable-shared --prefix=$INSTDIR
   make |& tee  make.gcc9.log
   make install

#  --------------------------------------
# ....BUILD IOAPI
#  --------------------------------------

# Build I/O API version that supports NCF4 
# Note - this script works for gcc 9.1, to use gcc 10 and above, use the  -fallow-argument-mismatch argument
#  As of Aug. 28, 2020, there are now new BIN=Linux*gfort10* types and corresponding Makeinclude.Linux*gfort10* that incorporate this flag for the I/O API and M3Tools. 
# The above information is from the I/O API documentation: https://www.cmascenter.org/ioapi/documentation/all_versions/html/AVAIL.html

   cd $INSTDIR

#  --------------------------------------
#  Add  to the library path
#  --------------------------------------
   if (! $?LD_LIBRARY_PATH) then
      setenv  LD_LIBRARY_PATH $INSTDIR/lib
   else
     setenv  LD_LIBRARY_PATH ${LD_LIBRARY_PATH}:$INSTDIR/lib
   endif
   if (! $?PATH) then
      setenv  PATH $INSTDIR/lib
   else
     setenv  PATH ${PATH}:$INSTDIR/lib
   endif
#  ----------------------
#  Unpack and build IOAPI
#  ----------------------
   git clone https://github.com/cjcoats/ioapi-3.2
   cd ioapi-3.2
   git checkout -b 20200828
   setenv BASEDIR $INSTDIR/ioapi-3.2
   setenv BIN Linux2_x86_64gfort
   mkdir $BASEDIR/$BIN
   setenv CPLMODE nocpl
   # Edit Makefile or use syntax: make BIN=Linux2_x86_64pg  CPLMODE=nocpl INSTALL=$INSTDIR
   cd $BASEDIR/ioapi
   # Copy the Makefile template
   cp $BASEDIR/ioapi/Makefile.$CPLMODE  ${BASEDIR}/ioapi/Makefile
   cp ${BASEDIR}/m3tools/Makefile.$CPLMODE  ${BASEDIR}/m3tools/Makefile
   # Modify to specify the path of the netcdf libraries
   sed -i 's/\-lnetcdff/\-L\$\{HOME\}\/lib \-lnetcdff \-lnetcdf \-lhdf5_hl \-lhdf5 \-lm \-ldl \-lz \-lcurl/g' ${BASEDIR}/m3tools/Makefile
   # need updated Makefile to include ‘-DIOAPI_NCF4=1’ to the MFLAGS make-variable to avoid multiple definition of `nf_get_vara_int64_’
   # Makefile can be edited to use these options instead of the default options
   #    VFLAG  = -DVERSION='3.2-nocpl-ncf4'
   #    DEFINEFLAGS = -DIOAPI_NCF4=1 $(ARCHFLAGS) $(PARFLAGS)
   #This will remove # from the start of line 102 or add it if it wasn't already there:
   sed -i '102s/^#/\n/; 102s/^[^\n]/#&/; 102s/^\n//' Makefile
   sed -i '100s/^#/\n/; 100s/^[^\n]/#&/; 100s/^\n//' Makefile
   sed -i '109s/^#/\n/; 109s/^[^\n]/#&/; 109s/^\n//' Makefile
   sed -i '111s/^#/\n/; 111s/^[^\n]/#&/; 111s/^\n//' Makefile
   #sed -i -e 's/m64/m64 -DIOAPI_NCF4=1/g' Makeinclude.Linux2_x86_64gfort 
   make HOME=$INSTDIR | & tee make.ioapi.log
   cd $INSTDIR/ioapi-3.2/m3tools
   make HOME=$INSTDIR | & tee make.m3tools.log

#  --------------------------------------
# ....BUILD CCTM
#  --------------------------------------

#  -----------------------
#  Download and build CMAQ
#  -----------------------
# NOTE - please change the BUILD, CMAQ_HOME and OPENMPI directory to your local paths
# To find the openmpi path, search for mpirun, and then look for the include and lib directories
# > which mpirun
setenv BUILD $HOME/CMAQv5.5/LIBRARIES
setenv IOAPI_DIR $BUILD/ioapi-3.2/Linux2_x86_64gfort
setenv NETCDF_DIR $BUILD/lib
setenv NETCDFF_DIR $BUILD/lib
setenv OPENMPI $HOME/openmpi_4.0.1/
cd $BUILD/..
#git clone -b 55  https://github.com/USEPA/CMAQ/CMAQ.git CMAQ_REPO_v55
#git clone -b 5.5_testing ssh://github.com/lizadams/CMAQ_CMAS.git CMAQ_REPO_v55
git clone -b main https://github.com/USEPA/CMAQ.git CMAQ_REPO_v55

echo "downloaded CMAQv55"
cd $BUILD/../CMAQ_REPO_v55/
# Change CMAQ_HOME to a local directory
   #This will remove # from the start of line 102 or add it if it wasn't already there:
      sed -i '19s/^#/\n/; 19s/^[^\n]/#&/; 19s/^\n//' bldit_project.csh
      sed -i '20i set CMAQ_HOME = $HOME/CMAQv5.5/gcc_openmpi' bldit_project.csh

set CMAQ_HOME = $BUILD/../gcc_openmpi
mkdir $BUILD/../gcc_openmpi
./bldit_project.csh
source ./config_cmaq.csh gcc

# edit mcip MAKEFILE
cd ../gcc_openmpi/PREP/mcip/src

# edit config_cmaq.csh to specify the library locations
 cd $BUILD/../gcc_openmpi/
 sed -i '144i \       setenv BUILD $HOME/CMAQv5.5/LIBRARIES' config_cmaq.csh
 sed -i '145i \       setenv OPENMPI $HOME/openmpi_4.0.1/' config_cmaq.csh
 sed -i 's@ioapi_inc_gcc@$BUILD\/ioapi-3.2\/ioapi\/fixed_src@g' config_cmaq.csh
 sed -i 's@ioapi_lib_gcc@$BUILD\/ioapi-3.2\/Linux2_x86_64gfort@g' config_cmaq.csh
 sed -i 's@netcdf_lib_gcc@$BUILD\/lib@g' config_cmaq.csh
 sed -i 's@netcdf_inc_gcc@$BUILD\/include@g' config_cmaq.csh
 sed -i 's@netcdff_lib_gcc@$BUILD\/lib@g' config_cmaq.csh
 sed -i 's@netcdff_inc_gcc@$BUILD\/include@g' config_cmaq.csh
 sed -i 's@mpi_incl_gcc@$OPENMPI\/include@g' config_cmaq.csh
 sed -i 's@mpi_lib_gcc@$OPENMPI\/lib@g' config_cmaq.csh
 #edit the config_cmaq.csh to use -fopenmp due to it being used by default for I/O API Library
 sed -i '172i \       setenv myLINK_FLAG -fopenmp' config_cmaq.csh
 #edit the config_cmaq.csh to add extra libraries
 sed -i 's@-lnetcdf\"  #@-lnetcdf -lcurl -lhdf5 -lhdf5_hl \"  #@g'  config_cmaq.csh
cd $BUILD/../gcc_openmpi/CCTM/scripts/
 cp bldit_cctm.csh bldit_cctmv55_cb6r5_m3dry.csh
 # Add extra libs to support nc4 compression in config_cmaq.csh
 #  -lnetcdf -lhdf5_hl -lhdf5 -lm -ldl -lz -lcurl
  setenv extra_lib "-lnetcdf -lhdf5_hl -lhdf5 -lm -ldl -lz -lcurl"
 # Add openmp flag to match what was used in I/O API in config_cmaq.csh
 # setenv myLINK_FLAG  "-fopenmp" # openMP not supported w/ CMAQ
#./bldit_cctmv55_cb6r5_m3dry.csh gcc |& tee ./bldit_cctmv55_cb6r5_m3dry.log

# Verify that the executable was created.
#ls -rlt BLD_CCTM_v55_gcc_cb6r5_ae7_aq_m3dry/*.exe


#Note, to run CMAQ, please create modules or set the LD_LIBRARY_PATH to include the directories for $BUILD/lib at run time.

##see this tutorial for instructions to install modules: 
##https://pcluster-cmaq.readthedocs.io/en/latest/user_guide_pcluster/developers_guide/cmaq-vm/install.html#install-environment-modules
## If you have modules on your machine, you can create custom modules
## https://pcluster-cmaq.readthedocs.io/en/latest/user_guide_pcluster/developers_guide/cmaq-vm/install.html#create-custom-environment-module-for-libraries
