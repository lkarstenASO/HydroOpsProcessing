# Module file for handling the warning/error of our pipeline. 

import os
import sys
from slack_sdk import WebClient

class errConfig:
    """
    Abstract class to handle all configuration details for 
    dealing with warning/error options. 
    """
    def __init__(self,args):
        self.slackWarnChannel = "hydro-warnings"
        self.slackErrChannel = "hydro-error"
        self.slackAppToken = None
        self.warningMsg = None
        self.errMsg = None
        self.slackFlag = False
        if args.slack is True:
            self.slackFlag = True
        self.slackClient = None

    def initSlack(self):
        """
        Initialize our Slack App to report any warnings and messages we may 
        want to disseminate. 
        """
        if not self.slackFlag:
            print("Executing without Slack messaging")
            return
        try:
            self.slackAppToken = os.environ["SLACK_TOKEN"]
        except:
            print("Unable to locate SLACK_TOKEN from environment")
            sys.exit(-1)
        try:
            self.slackClient = WebClient(token=self.slackAppToken)
        except:
            print("Unable to create Slack Client given token provided")
            sys.exit(-1)

    def errOut(self):
        """
        Function that will post an error message to Slack indicating a catastrophic error. 
        """
        print(self.errMsg)
        sys.exit(-1)
