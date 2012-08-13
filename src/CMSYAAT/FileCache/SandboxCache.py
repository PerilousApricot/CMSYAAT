'''
Created by Andrew Melo <andrew.melo@gmail.com> on Jul 11, 2012

'''

import os
import glob
import os.path
import tempfile
import logging
import tarfile
from contextlib import closing

from WMCore.Services.UserFileCache.UserFileCache import UserFileCache
import CMSYAAT.Utilities.SCRAMHelper

def filterTar(x):
    if 'CVS' in x or\
       '.svn' in x or\
       '.git' in x:
        return True
    else:
        return False

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
            fileHandle = os.fdopen( fileHandle, 'w' )
        else:
            fileHandle = open( fileName, "w")

        print "rootDir is %s" % rootDir
        globsToAdd = ['lib','module','src/*/data', 'src/*/*/data', 'src/*/*/*/data']
        globsToAdd.extend( extraFiles )
        filesToAdd = []
        
        for oneGlob in globsToAdd:
            filesToAdd.extend( glob.iglob( os.path.join( rootDir, oneGlob) ) )
        
        rootDir = os.path.split( rootDir )[0]
        with closing(tarfile.open( fileobj = fileHandle, mode = "w|gz" )) as tar:
            for oneFile in filesToAdd:
                fileToAdd = os.path.join( rootDir, oneFile )
                pathToAdd = os.path.relpath( oneFile, rootDir )
                print "File: %s Path: %s" % (fileToAdd, pathToAdd)
                print "Root: %s File: %s" % (rootDir, oneFile)
                tar.add( fileToAdd,
                         pathToAdd,
                         exclude = filterTar)
        
        self.sandbox = fileName
        return fileName
    
    def uploadSandboxToUFC( self, url, sandbox = None, name = "YAATFile" ):
        if not sandbox:
            sandbox = self.sandbox
        req = UserFileCache( { 'endpoint' : url} )
        return req.upload( sandbox, name )
            
        
                
