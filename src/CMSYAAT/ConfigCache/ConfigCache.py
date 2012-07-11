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

from WMCore.Cache.WMConfigCache import ConfigCache as WMConfigCache
from PSetTweaks.WMTweak import makeTweak

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
    
        
    def upload(self, configModule, group, userDN,
               label="Autogenerated by YAAT",
               description="Autogenerated by YAAT",
               url="http://se2.accre.vanderbilt.edu:5984",
               database="wmagent_configcache"):
        
        if url.endswith('/'):
            raise RuntimeError, "URL shouldn't have a trailing slash"
        configCache = WMConfigCache(url, database)
        configCache.createUserGroup(group, userDN)
        tweaks = makeTweak(configModule.process).jsondictionary()
        filename = self.writeFile(configModule)
        configCache.addConfig(filename)
        configCache.setPSetTweaks(tweaks)
        configCache.setLabel(label)
        configCache.setDescription(description)
        configCache.save()
        targetUrl = "%s/%s/%s/configFile" % (url, database, configCache.document["_id"])
        return targetUrl

    def writeFile(self, filename=''):
        """
        write to tempfile FIXME
        Persist fully expanded _cfg.py file
        """

        self.outputFile = filename
        self.logger.debug("Writing CMSSW config to %s" % self.outputFile)
        outFile = open(filename, "wb")
        outFile.write("import FWCore.ParameterSet.Config as cms\n")
        outFile.write(self.fullConfig.process.dumpPython())
        outFile.close()

        return


    def outputFiles(self):
        """
        Returns a tuple of lists of output files. First element is TFileService files,
        second is PoolOutput files
        """

        tFiles = []
        poolFiles = []

        # Find TFileService
        if self.fullConfig.process.services.has_key('TFileService'):
            tFileService = self.fullConfig.process.services['TFileService']
            if "fileName" in tFileService.parameterNames_():
                tFiles.append(getattr(tFileService, 'fileName', None).value())

        # Find files written by output modules
        poolFiles = []
        outputModuleNames = self.fullConfig.process.outputModules_().keys()

        for outputModName in outputModuleNames:
            outputModule = getattr(self.fullConfig.process, outputModName)
            poolFiles.append(outputModule.fileName.value())

        # If there are multiple output files, make sure they have filterNames set
        if len(outputModuleNames) > 1:
            for outputModName in outputModuleNames:
                try:
                    outputModule = getattr(self.fullConfig.process, outputModName)
                    dataset      = getattr(outputModule, 'dataset')
                    filterName   = getattr(dataset, 'filterName')
                except AttributeError:
                    raise RuntimeError('Your output module %s does not have a "dataset" PSet ' % outputModName +
                                       'or the PSet does not have a "filterName" member.')

        return tFiles, poolFiles
