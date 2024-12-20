# Instructions for installing CMAQ

## Manual installation within apptainer

- Create container containing gcc, gfortran, openmpi, netcdf-C and netcdf-Fortran using [cmaq-5.4-ubuntu-22.04.def](file:///home/airpact/airpact6/dev/apptainer/cmaq-5.4_ubuntu-22.04.def)

- Follow instructions in [USEPA CMAQ tutorial on building libraries using gcc](https://github.com/USEPA/CMAQ/blob/main/DOCS/Users_Guide/Tutorials/CMAQ_UG_tutorial_build_library_gcc.md)

  - Log into the container using ```apptainer shell -f -w cmaq-5.4_ubuntu-22.04.def```
  ```
  csh

  which gfortran
  which gcc
  which g++

  setenv FC gfortran
  setenv CC gcc
  setenv CXX g++

  setenv NCDIR /usr/local
  setenv LD_LIBRARY_PATH  ${NCDIR}:${LD_LIBRARY_PATH}
  setenv CPPFLAGS -I${NCDIR}/include
  setenv NFDIR /usr/local
  setenv LD_LIBRARY_PATH  ${NFDIR}:${LD_LIBRARY_PATH}

  setenv CPPFLAGS -I${NCDIR}/include
  setenv LDFLAGS -L${NCDIR}/lib
  setenv LIBS "-lnetcdf"

  ldconfig
  ```