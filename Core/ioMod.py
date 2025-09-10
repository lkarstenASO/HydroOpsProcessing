# Top module file for handling I/O

import boto3
import sys
from urllib import request
from os.path import isfile
from os import remove

class ioObj:
    """
    Abstract class for storing information about our local/cloud/external I/O
    """
    def __init__(self,args):
        self.asoAwsObject = None
        self.inspectorLocalDir = "/mnt/data/tomcat/data"
        self.asoHydroBucket = "aso-wrf-hydro"
        self.asoHydroOpsS3 = "Operations"
        self.ftpPath = None
        self.localPath = None
        self.asoS3Path = None
        self.scratchDir = args.scratchDir[0]

        try:
            self.asoAwsObject = boto3.client('s3')
        except:
            print("Unable to establish ASO AWS S3 client.")
            sys.exit(-1)

    def downloadFtpFile(self,ftpPath,localPath,errObj):
        """
        Function to download our FTP file locally
        """
        try:
            request.urlretrieve(ftpPath,localPath)
        except:
            errObj.errMsg = "Unable to download TAR file: " + ftpPath
            if isfile(localPath):
                remove(localPath)
            errObj.errOut()

    def openTarFile(self,tarPath,errObj):
        """
        Function to open our TAR file
        """
        import tarfile

        try:
            tf = tarfile.open(tarPath)
        except:
            errObj.errMsg = "Unable to open TAR file: " + tarPath
            errObj.errOut()
        return tf

    def extractTarFile(self,tf,fileName,outDir,errObj):
        """
        Function to extract out a specific file from our TAR file
        """
        df = tf.getmember(fileName)
        tf.extractall(outDir,members=[df])
        if not isfile(outDir + "/" + fileName):
            errObj.errMsg = "Unable to locate expected extracted file: " + outDir + "/" + fileName
            errObj.errOut()

    def gzipFile(self,gzPath,outPath,errObj):
        """
        Function to gunzip a file and remove the .gz after processing
        """
        import gzip

        try:
            fIn = gzip.open(gzPath, "rb")
            fOut = open(outPath,"wb")
            fOut.write(fIn.read())
        except:
            errObj.errMsg = "Unexpected read/write error extracting: " + gzPath
            errObj.errOut()
            if isfile(outPath):
                remove(outPath)
            return
        if isfile(gzPath):
            remove(gzPath)

