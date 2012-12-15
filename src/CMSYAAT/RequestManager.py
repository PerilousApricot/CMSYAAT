'''
Created by Andrew Melo <andrew.melo@gmail.com> on Aug 9, 2012

'''

from CMSYAAT.Request import Request
# WARNING: Stick of redundancy stick
from CMSYAAT.RequestManagerImpl.RequestManagerImpl import RequestManagerImpl
class RequestManager(object):
    '''
    Client-Facing Interface to WMAgent's RequestManager
    '''


    def __init__(self, endpoint = "http://cmsweb.cern.ch/reqmgr"):
        '''
        Constructor
        '''
        self.endpoint = endpoint
    
    def listRequests(self):
        """
        Returns a list of requests in the reqmgr

        TODO add generator form
        """
        reqmgr = RequestManagerImpl()
        retval = []
        for request in reqmgr.listRequests(self.endpoint):
            tmpRequest = Request()
            tmpRequest.setReqmgrUrl( self.endpoint )
            tmpRequest.setWorkflowName( request['request_name'] )
            retval.append( tmpRequest )
        return retval

    
    def submitRequest(self, request):
        """
        Given a request object, submit it to the reqmgr
        
        Returns a new request object initialized with the new remote ID
        """
        reqmgr = RequestManagerImpl()
        workflow = reqmgr.makeRequest( self.endpoint, request.getRequestDict() )
        workflowName = workflow['RequestName']
        reqmgr.approveRequest( self.endpoint, workflow )
        reqmgr.assignRequest( self.endpoint, workflow, request.getTargetTeam() )
        request.setWorkflowName( workflowName )
        return request

    def submitRequestForTesting(self, request, renameRequestForTesting = True):
        """
        Submits a request to reqmgr for testing. This means fudgeing the job
        splitting algorithms to be as small as possible, forcing CMSSW to only
        process one event, turning down the stageout retries and pauses to zero
        
        Basically, tries to find the quickest way to test that your job wil
        work on the actual service
        
        To make the job show up separately in the request lists, the 
        renameRequestForTesting parameter will automagically prepend
        CMSYAAT-TEST to the beginning of the request string
        """
        raise NotImplementedError

    def newRequest(self):
        """
        Factory function to make a new blank request, initialized to point to
        this request manager
        """
        return Request( )
    
    def newMCRequest(self, request):
        """
        Factory function that returns new MC request objects, initialized to 
        point to this request manager
        """
        raise NotImplementedError
    
    def newProcessingRequest(self, request):
        """
        Factory function that returns new MC request objects, initialized to 
        point to this request manager
        """
        raise NotImplementedError
    
