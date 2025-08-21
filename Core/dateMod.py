# Top module file for handling datetime operations 

import datetime
import sys

class dateObj():
    """
    Abstract class for handling datetime information and processing. 
    """
    def __init__(self):
        self.begProcWindow = None
        self.endProcWindow = None
        self.obsDt = None # Seconds
        self.nObsSteps = None
        self.analysisDt = None # Seconds
        self.nAnalysisSteps = None
    def calcArgProcWindow(self,lookback,begDate,endDate):
        """
        Generic function for calculating our processing window 
        based on user-provided arguments for a lookback/proc 
        window. 
        """
        if lookback is not None:
            if begDate is not None:
                print("Either specify a lookback or a beginning/ending window of processing")
                sys.exit(-1)
            if endDate is not None:
                print("Either specify a lookback or a beginning/ending window of processing")
                sys.exit(-1)
            if lookback <= 0:
                print("Please specify a positive value for the lookBack period")
                sys.exit(-1)

        if begDate is not None:
            if endDate is None:
                print("Please specify a ending date for this processing window.")
                sys.exit(-1)
            if len(begDate) != 10:
                print("Improper begDate length specified")
                sys.exit(-1)
            try:
                self.begProcWindow = datetime.datetime.strptime(begDate,'%Y%m%d%H')
            except:
                print("Unable to process provided begDate: " + begDate)
                sys.exit(-1)

        if endDate is not None:
            if begDate is None:
                print("Please specify a beginning date for this processing windw")
                sys.exit(-1)
            if len(endDate) != 10:
                print("Improper endDate length specified")
                sys.exit(-1)
            try:
                self.endProcWindow = datetime.datetime.strptime(endDate,'%Y%m%d%H')
            except:
                print("Unable to process provided endDate: " + endDate)
                sys.exit(-1)

            if endDate <= begDate:
                print("Please provide endDate that is after begDate")
                sys.exit(-1)