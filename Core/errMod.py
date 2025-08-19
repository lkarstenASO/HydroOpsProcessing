# Module file for handling the warning/error of our pipeline. 

import os
import sys

class errConfig:
    """
    Abstract class to handle all configuration details for 
    dealing with warning/error options. 
    """
    def __init__(self):
        self.slackWarnChannel = "hydro-warnings"
        self.slackErrChannel = "hydro-error"
        self.slackAppToken = None
        self.warningMsg = None
        self.errMsg = None

    def initSlack(self):
        """
        Initialize our Slack App to report any warnings and messages we may 
        want to disseminate. 
        """
        try:
            self.slackAppToken = os.environ(["SLACK_TOKEN"])
        except:
            print("Unable to locate SLACK_TOKEN from environment")
            sys.exit(-1)
