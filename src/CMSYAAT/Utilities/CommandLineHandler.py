# common command line handling

from optparse import OptionParser
from CMSYAAT.Utilities import Logging
from logging import DEBUG
def getParser(commonArgs = []):
    parser = OptionParser()
    parser.add_option('-v', dest='verbose', action='store_true',
                      default=False, help='Increase verbosity')
    for arg in commonArgs:
        if arg == 'endpoint':
            parser.add_option("-e", "--endpoint", dest="endpoint",
                  help="Target request manager",
                  default="http://cmsweb.cern.ch/reqmgr")
    
    return parser

def validateArguments( options, args ):
    if options.verbose:
        rootCMSYAAT = Logging.getLogger('CMSYAAT')
        rootCMSYAAT.setLevel( DEBUG ) 
    return True
