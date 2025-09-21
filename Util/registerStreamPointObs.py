# Utility function for registering a new in-situ streamflow observation point 
# into our Postgres RDS instance hosted on AWS. 

import argparse
import psycopg2
import os
import sys
import pandas as pd

cwd = os.getcwd()
parentWd = os.path.dirname(cwd)
sys.path.append(parentWd)
from Core import dbMod

def main():
    """
    Utility for registering new in-situ observation locations into 
    our RDS table. 
    """
    parser = argparse.ArgumentParser(description="RDS Utility for registering new in-situ observation locations")
    parser.add_argument('metaCSV', type=str, nargs='+', help='Required CSV with metadata to input')

    # Parse our arguments
    args = parser.parse_args()

    # Initialize our DB class and connection
    dbObj = dbMod.dbObj()

    if not os.path.isfile(args.metaCSV[0]):
        print("Unable to locate metadata file: " + args.metaCSV[0])
        sys.exit(-1)

    dfMeta = pd.read_csv(args.metaCSV[0])
    
    # Sanity checking to ensure the format of the input CSV is correct. 
    if "Agency" not in list(dfMeta.keys()):
        print("Unable to locate Agency in: " + args.metaCSV[0])
        sys.exit(-1)
    if 'ID' not in list(dfMeta.keys()):
        print("Unable to locate ID in: " + args.metaCSV[0])
        sys.exit(-1)
    if 'Station Name' not in list(dfMeta.keys()):
        print("Unable to locate Station Name in: " + args.metaCSV[0])
        sys.exit(-1)
    if 'Latitude' not in list(dfMeta.keys()):
        print("Unable to locate Latitude in: " + args.metaCSV[0])
        sys.exit(-1)
    if 'Longitude' not in list(dfMeta.keys()):
        print("Unable to locate Longitude in: " + args.metaCSV[0])
        sys.exit(-1)
    if 'FNF Flag' not in list(dfMeta.keys()):
        print("Unable to locate FNF Flag in: " + args.metaCSV[0])
        sys.exit(-1)
    if 'Units' not in list(dfMeta.keys()):
        print("Unable to locate Units in: " + args.metaCSV[0])
        sys.exit(-1)

    # Loop over our stations and do a check to see if this information has already been entered. 
    numStations = len(dfMeta['ID'])
    for station in range(0,numStations):
        # Do some sanity checking on our data. 
        if dfMeta['Agency'][station] not in ['USGS','CDEC','CDWR']:
            print("Invalid Agency: " + dfMeta['Agency'][station] + " for station name: " + dfMeta['Station Name'][station])
            sys.exit(-1)

        # Ensure this station hasn't already been entered into the DB. 
        dbObj.checkStationMeta(dfMeta,station) 

    # Next, Let's enter our database information. 
    for station in range(0,numStations):
        # Check to see if this location has already been registered
        stationStatus = dbObj.checkStreamPointMeta(dfMeta,station)

        if not stationStatus:
            dbObj.enterStreamPointMeta(dfMeta,station)

if __name__ == "__main__":
    main()

