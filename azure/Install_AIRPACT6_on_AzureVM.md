# Installation of AIRPACT6 software on Azure VM

## Create an Azure VM running Centos 8.3

## SMOKE

1. Download SMOKE model
- CMAS website
  - GitHub site
  - 3 files that are needed

2. Set up correct shell
- sudo chsh -s /bin/csh vpwalden
  - Log out, then back in again
- Check shell type using ```echo $SHELL```

3. Unpack data
- Had to gzip files because install script expected them and I downloaded tar, not tar.gz; grrrr
    ```
    mkdir /home/vpwalden/models/smoke_v481
    source smoke_install_v481.csh
    ```

4. Library installations
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


