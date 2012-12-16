#!/usr/bin/env python2.6

import os
import sys
import pwd
import json

from optparse import OptionParser
from CMSYAAT.RequestManager import RequestManager
from CMSYAAT.Utilities import Logging, CommandLineHandler
Logging.initLogging()

# TODO: Get some common options parsing
commonArgs = ['endpoint','wmstat']
parser = CommandLineHandler.getParser(commonArgs)

(options, args) = parser.parse_args()
CommandLineHandler.validateArguments(options, args)

# should implement
# http://code.activestate.com/recipes/574459-easier-positional-arguments-for-optparse/
if len(args) == 0:
    logging.error("You must provide a request to examine")
    sys.exit(1)

reqmgr = RequestManager( endpoint = options.endpoint,
                         wmstat   = options.wmstat )
for requestName in args:
    request = reqmgr.getRequest( requestName )
    resultSummary = request.getJobResultsSummary()
    countSummary = request.getJobCountSummary()
    countSummaryBySite = request.getJobCountSummaryPerSite()

    print requestName
    print ""
    print "Current job status:"
    accountedJobs = 0
    print countSummaryBySite
    statusOrder = sorted(countSummary.keys())
    statusOrder.remove('total')
    statusOrder.append('uninjected')
    statusOrder.append('total')
    for key in sorted(countSummary.keys()):
        if key == 'total':
            continue
        print "  %s: %i" % (key, countSummary[key])
        accountedJobs += int(countSummary[key])
    print "  uninjected: %i" % (int(countSummary['total']) - int(accountedJobs))
    print "  total: %i" % (countSummary['total'],)
    
    print "Job exit codes:"
    for row in resultSummary['bycount']:
        print "  %i: %s" % (row['value'], row['key'][1:])
sys.exit( 0 )
