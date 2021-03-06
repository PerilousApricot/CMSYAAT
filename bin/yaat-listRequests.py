#!/usr/bin/env python2.6

import os
import sys
import pwd
import json

from optparse import OptionParser
from CMSYAAT.RequestManager import RequestManager
from CMSYAAT.Utilities import Logging

# TODO: Get some common options parsing
parser = OptionParser()

parser.add_option("-e", "--endpoint", dest="endpoint",
                  help="Target request manager",
                  default="http://cmsweb.cern.ch/reqmgr")

(options, args) = parser.parse_args()

reqmgr = RequestManager( endpoint = options.endpoint )

for request in reqmgr.listRequests():
    print request.getWorkflowName()

sys.exit( 0 )
