#!/usr/bin/env python2.6

import sys
import pwd

from optparse import OptionParser
from CMSYAAT.FileCache.ConfigCache import ConfigCache

# TODO: Get some common options parsing
parser = OptionParser()
parser.add_option("-f", "--filename", dest="filename",
                  help="Configuration to dump")
parser.add_option('-o', dest="output", default=None,
                  help="Output file (defaults to stdout)")
(options, args) = parser.parse_args()


cacheFile = ConfigCache()
config = cacheFile.loadConfig( options.filename )
print config.process.dumpPython()

