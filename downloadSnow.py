# Top level program to download snow observations and analysis 
# products. 

# Logan Karsten
# Airborne Snow Observatories Inc.,
# logan.karsten@airbornesnowobservatories.com

import argparse
import os
import sys
from Core import dateMod
from Core import ioMod
from Core import configMod

def main():
    """
    Main calling program to pull down either point snow observations or gridded 
    snow analysis products. 
    
    The following arguments are required:
    --product - Acceptable values are [SNODAS]

    # The following arguments are optional
    --lookBack - Lookback period in hours
    --begDate - Beginning date of pull (if lookback is not provided) in YYYYMMDDHH format
    --endDate - Ending date of pull (if lookback is not provided) in YYYYMMDDHH format
    """
    # Initialize our arguments
    parser = argparse.ArgumentParser(description="Snow download program")
    parser.add_argument('-p','--product', type=str, nargs='+', help='Product being downloaded - Choices are: \n SNODAS')
    parser.add_argument('-s','--scratchDir', type=str, nargs='+', help="Scratch directory to use for temporary files")
    parser.add_argument('-l','--lookBack', type=int, nargs='?', help='Lookback of processing in hours')
    parser.add_argument('-b','--begDate', type=str, nargs='?', help='Beginning date of processing window in YYYYMMDDHH format')
    parser.add_argument('-e','--endDate', type=str, nargs='?', help='Ending date of processing window in YYYYMMDDHH format')
    parser.add_argument('-hy','--hydroInspector', action='store_true', help='Process data for HydroInspector to local disk? True/False')

    # Parse our arguments
    args = parser.parse_args()

    # Initialize our cloud storage object
    ioObj = ioMod.ioObj()

    # Sanity checking
    if args.scratchDir is None:
        print("Please provide scratchDir argument")
        sys.exit(-1)
    else:
        if not os.path.isdir(args.scratchDir[0]):
            print("Unable to locate scratch directory: " + args.scratchDir[0])
            sys.exit(-1)

    if args.product is None:
        print("Please provide a product to process")
        sys.exit(-1)
    else:
        if args.product[0] not in ['SNODAS']:
            print("Invalid product: " + args.product[0])
            sys.exit(-1)

    if args.begDate is None and args.endDate is None and args.lookBack is None:
        print("Please provide date options for the program")
        sys.exit(-1)

    # Initialize our date object
    dateObj = dateMod.dateObj()
    dateObj.calcArgProcWindow(args.lookBack,args.begDate,args.endDate)

    # Initialize our metadata objects depending on what argument was provided. 
    analysisMeta = configMod.analysisMeta(args.product[0], dateObj)
    
if __name__ == "__main__":
    main()
