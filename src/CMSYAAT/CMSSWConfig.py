'''
Created by Andrew Melo <andrew.melo@gmail.com> on Aug 10, 2012

'''

class CMSSWConfig(object):
    '''
    Represents one CMSSW configuration, either locally or stored in ConfigCache
    
    Note that for WMCore, it can only accept "fully-expanded" configurations,
    which is basically the result from process.dumpPython(). This means that
    any command line arguments, etc... are baked into each CMSSWConfig, so
    workflows that have useData (or other) flags, will have to make a new
    config for each flag
    
    This class handles generating "fully-expanded" configurations from a cmssw
    configuration and a CMSSW working directory. You don't need to source the
    environment beforehand. This class handles that.
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.url = None
        self.localPath = None
        
    def expandConfig(self, config, directory, target = None, args = []):
        """
        given a CMSSW config and the directory of a CMSSW installation, expand
        the configuration into the format needed for WMCore
        
        configuration is written to target if given, /tmp otherwise
        
        args is the list of command line arguments that should be passed to
        the configuration, similar to what would be placed after cmsRun <conf>
        
        returns the path to the configuration
        """
        pass
    
    def getConfig(self):
        """
        If localPath is set (i.e. if we expanded a config from this instance),
        return the path
        
        Otherwise, download the config from the ConfigCache
        
        returns the location of the configuration
        """
        pass
    
    

    
    