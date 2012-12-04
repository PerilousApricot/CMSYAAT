#!/usr/bin/env python2.6

import os
import sys
import pwd
import json

from CMSYAAT.RequestManager import RequestManager
from CMSYAAT.Utilities import Logging
Logging.initLogging()
from CMSYAAT.Utilities import CommandLineHandler

# TODO: Get some common options parsing
commonArgs = ['endpoint']
parser = CommandLineHandler.getParser(commonArgs)

(options, args) = parser.parse_args()
CommandLineHandler.validateArguments(options, args)

reqmgr = RequestManager( endpoint = options.endpoint )
for request in args:
    requestDict = json.loads( open( request, 'r' ).read() )
    newRequest = reqmgr.newRequest()
    newRequest.setRequestDict( requestDict )
    reqmgr.submitRequest( newRequest )
    print newRequest.getWorkflowName()

sys.exit( 0 )
