'''
Created by Andrew Melo <andrew.melo@gmail.com> on Aug 9, 2012

'''

class RequestManager(object):
    '''
    Interface to WMAgent's RequestManager
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
    def listRequests(self):
        """
        Returns a list of requests owned by the user
        """
        raise NotImplementedError
    
    def submitRequest(self, request):
        """
        Given a request object, submit it to the reqmgr
        
        Returns a new request object initialized with the new remote ID
        """
        raise NotImplementedError
    
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
    