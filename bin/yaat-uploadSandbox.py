#!/usr/bin/env python2.6

from optparse import OptionParser
from CMSYAAT.FileCache.SandboxCache import SandboxCache

# TODO: Get some common options parsing
parser = OptionParser()
parser.add_option("-w", "--workdir", dest="workdir",
                  help="CMSSW Installation to upload")
parser.add_option("-h", "--hostname", dest="hostname",
                  help="Target endpoint",
                  default="https://cmsweb.cern.ch/crabcache")
(options, args) = parser.parse_args()

cache = SandboxCache( )
cache.generateSandboxFromWorkingDirectory( options.workdir )
target = cache.upload()
print target