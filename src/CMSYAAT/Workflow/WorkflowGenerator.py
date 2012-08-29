'''
Created by Andrew Melo <andrew.melo@gmail.com> on Jul 11, 2012

'''
import logging
import shutil
import tempfile
import os.path

from WMCore.Services.Requests import JSONRequests

class WorkflowGenerator(object):
    '''
    Represents a first pass at a job request API
    '''


    def __init__(self, logger = None):
        '''
        Constructor
        '''
        if logger:
            self.logger = logger
        else:
            self.logger = logging 
    
    def debugHttpError(self, data, status, reason):
        self.logger.debug("Http request failed")
        self.logger.debug("Status: %s" % status)
        self.logger.debug("Reason: %s" % reason)
        self.logger.debug("Data: %s" % data)
    
    def submitRequestToReqMgr(self, url, params):
        workflow = self.makeRequest(url, params)    
        self.approveRequest(url, workflow)
        self.assignRequest(url, workflow, team="CMSYAATTeam")
        
    def makeRequest(self, url, params):
        request = JSONRequests(url)
        headers  =  {"Content-type": "application/x-www-form-urlencoded",
                 "Accept": "text/plain"}

        request.post("/reqmgr/create/makeSchema", params, headers)
    
        (data, status, reason, _) = request.getresponse()
        if status != 303:
            self.debugHttpError(data, status, reason)            
            raise RuntimeError, "POST failed with code %s" % status
            
        workflow=data.split("'")[1].split('/')[-1]
        self.logger.info('Injected workflow:',workflow,'into',url)
        return workflow

    def approveRequest(self, url,workflow):
        params = {"requestName": workflow,              "status": "assignment-approved"}
        request = JSONRequests(url)
        headers  =  {"Content-type": "application/x-www-form-urlencoded",
                 "Accept": "text/plain"}
        request.put("/reqmgr/reqMgr/request", params, headers)
        
        (data, status, reason, _) = request.getresponse()
        if status != 200:
            self.debugHttpError(data, status, reason)            
            raise RuntimeError, "PUT failed with code %s" % status
        self.logger.info("Approved the workflow %s" % workflow)
        
    def produceWMWorkflow(self, params):
        from WMCore.WMSpec.StdSpecs.Analysis import AnalysisWorkloadFactory
        factory = AnalysisWorkloadFactory()
        return factory("DEMOWORKFLOW", params)
    
    def produceWMTask(self,params,taskName):
        from WMCore.WMSpec.StdSpecs.Analysis import AnalysisWorkloadFactory
        factory = AnalysisWorkloadFactory()
        return factory("DEMOWORKFLOW", params).getTask(taskName)
    
    def produceSandboxForWorkflow(self, workload, targetFile = None, includeWMCore = True ):
        """
        Given a workflow, builds a sandbox for interactive use
        """
        from WMCore.WMRuntime.SandboxCreator import SandboxCreator
        creator = SandboxCreator()
        if not includeWMCore:
            creator.disableWMCorePackaging()
        tempDir = tempfile.mkdtemp()
        try:
            tarballPath = creator.makeSandbox(tempDir, workload)
        finally:
            pass
        #    if os.path.exists( tempDir ):
        #        shutil.rmtree( tempDir )
        return tarballPath
           
    def assignRequest(self,url,workflow,team,site,args={}):
        params = {"action": "Assign",
                  "Team"+team: "checked",
                  "SiteWhitelist": [],
                  "SiteBlacklist": [],
                  "MergedLFNBase": "/store/user",
                  "UnmergedLFNBase": "/store/temp/user",
                  "MinMergeSize": 1,
                  "MaxMergeSize": 1,
                  "MaxMergeEvents": 50000,
                  #"AcquisitionEra": era,
                  "maxRSS": 4294967296,
                  "maxVSize": 4294967296,
                  "dashboard": "CMSYAATAnalysis",
                  "checkbox"+workflow: "checked"}
    
        request = JSONRequests(url)
        headers  =  {"Content-type": "application/x-www-form-urlencoded",
                 "Accept": "text/plain"}
        request.post("/reqmgr/assign/handleAssignmentPage", params, headers)
        
        (data, status, reason, _) = request.getresponse()
        if status != 200:
            self.debugHttpError(data, status, reason)            
            raise RuntimeError, "POST failed with code %s" % status
        self.logger.info("Assigned the workflow %s" % workflow)
        