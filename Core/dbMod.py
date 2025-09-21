import os
import sys
import psycopg2

class dbObj:
    """
    Abstract class to handle databaset operations with our RDS
    database we have created
    """
    def __init__(self):
        self.dbConn = None
        self.dbCursor = None
        self.dbHost = 'wrf-hydro-dev-db.cgk4m6rkkjzo.us-west-2.rds.amazonaws.com'

        # First we will check if the DB password has been set in the environment.
        # If it hasn't, prompt the user to type it in.
        try:
            pwdTmp = os.environ['HYDRO_DB_PWD']
        except KeyError:
            try:
                pwdTmp = input("Enter Database Password:")
            except:
                print("Error in user input")
                sys.exit(-1)

        # Sanity checking
        if pwdTmp == None:
            print("Password provided is Nonetype")
            sys.exit(-1)

        if len(pwdTmp) == 0:
            print("Zero length password passed to program")
            sys.exit(-1)

        # Establish our connection to the database. 
        try:
            self.dbConn = psycopg2.connect("dbname='hydro' host=" + "\'" + self.dbHost + \
                                           "\' user='postgres' password=" + "\'" + pwdTmp + "\'")
        except:
            print("Unable to connect to the hydro DB")
            sys.exit(-1)

        self.dbCursor = self.dbConn.cursor()

    def create_table(self,cmd):
        """
        Function to quickly create a table given a command provided. 
        """
        self.dbCursor.execute(cmd)
        self.dbConn.commit()
        #try:
        #    self.dbCursor.execute(cmd)
        #except:
        #    print("Unable to create table for command: " + cmd)
        #    sys.exit(-1)

        #try:
        #    self.dbConn.commit()
        #except:
        #    print("Unable to commit commit transaction for cmd: " + cmd)
        #    sys.exit(-1)

    def close(self):
        """
        Function to close our PSQL connection
        """
        try:
            self.dbCursor.close()
        except:
            print("Unable to close the database cursor")
            sys.exit(-1)

        try:
            self.dbConn.close()
        except:
            print("Unable to close the PSQL database connector")
            sys.exit(-1)

    def checkStreamPointMeta(self,dfMeta,stationNum):
        """
        Function that will check the database to see if a particular 
        streamflow station already has been registered into the
        Postgres DB. Input arguments are:
        dfMeta - Pandas dataframe that contains the station metadata
        stationNum - Which station index number are we checking? 
        """
        # Compose the SQL command that will check for the unique primary key ID 
        # given the network type and network ID. If any results are returned,
        # then flag an error as this station has already been entered into 
        # the database. 
        if str(dfMeta['Agency'][stationNum]) == "USGS":
            networkIdTmp = str(dfMeta['ID'][stationNum])
            if len(networkIdTmp) < 8:
                # USGS IDs need to have a padded 0 if they aren't of length 8
                networkIdTmp = "0" + networkIdTmp
        else:
            networkIdTmp = str(dfMeta['ID'][stationNum])
        networkTmp = str(dfMeta['Agency'][stationNum])

        # Compose our SQL command
        cmd = "SELECT \"id\" from \"station_meta_streamflow\" where \"agency_id\"='" + \
              str(networkIdTmp) + "' and \"agency_name\"='" + str(networkTmp) + "';"
        
        foundStation = False
        try:
            self.dbCursor.execute(cmd)
        except:
            print("Unable to execute the SQL command: " + cmd)
            sys.exit(-1)

        result = self.dbCursor.fetchone()
        
        if result != None:
            print("Station ID: " + networkIdTmp + " already entered for network: " + networkTmp)
            foundStation = True

        return foundStation
    
    def enterStreamPointMeta(self,dfMeta,stationNum):
        """
        Function that will enter station metadata into our database. 
        """
        # Setup the variables we need to enter. 
        if str(dfMeta['Agency'][stationNum]) == "USGS":
            networkIdTmp = str(dfMeta['ID'][stationNum])
            if len(networkIdTmp) < 8:
                # USGS IDs need to have a padded 0 if they aren't of length 8
                networkIdTmp = "0" + networkIdTmp
        else:
            networkIdTmp = str(dfMeta['ID'][stationNum])
        networkTmp = str(dfMeta['Agency'][stationNum])
        nameTmp = str(dfMeta['Short Name'][stationNum])
        latTmp = float(dfMeta['Latitude'][stationNum])
        if latTmp is None:
            latTmp = -9999.0
        lonTmp = float(dfMeta['Longitude'][stationNum])
        if lonTmp is None:
            lonTmp = -9999.0
        fnfFlagTmp = dfMeta['FNF Flag'][stationNum]
        if fnfFlagTmp == "True" or fnfFlagTmp == "true":
            fnfFlagTmp = True
        else:
            fnfFlagTmp = False
        unitsTmp = str(dfMeta['Units'][stationNum])

        # Compose our SQL command
        cmd = "INSERT INTO \"station_meta_streamflow\" (agency_name,agency_id,station_name,fnf_flag,latitude,longitude,units) VALUES " + \
              "('%s','%s','%s','%s','%f','%f','%s');" % (networkTmp,networkIdTmp,nameTmp,fnfFlagTmp,latTmp,lonTmp,unitsTmp)
        
        try:
            self.dbCursor.execute(cmd)
            self.dbConn.commit()
        except:
            print("Unable to execute SQL command: " + cmd)
            sys.exit(-1)
