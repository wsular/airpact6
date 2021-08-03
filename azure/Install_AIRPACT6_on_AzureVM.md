# Installation of AIRPACT6 software on Azure VM

## Create an Azure VM running Centos 8.3

## Library installations
- Locations of libraries on aeolus is: ```/home/airpact5/AIRHOME/lib/CMAQ5.2/lib/x86_64/gcc```
  - this directory contains 3 directories for:
    - ioapi/lib
    ```
    include_files -> /home/lar/opt/ioapi-3.1/ioapi/fixed_src
    lib -> /home/lar/opt/ioapi-3.1/Linux2_x86_64pg_pgcc_nomp
    modules -> /home/lar/opt/ioapi-3.1/Linux2_x86_64pg_pgcc_nomp
    ```
    - mpi
      - Link to: ```/opt/openmpi-pgi/1.6```
    - netcdf/lib
      - Contains all the necessary files; installed here
        - ```libnetcdf.a``` and ```libnetcdf_c++.a``` are here
  - ioapi
    - [The EDSS/Models-3 I/O API](https://www.cmascenter.org/ioapi/documentation/all_versions/html/index.html)
      - [Build and installation instructions for I/O API Versions 3.0, 3.1, and 3.2](https://www.cmascenter.org/ioapi/documentation/all_versions/html/AVAIL.html#build)
  - mpi
    - [OPENMPI installation in CENTOS7](https://mfix.netl.doe.gov/forum/t/openmpi-installation-in-centos7/543)
      ```
      sudo yum install openmpi-devel
      module load mpi
      mpifort --version
      ```
  - netcdf
    - [netCDF-C 4.8.0](https://github.com/Unidata/netcdf-c/releases/v4.8.0)
    - [NetCDF Fortran Library](https://github.com/Unidata/netcdf-fortran)

## CMAQv5.3.2
- [CMAQv5.3.2 GitHub site](https://github.com/USEPA/CMAQ)
  ```
  git clone -b master https://github.com/USEPA/CMAQ.git CMAQ_REPO
  ```

## SMOKE
- [Installing SMOKE](https://www.cmascenter.org/smoke/documentation/4.8/html/ch12s03.html)

1. [Created an account at CMAS](https://www.cmascenter.org/register/create_account_action.cfm)
   
2. Download SMOKE model
- CMAS website
  - GitHub site
  - 3 files that are needed

3. Set up correct shell
- sudo chsh -s /bin/csh vpwalden
  - Log out, then back in again
- Check shell type using ```echo $SHELL```

4. Unpack data
- Had to gzip files because install script expected them and I downloaded tar, not tar.gz; grrrr
    ```
    mkdir /home/vpwalden/models/smoke_v481
    source smoke_install_v481.csh
    ```

