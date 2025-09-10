# Top module file for handling datetime operations 

import datetime
import sys

class dateObj:
    """
    Abstract class for handling datetime information and processing. 
    """
    def __init__(self):
        self.begProcWindow = None
        self.endProcWindow = None
        self.lookbackHours = None
        self.obsDt = None # Seconds
        self.nObsSteps = None
        self.analysisDt = None # Seconds
        self.nAnalysisSteps = None
        self.analysisLagDt = None # Seconds
        self.currentAnalysisDate = None
        self.lookFlag = False
        self.customWindowFlag = False
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
            self.lookFlag = True
            self.lookbackHours = int(lookback)

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
            self.customWindowFlag = True

    def calcAnalysisInfo(self):
        """
        Function to calculate the number of analysis steps
        """
        # First, determine if the datetime information passed by the user
        # jives with the dataset provided. 
        if self.customWindowFlag:
            # We are using a custom window passed by the user
            dtTmp = self.endProcWindow - self.begProcWindow
            dtTmpSeconds = int(dtTmp.days*86400.0) + int(dtTmp.seconds)
            # Make sure the time window specified by the user is an even divider of the frequency produced
            if dtTmpSeconds%int(self.analysisDt) != 0:
                print("Custom time window does not work with product step of: " + str(self.analysisDt) + " seconds...")
                sys.exit(-1)
            self.nAnalysisSteps = int(dtTmpSeconds/self.analysisDt)
        if self.lookFlag:
            # Sanity checking - Make sure the lookback period is an even divider of the frequency produced
            analysisDtHours = self.analysisDt/3600
            if self.lookbackHours%analysisDtHours != 0:
                print("You have specified a lookback period which is incompatable with the analysis frequency")
                sys.exit(-1)
            # Get our current UTC time
            utcNow = datetime.datetime.now(datetime.timezone.utc)
            if self.analysisLagDt == 86400:
                # We are processing data on a daily timestep. 
                utcNow = utcNow - datetime.timedelta(seconds=86400)
                self.endProcWindow = datetime.datetime(utcNow.year,utcNow.month,utcNow.day)
            self.begProcWindow = self.endProcWindow - datetime.timedelta(seconds=self.lookbackHours*3600)
        print("Processing data for: " + self.begProcWindow.strftime('%Y-%m-%d %H:00') + " to: " + self.endProcWindow.strftime('%Y-%m-%d %H:00'))
        dtTmp = self.endProcWindow - self.begProcWindow
        dtTmp = int(dtTmp.days*86400) + int(dtTmp.seconds)
        self.nAnalysisSteps = int(dtTmp/self.analysisDt)

    def getCurrentAnalysisDate(self,stepNum):
        """
        Function that will calculate the current analysis date we are processing.
        """
        self.currentAnalysisDate = self.begProcWindow + datetime.timedelta(seconds=stepNum*self.analysisDt)