# Top module file for handling I/O

import boto3
import sys

class ioObj():
    """
    Abstract class for storing information about our local/cloud/external I/O
    """
    def __init__(self):
        self.asoAwsObject = None
        self.inspectorLocalDir = "/mnt/data/tomcat/data"

        try:
            self.asoAwsObject = boto3.client('s3')
        except:
            print("Unable to establish ASO AWS S3 client.")
            sys.exit(-1)
