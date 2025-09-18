#!/usr/bin/bash

# Top level bash script to build out our processing istance, which 
# shares a mounted drive with the HydroInspector instance

# First install our necessary packages
sudo dnf update -y
sudo dnf install postgresql15 -y
sudo dnf install wget -y
sudo dnf install unzip -y

# Change the permissions of our mounted directory
sudo chmod -R a+rwx /data

# Download our bash_profile
# TODO


# Install mamba
cd /data
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh
# IMPORTANT - Ensure you specify /data/miniforge in data installation directory

# Install Mamba
conda config --add channels conda-forge
conda update -n base --all
conda install -n base mamba 

# Create our Mamba environment for dealing with GDAL with NetCDF support
mamba create -n gdal_nc -c conda-forge gdal=3.11 libgdal-netcdf netcdf4 boto3 slack_sdk
mamba create -n obs_ingest -c conda-forge psycopg2