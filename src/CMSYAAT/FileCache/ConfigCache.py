"""
Module to handle CMSSW _cfg.py file

Gypsied from CrabClient (which pulled from inject-to-config-cache)
This should probably be merged back into WMCore
"""

import imp
import json
import os
import sys
import logging
import tempfile

from WMCore.Cache.WMConfigCache import ConfigCache
from PSetTweaks.WMTweak import makeTweak

from CMSYAAT.Utilities.Proxy import requireProxy
from CMSYAAT.Utilities.SCRAMHelper import SCRAMWorkDirectory

class ConfigCache(object):
    """
    Class to handle CMSSW _cfg.py file
    """
    def __init__(self, logger=None):
        if logger:
            self.logger = logger
        else:
            self.logger = logging
                
    def loadConfig(self, configPath, arguments = [], scramDir = ""):
        """
        _loadConfig_
    
        Import a config.
        """
        self.logger.info("Importing the config, this may take a while...")
        sys.stdout.flush()
        with SCRAMWorkDirectory( scramDir ):
            cfgBaseName = os.path.basename(configPath).replace(".py", "")
            cfgDirName = os.path.dirname(configPath)
            modPath = imp.find_module(cfgBaseName, [cfgDirName])
            originalArgv = sys.argv
            try:
                if arguments:
                    sys.argv = [configPath]
                    sys.argv.extend(arguments)
                    
                loadedConfig = imp.load_module(cfgBaseName, modPath[0],
                                               modPath[1], modPath[2])
            finally:
                if arguments:
                    sys.argv = originalArgv
              
        self.logger.info("done")
        
        return loadedConfig
    
    @requireProxy
    def upload(self, configModule, group, userDN,
               label="Autogenerated by YAAT",
               description="Autogenerated by YAAT",
               url="http://se2.accre.vanderbilt.edu:5984",
               database="wmagent_configcache"):
        
        if url.endswith('/'):
            raise RuntimeError, "URL shouldn't have a trailing slash"
        configCache = ConfigCache(url, database)
        configCache.createUserGroup(group, userDN)
        tweaks = makeTweak(configModule.process).jsondictionary()
        fileName = tempfile.mkstemp()
        try:
            filename = self.writeFile(configModule, fileName)
            configCache.addConfig(filename)
            configCache.setPSetTweaks(tweaks)
            configCache.setLabel(label)
            configCache.setDescription(description)
            configCache.save()
        finally:
            if os.path.exists(fileName):
                os.unlink(fileName)
        targetUrl = "%s/%s/%s/configFile" % (url, database, configCache.document["_id"])
        
        return targetUrl

    def writeFile(self, sourceModule, filename):
        """
        write to tempfile FIXME
        Persist fully expanded _cfg.py file
        """
        
        self.outputFile = filename
        self.logger.debug("Writing CMSSW config to %s" % self.outputFile)
        outFile = open(filename, "wb")
        outFile.write("import FWCore.ParameterSet.Config as cms\n")
        outFile.write(sourceModule.dumpPython())
        outFile.close()
        
        return filename


