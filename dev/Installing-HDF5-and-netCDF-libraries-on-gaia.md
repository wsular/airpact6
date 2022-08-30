# Installing netCDF libraries on gaia

## 29 August 2022

### zlib on Ubuntu 22.04
- The zlib1g package is apparently installed as part of Ubuntu 22.04, so I did not install zlib manually.
  - zlib is needed by HDF5

### Install the HDF5 library
1. Navigate to the [HDF Group site](https://www.hdfgroup.org/downloads/hdf5/)
2. Scroll down and choose [Click here to obtain code for all platforms](https://www.hdfgroup.org/downloads/hdf5/)
3. Download the latest version of HDF5 by choosing on the tar.gz version.
   - Today the latest version is hdf5-1.12.2.tar.gz
4. Move this file to /opt and decompress it
   ```
   cd /home/vonw/Downloads
   sudo mv hdf5-1.12.2.tar.gz /opt/.
   cd /opt
   sudo tar xvfz hdf5-1.12.2.tar.gz
   ```
5. Make HDF5 (instructions from INSTALL_parallel in hdf5-1.12.2/release_notes directory)
   ```
   whereis mpicc      # Output /usr/bin/mpicc
   cd /opt
   sudo CC=/usr/bin/mpicc ./configure --enable-parallel --prefix=/opt/hdf5-1.12.2
   sudo make
   sudo make check
   sudo make install
   ```

### Install the netCDF libraries
4. Navigate to the [UCAR downloads page](https://downloads.unidata.ucar.edu)
5. Click on [NetCDF Libraries](https://downloads.unidata.ucar.edu/netcdf/)
6. Download the latest version of netCDF-C as source files in tar.gzip format by clicking on the appropriate link.
   - Today the latest version is 4.9.0
7. Download the latest version of netCDF-FORTRAN as source files in tar.gzip format by clicking on the appropriate link.
   - Today the latest version is 4.6.0
8. Move these files to /opt
   ```
   cd /home/vonw/Downloads
   sudo mv netcdf-c-4.9.0.tar.gz /opt/.
   sudo mv netcdf-fortran-4.6.0.tar.gz /opt/.
   ```
9.  Navigate to the /opt directory
   ```
   cd /opt
   ```
11. Unzip and untar both files
   ```
   sudo tar xfvz netcdf-c-4.9.0.tar.gz
   sudo tar xfvz netcdf-fortran-4.6.0.tar.gz
   ```
   - This creates two directories in /opt that contain the source code.
11. blaq
12. 