# Utility for initializing our database tables, which will house metadata and 
# values for:
# - Model domain information
# - Model run information
# - Analysis values from model runs along with observations for analysis

import psycopg2
import os
import sys

cwd = os.getcwd()
parentWd = os.path.dirname(cwd)
sys.path.append(parentWd)
from Core import dbMod

def main():
    """
    Main function to initialize our tables
    """
    # Initialize our DB object
    dbObj = dbMod.dbObj()

    # Create our point observation tables
    cmd = """
    CREATE TABLE IF NOT EXISTS station_meta_streamflow (
        id SERIAL PRIMARY KEY,
        agency_name VARCHAR(64),
        agency_id VARCHAR(64),
        station_name VARCHAR(128),
        fnf_flag BOOL,
        latitude FLOAT,
        longitude FLOAT,
        units VARCHAR(16)
    );
    """
    dbObj.create_table(cmd)
    print("Successfully created station_meta_streamflow table!")

    cmd = """
    CREATE TABLE IF NOT EXISTS streamflow_obs (
        id INTEGER,
        discharge TIMESTAMPTZ
    );
    """
    dbObj.create_table(cmd)
    print("Successfully created streamflow_obs table!")

    # Create our model domain metadata table
    cmd = """
    CREATE TABLE IF NOT EXISTS model_domain_metadata (
        id SERIAL PRIMARY KEY,
        name VARCHAR(64),
        s3_domain_dir VARCHAR(512),
        dx_land INTEGER,
        dx_rt INTEGER
    );
    """
    dbObj.create_table(cmd)
    print("Successfully created model_domain_metadata table!")

    # Create our model run table
    cmd = """
    CREATE TABLE IF NOT EXISTS model_run_metadata(
        id SERIAL PRIMARY KEY,
        name VARCHAR(64),
        retro_flag BOOL,
        ana_flag BOOL,
        fcst_flag BOOL,
        ensemble_flag BOOL,
        forcing_source INTEGER,
        retro_beg_date TIMESTAMPTZ,
        retro_end_date TIMESTAMPTZ,
        fcst_hours INTEGER,
        num_ens_members INTEGER,
        forcing INTEGER,
        supp_forcing_precip INTEGER,
        physics_config INTEGER,
    );
    """
    dbObj.create_table(cmd)
    print("Successfully model_run_metadata table!")

    # Create our analysis tables

if __name__ == "__main__":
    main()