class ingestObj:
    """
    Abstract class to handle downloading and ingesting various datasets 
    for ASO Hydrologic Prediction
    """
    def __init__(self):
        self.complete = False
    
    def ingestAnalysis(self,analysisMeta,dateObj,ioObj,errObj):
        """
        Polymorphic function that will direct to the proper functions 
        below to download/process various analysis datasets.
        """
        if not analysisMeta.runFlag:
            return
        ingestFunctions = {
            1: self.ingestSNODAS
        }
        ingestFunctions[analysisMeta.keyValue](analysisMeta,dateObj,ioObj,errObj)

    def ingestSNODAS(self,analysisMeta,dateObj,ioObj,errObj):
        """
        Function to download daily SNODAS SWE/Depth grids, process 
        them into NetCDF files, and place them into final locations
        for S3/HydroInspector access. 
        """
        import tarfile
        import gzip
        from osgeo import gdal

        # Establish a global HDR
        SNODAS_HEADER="""ENVI
        samples = 6935
        lines   = 3351
        bands   = 1
        header offset = 0
        file type = ENVI Standard
        data type = 2
        interleave = bsq
        byte order = 1
        """

        # We will loop over each of our steps in our time window 
        # and ingest our SNODAS data for each step. 
        for step in range(0,dateObj.nAnalysisSteps):
            dateObj.getCurrentAnalysisDate(step)

            # Establish filenames
            ncFileName = dateObj.currentAnalysisDate.strftime('%Y%m%d') + "0600.SNODAS.nc"
            tarFileName = "SNODAS_" + dateObj.currentAnalysisDate.strftime("%Y%m%d") + ".tar"
            sneqvGzFileName = "us_ssmv11034tS__T0001TTNATS" + dateObj.currentAnalysisDate.strftime('%Y%m%d') + "05HP001.dat.gz"
            snowhGzFileName = "us_ssmv11036tS__T0001TTNATS" + dateObj.currentAnalysisDate.strftime('%Y%m%d') + "05HP001.dat.gz"
            sneqvDatFileName = "SNODAS_SNEQV_" + dateObj.currentAnalysisDate.strftime('%Y%m%d') + ".dat"
            snowhDatFileName = "SNODAS_SNOWH_" + dateObj.currentAnalysisDate.strftime('%Y%m%d') + ".dat"
            sneqvHdrFileName = "SNODAS_SNEQV_" + dateObj.currentAnalysisDate.strftime('%Y%m%d') + ".hdr"
            snowhHdrFileName = "SNODAS_SNOWH_" + dateObj.currentAnalysisDate.strftime('%Y%m%d') + ".hdr"
            sneqvNcFileName = "SNODAS_SNEQV_" + dateObj.currentAnalysisDate.strftime('%Y%m%d') + ".nc"
            snowhNcFileName = "SNODAS_SNOWH_" + dateObj.currentAnalysisDate.strftime('%Y%m%d') + ".nc"

            # First we will check to see if this timestep has already been processed. 
            # We will check our S3 listing first. 
            # TODO - RDS logging/check?
            ncPathCloud = ioObj.asoHydroOpsS3 + "/" + analysisMeta.topCloudOutDir + "/" + \
                          dateObj.currentAnalysisDate.strftime('%Y%m') + "/" + ncFileName
            completeStatus = False
            try:
                check = ioObj.asoAwsObject.head_object(Bucket=ioObj.asoHydroBucket, Key=ncPathCloud)
                # If successful, we have found our final output file. We do not
                # need to process this file and can continue
                print("Found File")
                completeStatus = True
                continue
            except:
                print("Did not find file: " + ncPathCloud + " - Processing....")
                completeStatus = False
                # First, We will need to download the SWE and Snow Depth files from FTP
                snodasFtpPath = analysisMeta.sourceFtpDir + "/" + dateObj.currentAnalysisDate.strftime('%Y') + "/" + \
                                dateObj.currentAnalysisDate.strftime('%m_%b') + "/" + tarFileName
                tarTmpPath = ioObj.scratchDir + "/" + tarFileName
                ioObj.downloadFtpFile(snodasFtpPath,tarTmpPath,errObj)

                # Extract our file contents and process
                tf = ioObj.openTarFile(tarTmpPath,errObj)
                ioObj.extractTarFile(tf,sneqvGzFileName,ioObj.scratchDir,errObj)
                ioObj.extractTarFile(tf,snowhGzFileName,ioObj.scratchDir,errObj)

                # Remove our tar file
                remove(tarTmpPath)

                # Unzip the gzip files for snow depth and SWE
                ioObj.gzipFile(ioObj.scratchDir + "/" + sneqvGzFileName, ioObj.scratchDir + "/" + sneqvDatFileName, errObj)
                ioObj.gzipFile(ioObj.scratchDir + "/" + snowhGzFileName, ioObj.scratchDir + "/" + snowhDatFileName, errObj)

                # Create our temporary header files
                if isfile(ioObj.scratchDir + "/" + sneqvHdrFileName):
                    remove(ioObj.scratchDir + "/" + sneqvHdrFileName)
                if isfile(ioObj.scratchDir + "/" + snowhHdrFileName):
                    remove(ioObj.scratchDir + "/" + snowhHdrFileName)
                fh = open(ioObj.scratchDir + "/" + sneqvHdrFileName, "w")
                fh.write(SNODAS_HEADER)
                fh.close()
                fh = open(ioObj.scratchDir + "/" + snowhHdrFileName, "w")
                fh.write(SNODAS_HEADER)
                fh.close()

                # Use GDAL to convert out .dat files into temporary NetCDF files. 
                if isfile(ioObj.scratchDir + "/" + sneqvNcFileName):
                    remove(ioObj.scratchDir + "/" + sneqvNcFileName)
                if isfile(ioObj.scratchDir + "/" + snowhNcFileName):
                    remove(ioObj.scratchDir + "/" + snowhNcFileName)

                #try:
                gdal.Translate(
                    ioObj.scratchDir + "/" + sneqvNcFileName,
                    ioObj.scratchDir + "/" + sneqvDatFileName,
                    format="NETCDF",
                    outputSRS='+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs',
                    noData="-9999",
                    outputBounds=[-124.73333333, 52.87500000, -66.94166667, 24.95000000]
                )
                #except:
                #    errObj.errMsg = "Unable to convert SNODAS SNEQV to NetCDF for: " + dateObj.currentAnalysisDate.strftime('%Y-%m-%d')
                #    errObj.errOut()