'''
Created by Andrew Melo <andrew.melo@gmail.com> on Aug 10, 2012

'''

from CMSYAAT.FileCache.SandboxCache import SandboxCache
from CMSYAAT.Utilities.SCRAMHelper import GetCMSSWRootFromPath

class Sandbox(object):
    '''
    Represents one sandbox, which is additional libraries or data needed to
    make a configuration run with CMSSW. It is downloaded to the WN and
    unpacked just before cmsRun is executed
    
    Sandboxes can be stored in UserFileCache (managed centrally) or on a SE
    with xrootd attached (useful for temporary testing)
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.url = None
    
    def makeSandbox(self, directory, target = None):
        """
        Generates a tarball from the directory given. Handles setting the
        CMSSW environment in a subshell so you don't have to.
        
        Writes the tarball to target if given, otherwise a file in /tmp will
        be made
        
        returns the path of the tarball
        """
        helper = SandboxCache()
        self.directory = GetCMSSWRootFromPath(directory)
        self.tarballPath = helper.generateSandboxFromWorkingDirectory(\
                                        self.directory, target)
        return self.tarballPath
        
    def getSandbox(self, target = None):
        """
        If self.url is set, pulls the sandbox from there.
        
        target specifies the output file, a tempfile is used otherwise
        
        returns the path of the tarball
        """
        raise NotImplementedError