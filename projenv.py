import os
import sys

# Configure environment
wrkdir, _ = os.path.split(__file__)
vendor_path = os.path.abspath(wrkdir+"/vendor")
sys.path.append(vendor_path)
