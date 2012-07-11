#!/usr/bin/env python2.6

from CMSYAAT.FileCache.ConfigCache import ConfigCache

cacheFile = ConfigCache()
config = cacheFile.loadConfig('LHEToAODSIM_cfg.py')
print "got config"
target = cacheFile.upload(config, 'meloam', 'meloam',
                    url="http://andrewmelo.cloudant.com:5984",
                    database="configcache",
                    )
print "Target is %s" % target
