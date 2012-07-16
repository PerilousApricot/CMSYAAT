'''
Created by Andrew Melo <andrew.melo@gmail.com> on Jul 11, 2012

'''

import glob
import os.path
import tempfile
import logging
import tarfile

from WMCore.Services.UserFileCache.UserFileCache import UserFileCache

class SandboxCache(object):
    '''
    Handles generating and uploading Sandboxes to a cache
    '''

    def __init__(self, logger=None):
        self.sandbox = None
        if logger:
            self.logger = logger
        else:
            self.logger = logging
    
    def getCMSSWRootFromPath(self, workdir):
        original = workdir
        x = 0
        while x < 100: # sanity check
            if os.path.exists(os.path.join(workdir, ".SCRAM")):
                return os.path.abspath(workdir)
            else:
                x = x + 1
                workdir = os.path.normpath( workdir + "/.." )
        raise RuntimeError, "The path %s doesn't appear to be a CMSSW installation" % original
    
    def generateSandboxFromWorkingDirectory(self, workdir, fileName = None, extraFiles = []):
        rootDir = self.getCMSSWRootFromPath(workdir)
        if not fileName:
            (fileHandle, fileName) = tempfile.mkstemp()
        else:
            fileHandle = open( fileName, "w")
        
        globsToAdd = ['lib','module','src/*/data', 'src/*/*/data', 'src/*/*/*/data']
        globsToAdd.extend(extraFiles)
        filesToAdd = []
        
        for oneGlob in globsToAdd:
            filesToAdd.extend( glob.iglob( oneGlob ) )
            
        with tarfile.open( fileHandle, "w|gz" ) as tar:
            for oneFile in filesToAdd:
                tar.add( os.path.join( rootDir, oneFile),
                         oneFile )
        
        self.sandbox = fileName
        return fileName
    
    def uploadSandboxToUFC( self, url, sandbox = None, name = "YAATFile" ):
        if not sandbox:
            sandbox = self.sandbox
        req = UserFileCache( { 'endpoint' : url} )
        return req.upload( sandbox, name )
            
        
                