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
        obs_date TIMESTAMPTZ,
        discharge FLOAT
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
        dx_hydro INTEGER,
        lake_flag BOOL,
        reach_based_stack BOOL,
        version_label VARCHAR(64),
        parent_domain_id INTEGER,
        parent_domain_x1 INTEGER,
        parent_domain_x2 INTEGER,
        parent_domain_y1 INTEGER,
        parent_domain_y2 INTEGER
    );
    """
    dbObj.create_table(cmd)
    print("Successfully created model_domain_metadata table!")

    # Create our physics configuration table. 
    cmd = """
    CREATE TABLE IF NOT EXISTS model_physics_config (
        id SERIAL PRIMARY KEY,
        name VARCHAR(64),
        forcing_timestep_hours INTEGER,
        lsm_timestep_hours INTEGER,
        num_soil_layers INTEGER,
        rstrt_swc INTEGER,
        subrtswcrt INTEGER,
        ovrtswcrt INTEGER,
        rt_option INTEGER,
        channrtswcrt INTEGER,
        channel_option INTEGER,
        dtrt_ch INTEGER,
        dtrt_ter INTEGER,
        soil_override INTEGER,
        compound_channel BOOL,
        gwbaseswcrt INTEGER,
        bucket_loss INTEGER,
        udmp_opt INTEGER,
        imperv_adj INTEGER,
        dyn_veg_opt INTEGER,
        can_stom_res_opt INTEGER,
        btr_opt INTEGER,
        runoff_opt INTEGER,
        sfc_drag_opt INTEGER,
        frozen_soil_opt INTEGER,
        supercool_water_opt INTEGER,
        rad_transfer_opt INTEGER,
        snow_albedo_opt INTEGER,
        pcp_partition_opt INTEGER,
        tbot_opt INTEGER,
        temp_time_scheme INTEGER,
        glacier_opt INTEGER,
        sfc_res_opt INTEGER,
        imperv_opt INTEGER,
        lsm_only BOOL
    );
    """
    dbObj.create_table(cmd)
    print("Successfully created model_physics_config table!")

    # Create our forcing ingest metadata table
    cmd = """
    CREATE TABLE IF NOT EXISTS forcing_ingest_metadata(
        id SERIAL PRIMARY KEY,
        name VARCHAR(32),
        key_lookup INTEGER,
        data_format VARCHAR(16),
        ftp_source BOOL,
        aws_s3_source BOOL,
        ftp_url VARCHAR(256),
        s3_source_bucket VARCHAR(64),
        s3_source_directory VARCHAR(128),
        s3_login_req BOOL,
        cycle_freq INTEGER,
        forcing_freq INTEGER,
        cycle_duration INTEGER,
        t0_flag BOOL,
        s3_out_dir VARCHAR(128),
        lagHours INTEGER,
        conversionFlag BOOL
    );
    """
    dbObj.create_table(cmd)
    print("Successfully created forcing_ingest_metadata table!")

    # Create our forcing entry table
    cmd = """
    CREATE TABLE IF NOT EXISTS forcing_ingest_entry(
        id SERIAL PRIMARY KEY,
        key_lookup INTEGER,
        reanalysis_flag BOOL,
        cycle_date TIMESTAMPTZ,
        forecast_date TIMESTAMPTZ,
        forecast_hour INTEGER,
        s3_dir VARCHAR(256)
    );
    """
    dbObj.create_table(cmd)
    print("Successfully created forcing_ingest_entry table!")

    # Create our model run table
    #cmd = """
    #CREATE TABLE IF NOT EXISTS model_run_metadata(
    #    id SERIAL PRIMARY KEY,
    #    name VARCHAR(64),
    #    retro_flag BOOL,
    #    ana_flag BOOL,
    #    fcst_flag BOOL,
    #    ensemble_flag BOOL,
    #    forcing_source INTEGER,
    #    retro_beg_date TIMESTAMPTZ,
    #    retro_end_date TIMESTAMPTZ,
    #    fcst_cycle_date TIMESTAMPTZ,
    #    fcst_hours INTEGER,
    #    num_ens_members INTEGER,
    #    forcing INTEGER,
    #    supp_forcing_precip INTEGER,
    #    physics_config INTEGER
    #);
    #"""
    #dbObj.create_table(cmd)
    #print("Successfully created model_run_metadata table!")

    # Create our analysis tables

if __name__ == "__main__":
    main()