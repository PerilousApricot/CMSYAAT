#!/usr/bin/env python2.6

import os
import sys
import pwd

from optparse import OptionParser
from CMSYAAT.CMSSWConfigManager import CMSSWConfigManager

# TODO: Get some common options parsing
parser = OptionParser()
parser.add_option("-u", "--user", dest="user",
                  help="Username to store as", default=pwd.getpwuid(os.getuid()).pw_name)
parser.add_option("-g", "--group", dest="group",
                  help="Group to store as", default="CMSYAAT")
parser.add_option("-f", "--filename", dest="filename",
                  help="Configuration to upload")
parser.add_option("-e", "--endpoint", dest="endpoint",
        help="Target couch instance (formatted as https://cmsweb.cern.ch/couchdb/reqmgr_config_cache)",
        default="https://cmsweb.cern.ch/couchdb/reqmgr_config_cache")
parser.add_option("-w", "--workdir", dest="workdir",
                  help="CMSSW Installation to upload")

(options, args) = parser.parse_args()

factory = CMSSWConfigManager( endpoint = options.endpoint )

cache   = factory.newConfig()

cache.loadConfigFromFile( config    = options.filename,
                          directory = options.workdir,
                          args      = args )
target  = cache.uploadToConfigCache(
                        user      = options.user,
                        group     = options.group,
                        label     = os.path.basename(options.filename) )
print target
sys.exit( 0 )
