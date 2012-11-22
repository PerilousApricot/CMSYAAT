'''
Created by Andrew Melo <andrew.melo@gmail.com> on Aug 9, 2012

'''
from CMSYAAT.CMSSWConfig import CMSSWConfig

class CMSSWConfigManager(object):
    '''
    Interacts with ConfigCache, a subsystem that stores/caches CMSSW
    configurations.
    '''


    def __init__(self, endpoint = \
                        "https://cmsweb.cern.ch/couchdb/reqmgr_config_cache"):
        self.endpoint = endpoint
    
    def newConfig(self):
        """
        Returns a fresh CMSSWConfig object which can be customised and stored
        """
        return CMSSWConfig( endpoint = self.endpoint )
    
    def getConfig(self, url):
        """
        given a URL, return a CMSSWConfig object attached to it
        """
        config = CMSSWConfig()
        config.url = url
        return config
