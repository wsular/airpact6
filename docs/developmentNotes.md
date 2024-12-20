# Development notes for AIRPACT6

## Useful information

- To connect to Azure VM

    ``` {zsh}
    ssh -i ~/.ssh/airpact6_key.pem vpwalden@airpact6.westus2.cloudapp.azure.com
    ```

- To create a shell into a Singularity container

  ```{zsh}
  sudo singularity shell -s /usr/bin/tcsh --writable  /work/cmaq.sif
  ```

---

## 10 January 2023

- Use update-alternatives for multiple gcc versions
  - https://man7.org/linux/man-pages/man1/update-alternatives.1.html
  - https://www.dedicatedcore.com/blog/install-gcc-compiler-ubuntu/
  - https://www.baeldung.com/linux/update-alternatives-command

---

## 12 October 2022

- Successfully created a Singularity sandbox that can process MCIP files from UW WRF !!

---

## 10 October 2022

- Use specific RPM packages in airpact.def that were used by Carlie Coats to build his singularity container

---

## 13 August 2022

- Error message with current version of airpact6.def

  ``` {zsh}
  /opt/ioapi-3.2/ioapi/modpdata.F90:34: Error: Can't open included file 'mpif.h'
  make: *** [modpdata.mod] Error 1
  FATAL:   While performing build: while running engine: exit status 2
  ```

- Command to build Singularity Image File

  ``` {zsh}
  sudo singularity build /work/airpact6.sif airpact6.def
  ```

  - And as a sandbox directory structure

    ``` {zsh}
    sudo singularity build --sandbox /work/airpact6.sif airpact6.def
    ```

---

## 27 June 2022

- How to download UW WRF data using secure copy from aeolus (b/c sshkeys have been set up)

  ```{zsh}
  scp empact@rainier.atmos.washington.edu:/home/disk/rainier_mm5rt/data/2022062700/wrfout_d3.2022062700.f07.0000 .
  ```

  - It is might be possible to setup sshkeys between rainier and gaia as well.

---

## 14 October 2021

- Unfortunately, I didn't document how I downloaded the following packages, so I re-downloaded most of them...
  - [netcdf](https://www.unidata.ucar.edu/downloads/netcdf/)
    - netcdf-f

    ``` {zsh}
    wget https://www.unidata.ucar.edu/downloads/netcdf/ftp/netcdf-fortran-4.5.3.tar.gz
    tar xvfz netcdf-fortran-4.5.3.tar.gz
    rm netcdf-fortran-4.5.3.tar.gz
    ```

    - netcdf-c

    ``` {zsh}
    wget https://downloads.unidata.ucar.edu/netcdf-c/4.8.1/src/netcdf-c-4.8.1.tar.gz
    tar xvfz netcdf-c-4.8.1.tar.gz
    rm netcdf-c-4.8.1.tar.gz
    ```

    - Probably downloaded from [UCAR](https://www.unidata.ucar.edu/downloads/netcdf/)
  - [ioapi](https://github.com/cjcoats/ioapi-3.2)
    - /home/vpwalden/models/ioapi-3.2
  
    ``` {zsh}
    cd models
    git clone https://github.com/cjcoats/ioapi-3.2.git
    ```

  - [Sparse Matrix Operator Kernel Emissions (SMOKE)](https://www.cmascenter.org/smoke/)
    - /home/vpwalden/models/smoke-v481
    - Downloaded from [CMAS](https://www.cmascenter.org/smoke/) after creating an account at CMAS

- Cloned [CMAQ v5.3.3](https://github.com/USEPA/CMAQ)
  - [CMAQ User's Guide](/home/vpwalden/models/CMAQ_REPO/DOCS/Users_Guide/PDF/CMAQv5.3.3_UG_08_17_2021.pdf)

  ``` {zsh}
  cd models
  git clone -b main https://github.com/USEPA/CMAQ.git CMAQ_REPO

  ``` {zsh}
  - Now trying to figure out how to build CMAQ using the gcc compiler
    - Not sure how to access the NVIDIA compiler yet
      - Should be nvfortran once it's installed...
  - Note that MCIP5.3 is packaged with CMAQ5.3.3

---

## 30 June 2021

- Set up virtual machine at Azure
  - CENTOS-8.3
  - 'yum search all compiler' shows installed compilers
    - gcc and gfortran have not been installed, or at least they are not on the path yet...
  - Installed Development Tools

    ``` {zsh}
    sudo dnf group install "Development Tools"
    ```

    - This installed gcc and gfortran
      - gcc --version

        ``` {zsh}
        [vpwalden@airpact6 ~]$ gcc --version
        gcc (GCC) 8.4.1 20200928 (Red Hat 8.4.1-1)
        Copyright (C) 2018 Free Software Foundation, Inc.
        This is free software; see the source for copying conditions.  There is NO
        warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
        ```

  - Installed the NVIDIA HPC SDK
    - [NVIDIA](https://developer.nvidia.com/nvidia-hpc-sdk-downloads)

      ``` {zsh}
      wget https://developer.download.nvidia.com/hpc-sdk/21.5/nvhpc_2021_215_Linux_x86_64_cuda_11.3.tar.gz
      tar xpzf nvhpc_2021_215_Linux_x86_64_cuda_11.3.tar.gz
      sudo nvhpc_2021_215_Linux_x86_64_cuda_11.3/install
      ```

    - Added compiler directory to path in .bashrc
