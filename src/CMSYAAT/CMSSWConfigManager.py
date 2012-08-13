'''
Created by Andrew Melo <andrew.melo@gmail.com> on Aug 9, 2012

'''

class CMSSWConfigManager(object):
    '''
    Interacts with ConfigCache, a subsystem that stores/caches CMSSW
    configurations.
    '''


    def __init__(self):
        pass
    
    def newConfig(self):
        """
        Returns a fresh CMSSWConfig object which can be customised and stored
        """
        raise NotImplementedError
    
    def submitConfig(self, configuration):
        """
        Submits a configuration to ConfigCache, returning a new object linked
        to the remote database
        """
        raise NotImplementedError
    
    def getConfig(self, url):
        """
        given a URL, return a CMSSWConfig object attached to it
        """
        raise NotImplementedError
        