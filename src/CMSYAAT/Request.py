'''
Created by Andrew Melo <andrew.melo@gmail.com> on Aug 10, 2012

'''

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
    def getJobStatus(self):
        raise NotImplementedError
    jobStatus = property(getJobStatus)
    
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
