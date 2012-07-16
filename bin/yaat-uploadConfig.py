#!/usr/bin/env python2.6

import sys
import pwd

from optparse import OptionParser
from CMSYAAT.FileCache.ConfigCache import ConfigCache

# TODO: Get some common options parsing
parser = OptionParser()
parser.add_option("-u", "--user", dest="user",
                  help="Username to store as", default=pwd.getpwuid(os.getuid()))
parser.add_option("-g", "--group", dest="group",
                  help="Group to store as", default="CMSYAAT")
parser.add_option("-f", "--filename", dest="filename",
                  help="Configuration to upload")
parser.add_option("-h", "--hostname", dest="hostname",
                  help="Target couch instance (formatted as http://andrewmelo.cloudant.com:5984)",
                  default="http://se2.accre.vanderbilt.edu:5984")
parser.add_option("-d", "--database", dest="database",
                  help="Target database", default="wmagent_configcache")
(options, args) = parser.parse_args()


cacheFile = ConfigCache()
config = cacheFile.loadConfig( options.filename )
target = cacheFile.upload(config, options.user, options.group,
                    url=options.hostname,
                    database=options.database,
                    arguments=args,
                    )
print target
