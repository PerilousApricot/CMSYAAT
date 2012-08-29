'''
Created by Andrew Melo <andrew.melo@gmail.com> on Aug 9, 2012

'''
from CMSYAAT.CMSSWConfig import CMSSWConfig

class CMSSWConfigManager(object):
    '''
    Interacts with ConfigCache, a subsystem that stores/caches CMSSW
    configurations.
    '''


    def __init__(self, couchHost = "https://cmsweb.cern.ch/couchdb",
                       couchDB   = "reqmgr_config_cache"):
        self.couchHost = couchHost
        self.couchDB   = couchDB
    
    def newConfig(self):
        """
        Returns a fresh CMSSWConfig object which can be customised and stored
        """
        return CMSSWConfig( couchHost = self.couchHost,
                            couchDB   = self.couchDB )
    
    def getConfig(self, url):
        """
        given a URL, return a CMSSWConfig object attached to it
        """
        config = CMSSWConfig()
        config.url = url
        return config        