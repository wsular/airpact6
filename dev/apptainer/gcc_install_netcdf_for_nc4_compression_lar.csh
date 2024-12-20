#!/bin/csh -f
set echo

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

#  --------------------
#  Set directory for CMAQ Libraries 
#  -------------------

   mkdir -p $cwd/CMAQv5.5/LIBRARIES
   setenv INSTDIR $cwd/CMAQv5.5/LIBRARIES

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