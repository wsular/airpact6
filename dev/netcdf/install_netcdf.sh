#!/bin/bash
## NETCDF installation script.
# Download and install required library and data files for HDF and netCDF.
# Derived from https://gist.github.com/everdaniel/8a6e1d2b8cbfd048ec63b67ea7642e4f by Jamal Khan <jamal.khan@legos.obs-mip.fr>

# basic package managment
sudo apt update
sudo apt upgrade

## Directory Listing
export HOME=`/home/vonw/data/airpact6`
cd $HOME/netcdf
mkdir Downloads
mkdir Library

## Downloading Libraries
cd Downloads
wget -c https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.13/hdf5-1.13.1/src/hdf5-1.13.1.tar.gz
wget -c https://www.unidata.ucar.edu/downloads/netcdf/ftp/netcdf-c-4.8.1.tar.gz
wget -c https://www.unidata.ucar.edu/downloads/netcdf/ftp/netcdf-fortran-4.5.4.tar.gz

# Compilers
export DIR=$HOME/WRF/Library
export CC=gcc
export CXX=g++
export FC=gfortran
export F77=gfortran

# hdf5 library for netcdf4 functionality
cd $HOME/WRF/Downloads
tar -xvzf hdf5-1.10.5.tar.gz
cd hdf5-1.10.5
./configure --prefix=$DIR --with-zlib=$DIR --enable-hl --enable-fortran
make check
make install

export HDF5=$DIR
export LD_LIBRARY_PATH=$DIR/lib:$LD_LIBRARY_PATH

## Install NETCDF C Library
cd $HOME/WRF/Downloads
tar xzvf netcdf-c-4.7.1.tar.gz
cd netcdf-c-4.7.1/
export CPPFLAGS=-I$DIR/include 
export LDFLAGS=-L$DIR/lib
./configure --prefix=$DIR --disable-dap
make check
make install

export PATH=$DIR/bin:$PATH
export NETCDF=$DIR

## NetCDF fortran library
cd $HOME/WRF/Downloads
tar -xvzf netcdf-fortran-4.5.1.tar.gz
cd netcdf-fortran-4.5.1/
export LD_LIBRARY_PATH=$DIR/lib:$LD_LIBRARY_PATH
export CPPFLAGS=-I$DIR/include 
export LDFLAGS=-L$DIR/lib
export LIBS="-lnetcdf -lhdf5_hl -lhdf5 -lz" 
./configure --prefix=$DIR --disable-shared
make check
make install

