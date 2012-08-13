'''
Created by Andrew Melo <andrew.melo@gmail.com> on Aug 9, 2012

'''
from CMSYAAT.Sandbox import Sandbox

class SandboxManager(object):
    '''
    Generates and stores tarballs with libraries from a CMSSW working area.
    '''


    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def newSandbox(self):
        """
        Makes a new, fresh sandbox object, ready to be populated
        """
        return Sandbox()
    
    def submitSandboxToUFC(self, sandbox):
        """
        Uploads the sandbox to a UFC instance, returns a new object
        attached to the remote value
        """
        raise NotImplementedError
    
    def submitSandboxToSE(self, sandbox): 
        """
        Uploads the sandbox to an SE, where it can be read by xrootd. returns
        a new objet attached to the remote value
        """
        raise NotImplementedError
        