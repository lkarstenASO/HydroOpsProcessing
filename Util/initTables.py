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
        operations_flag BOOL,
        dx_land INTEGER,
        dx_hydro INTEGER,
        lake_flag BOOL,
        reach_based_stack BOOL,
        version_label VARCHAR(64),
        parent_domain_id INTEGER,
        parent_domain_x1 INTEGER,
        parent_domain_x2 INTEGER,
        parent_domain_y1 INTEGER,
        parent_domain_y2 INTEGER,
        bsi_flag BOOL,
        bsi_age_epoch TIMESTAMPTZ,
        notes VARCHAR(512)
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
        channel_loss INTEGER,
        lake_opt INTEGER,
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

    # Create a table to store information about reanalysis/retrospective
    # forcings for a given modeling domain. 
    cmd = """
    CREATE TABLE IF NOT EXISTS retro_forcing_entry(
        id SERIAL PRIMARY KEY,
        domain_id INTEGER,
        key_lookup INTEGER,
        beg_date TIMESTAMPTZ,
        end_date TIMESTAMPTZ,
        s3_dir VARCHAR(256)
    );
    """
    dbObj.create_table(cmd)
    print("Successfully created retro_forcing_entry table!")

    # Create our forcing processing table to keep track of what's 
    # been processed, etc. 
    cmd = """
    CREATE TABLE IF NOT EXISTS forcing_engine_entry(
        id SERIAL PRIMARY KEY,
        key_lookup INTEGER,
        domain_id INTEGER,
        spatial_method INTEGER,
        supp_pcp_flag BOOL,
        bsi_flag BOOL,
        reanalysis_flag BOOL,
        cycle_date TIMESTAMPTZ,
        forecast_date TIMESTAMPTZ,
        pcp_bias_adj BOOL,
        pcp_adj_factor FLOAT,
        s3_dir VARCHAR(256)
    );
    """
    dbObj.create_table(cmd)
    print("Successfully created forcing_engine_entry table!")

    # Create our model run metadata table
    cmd = """
    CREATE TABLE IF NOT EXISTS model_run_metadata(
        id SERIAL PRIMARY KEY,
        name VARCHAR(64),
        domain_id INTEGER,
        io_id INTEGER,
        retro_flag BOOL,
        ana_flag BOOL,
        fcst_flag BOOL,
        operations_flag BOOL,
        forcing_source INTEGER[],
        supp_pcp_source INTEGER[],
        retro_beg_date TIMESTAMPTZ,
        retro_end_date TIMESTAMPTZ,
        fcst_cycle_freq INTEGER,
        fcst_cycle_freq_offset INTEGER,
        fcst_hours INTEGER,
        physics_config INTEGER,
        esp_flag BOOL,
        beg_esp_mem_year INTEGER,
        end_esp_mem_year INTEGER,
        cold_start BOOL,
        restart_source INTEGER,
        alt_restart_date TIMESTAMPTZ
    );
    """
    dbObj.create_table(cmd)
    print("Successfully created model_run_metadata table!")

    # Create our model run entry table to keep track of model progress. 
    cmd = """
    CREATE TABLE IF NOT EXISTS model_run_entry(
        id SERIAL PRIMARY KEY,
        model_id INTEGER,
        esp_member INTEGER,
        beg_cycle_date TIMESTAMPTZ,
        end_cycle_date TIMESTAMPTZ,
        last_date_complete TIMESTAMPTZ,
        upload_complete BOOL,
        model_lock BOOL
    );
    """
    dbObj.create_table(cmd)
    print("Successfully created model_run_entry table!")

    # Create our I/O table that will hold output configurations for the model.
    cmd = """
    CREATE TABLE IF NOT EXISTS io_metadata(
        id SERIAL PRIMARY KEY,
        name VARCHAR(64),
        lsm_out_freq INTEGER,
        lsm_rst_freq INTEGER,
        force_type INTEGER,
        hydro_out_freq INTEGER,
        hydro_rst_freq INTEGER,
        order_to_write INTEGER,
        io_form_output INTEGER,
        io_config INTEGER,
        t0_flag INTEGER,
        out_channel_influx INTEGER,
        chrtout_domain INTEGER,
        chanobs_domain INTEGER,
        chrtout_grid INTEGER,
        lsmout_domain INTEGER,
        rtout_domain INTEGER,
        output_gw INTEGER,
        output_lake INTEGER,
        frxst_pts_out INTEGER
    );
    """
    dbObj.create_table(cmd)
    print("Successfully created io_metadata table!")

    # Create our spatial analysis metadata table. 
    cmd = """
    CREATE TABLE IF NOT EXISTS spatial_aoi_metadata(
        id SERIAL PRIMARY KEY,
        hydro_id VARCHAR(16),
        aso_id VARCHAR(16),
        name VARCHAR(64),
        domain_id INTEGER,
        notes VARCHAR(512)
    );
    """
    dbObj.create_table(cmd)
    print("Successfully created spatial_aoi_metadata table!")

    # Create our forecast point metadata table.
    cmd = """
    CREATE TABLE IF NOT EXISTS frxst_pt_metadata(
        id SERIAL PRIMARY KEY,
        hydro_id VARCHAR(64),
        domain_id INTEGER,
        name VARCHAR(64),
        aoi_id INTEGER,
        WRF_Hydro_Reach_ID INTEGER,
        obs_id INTEGER
    );
    """
    dbObj.create_table(cmd)
    print("Successfully created frxst_pt_metadata table!")

    # Create our table to hold model streamflow values for forecast points. 
    cmd = """
    CREATE TABLE IF NOT EXISTS frxst_pt_streamflow(
        id SERIAL PRIMARY KEY,
        frxstPt_id INTEGER,
        model_id INTEGER,
        forecast_cycle TIMESTAMPTZ,
        forecast_date TIMESTAMPTZ,
        esp_mem_year INTEGER,
        discharge_cfs FLOAT [],
        discharge_taf FLOAT []
    );
    """
    dbObj.create_table(cmd)
    print("Successfully created frxst_pt_streamflow table!")

    # Create our spatial analysis stats table. 
    cmd = """
    CREATE TABLE IF NOT EXISTS spatial_aoi_stats(
        model_id INTEGER,
        spatial_id INTEGER,
        forecast_cycle TIMESTAMPTZ,
        forecast_date TIMESTAMPTZ,
        esp_mem_year INTEGER,
        swe_volume_taf FLOAT,
        soilsat_avg FLOAT
    );
    """
    dbObj.create_table(cmd)
    print("Successfully created spatial_aoi_stats table!")

if __name__ == "__main__":
    main()