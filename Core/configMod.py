# Top level abstract modules that will define 
# key metadata for various inputs/outputs/etc

class analysisMeta:
    """
    Abstract class that will define our gridded 
    analysis products
    """
    def __init__(self,prodName,dateObj):
        """
        Abstract calss to define our gridded analysis. 
        """
        self.runFlag = False
        self.keyValue = None
        self.cloudFlag = None
        self.ftpFlag = None
        self.httpFlag = None
        self.sourceFtpDir = None
        self.topCloudOutDir = None

        productKeys = {
            "SNODAS": 1
        }
        if prodName in productKeys:
            print("Creating configuration for analysis product: " + prodName)
            self.runFlag = True
        else:
            print("No analysis products found to process")
            return
        self.keyValue = productKeys[prodName]

        timesteps = {
            1: 86400
        }
        dateObj.analysisDt = timesteps[self.keyValue]

        # For any product, we need to introduce a lag time from present going back when we expect
        # data to start showing up. 
        lagtime = {
            1: 86400
        }
        dateObj.analysisLagDt = lagtime[self.keyValue]

        cloudFlags = {
            1: False
        }
        self.cloudFlag = cloudFlags[self.keyValue]

        ftpFlags = {
            1: True
        }
        self.ftpFlag = ftpFlags[self.keyValue]

        upstreamFtp = {
            1: "ftp://sidads.colorado.edu/DATASETS/NOAA/G02158/masked"
        }
        self.sourceFtpDir = upstreamFtp[self.keyValue]

        topCloudDirs = {
            1: "Snow_Data/SNODAS"
        }
        self.topCloudOutDir = topCloudDirs[self.keyValue]

        # Calculate the number of steps we are processing 
        dateObj.calcAnalysisInfo()
