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
