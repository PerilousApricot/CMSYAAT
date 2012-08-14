'''
Created by Andrew Melo <andrew.melo@gmail.com> on Jul 11, 2012

'''

import glob
import os.path
import tempfile
import logging
import tarfile

from WMCore.Services.UserFileCache.UserFileCache import UserFileCache
import CMSYAAT.Utilities.SCRAMHelper

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
    

    def generateSandboxFromWorkingDirectory(self, workdir, fileName = None, extraFiles = []):
        rootDir = CMSYAAT.Utilities.SCRAMHelper.GetCMSSWRootFromPath(workdir)
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
            
        
                