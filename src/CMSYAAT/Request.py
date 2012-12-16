'''
Created by Andrew Melo <andrew.melo@gmail.com> on Aug 10, 2012

'''
import time
import math
from CMSYAAT.RequestManagerImpl.RequestManagerImpl import RequestManagerImpl
class Request(object):
    '''
    Represents one request to WMAgent. Roughly, one MC gen request or
    processing request
    
    Can be set with parameters, submitted to RequestManager and then
    monitored using the built-in properties
    
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.targetTeam = "TestingTeam"
        self.cacheTime = 10

    # some temporary functions
    def getTargetTeam(self):
        return self.targetTeam

    def setRequestDict(self, val):
        self.requestDict = val

    def getRequestDict(self):
        return self.requestDict

    def setWorkflowName(self, name):
        self.workflowName = name

    def getWorkflowName(self):
        return self.workflowName

    def getReqmgrUrl(self):
        return self.reqmgrUrl

    def setReqmgrUrl(self, url):
        self.reqmgrUrl = url

    def setWMStatUrl(self, url):
        self.wmstatUrl = url

    def getWMStatUrl(self):
        return self.wmstatUrl

    # TODO: metaprogramming
    def getWorkloadSummaryDocuments(self):
        if hasattr(self, '_workloadSummary') and \
                self._workloadSummary[1] + self.cacheTime > time.time():
            return self._workloadSummary[0][self.workflowName]
        else:
            reqmgr = RequestManagerImpl()
            summary = reqmgr.getRequestInfo(self.wmstatUrl,
                                                [self.workflowName])
            self._workloadSummary = [ summary, time.time() ]
            return self._workloadSummary[0][self.workflowName]

    def getJobSummaryDocuments(self):
        if hasattr(self, '_jobSummary') and \
                self._jobSummary[1] + self.cacheTime > time.time():
            return self._jobSummary[0][self.workflowName]
        else:
            reqmgr = RequestManagerImpl()
            summary = reqmgr.getJobSummary(self.wmstatUrl,
                                                [self.workflowName])
            self._jobSummary = [ summary, time.time() ]
            return self._jobSummary[0][self.workflowName]

    def getJobCountSummaryPerSite(self):
        summary = self.getWorkloadSummaryDocuments()
        retval = {}
        for key in summary:
            if not key.startswith('agent-'):
                continue
            for site in summary[key]['sites']:
                if not site in retval:
                    retval[site] = self.getJobCountSummary(site)
                else:
                    oneupdate = self.getJobCountSummary(site)
                    for k,v in oneupdate.iteritems():
                        retval[site][k] += v
        return retval

    def getJobCountSummary(self, site=None):
        summary = self.getWorkloadSummaryDocuments()
        total = int(math.floor(float(summary['request']['total_jobs'])))
        failed, submitted, resubmitted, running, cooloff, success = \
                (0,0,0,0,0,0)
        for key in summary:
            if not key.startswith('agent-'):
                continue
            if site:
                if not site in summary[key]['sites']:
                    continue
                status=summary[key]['sites'][site]
            else:
                status = summary[key]['status']
            if 'submitted' in status:
                submitted += status['submitted'].get('first',0)
                running   += status['submitted'].get('running',0)
                resubmitted += status['submitted'].get('queued', 0)
            if 'failure' in status:
                #logging.debug([val for val in \
                #                 status['failure'].values()])
                failed += sum([val for val in \
                                status['failure'].values()])
            success += status.get('success',0)
            if 'cooloff' in status:
                cooloff += sum([val for val in \
                                status['cooloff'].values()])

        return { 'failed' : failed, 'submitted' : submitted, 
                'resubmitted' : resubmitted, 'running' : running,
                'total' : total, 'cooloff': cooloff, 'success':success }

    def getJobResultsSummary(self):
        summary = self.getJobSummaryDocuments()
        sortByCount = sorted(summary['rows'], key=lambda x: -1 *x['value'])
        
        return {'bycount':sortByCount}
        # ["meloam_ASYNCTEST1_121215_092921_1181", "submitfailed", 61202, "T2_US_Vanderbilt", ["CondorError"]]
        

    def cancel(self):
        """
        Cancels the request. This doesn't actually slay all the jobs, and has
        some lag time. You should make sure a request is actually right before
        you submit it, or you're gonna burn a lot of fairshare
        """
        raise NotImplementedError
    
    def testInteractively(self):
        """
        Generates a WMAgent payload with the requested parameters, but with
        maxevents set to 1. This is a useful local check before submitting
        to the agent
        """
        raise NotImplementedError
    

    def setSandbox(self, sandbox):
        """
        Sets the sandbox for this request. Accepts a sandbox argument or a URL
        """
        raise NotImplementedError
    
    sandbox = property(None, setSandbox)
    
    
    def setCMSSWConfig(self, configuration):
        """
        Sets the required CMSSW configuration.
        
        """
        self.cmsswConfig = configuration
        raise NotImplementedError
    
    cmsswConfig = property(None, setCMSSWConfig)
    
    
    # returns the request information, as given by the remote reqmgr
    def getRequestInfo(self):
        raise NotImplementedError
    requestInfo = property(getRequestInfo)
    
    # returns a dict of
    #     jobStatus[task][state][ids]
    # to track the state of different jobs in the request
    #def getJobStatus(self):
    #    raise NotImplementedError
    #jobStatus = property(getJobStatus)
    
    # returns information about Active/Acquired/Complete WorkQueueElements
    # WQEs are the next largest division of a request above jobs. Basically,
    # a request is expanded into N WQEs, when are then each acquired by a
    # WMAgent. This helps scale the system by keeping an agent from having to
    # immediately generate EVERY job for every reqeust in the system. (A
    # typical WMAgent starts to keel over at 25k running/queued jobs)
    def getWorkqueueStatus(self):
        raise NotImplementedError
    workqueueStatus = property(getWorkqueueStatus)
    
    # returns information about the amount of processed input data.
    # Commented out for now, might add later
    def getInputStatus(self):
        raise NotImplementedError
    inputStatus = property(getInputStatus)
    
    # returns information about output files. Gives LFN/sites for all output
    # files and logs
    def getOutputStatus(self):
        raise NotImplementedError
    outputStatus = property(getOutputStatus)
