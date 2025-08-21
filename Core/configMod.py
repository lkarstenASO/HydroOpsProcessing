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
        self.dt = None
        self.cloudFlag = None
        self.ftpFlag = None
        self.httpFlag = None
        self.sourceFtpDir = None

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
        self.dt = timesteps[self.keyValue]
        dateObj.analysisDt = self.dt

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
