"""
Internal helpers to talk to the request manager
"""

import json
import httplib
import urllib
import datetime
from httplib import HTTPException
from CMSYAAT.Utilities.Proxy import requireProxy
from WMCore.Services.Requests import Requests, JSONRequests

class RequestManagerImpl:
    """
    Not a public interface, this is gross for now
    """
    def __init__(self):
        self.headers = {'User-agent':                                        
                            "CMSYAAT 1.0 github.com/PerilousApricot/CMSYAAT"}
        pass

    def checkStatusOrComplain( self, wantedStatus, retval, status, reason ):
        if status != wantedStatus:
            raise RuntimeError, ("Got HTTP code %s, expected %s \n" +
                                 "reason: %s \n" +
                                 "data: %s \n") % (status, wantedStatus,
                                                    reason, retval )

    # need to require proxies only if the URL is https
    #@requireProxy
    def makeRequest(self,url,params):
        request = JSONRequests( url )
        params['status'] = 'assignment-approved'
        try:
            retval, status , reason , _ = \
                    request.put( '/reqMgr/request', params )
        except HTTPException, e:
            if hasattr(e, 'result'):
                print e.result
            if hasattr(e, 'reason'):
                print e.reason
            raise

        self.checkStatusOrComplain( 200, retval, status, reason )
        return retval['RequestName']
        
    def assignRequest(self,url,workflow,team):
        # lame
        # https://github.com/dmwm/WMCore/blob/master/src/python/WMCore/HTTPFrontEnd/RequestManager/Assign.py#L177
        params = { 'requestName' : workflow,
                   'action' : 'Approve',
                   'Team' + team : 'checked',
                   'checkbox' + workflow : 'checked'}
    
        request = Requests( url )
        retval, status, reason, _ = \
                request.post( '/reqmgr/assign/handleAssignmentPage', 
                                params, self.headers )
        self.checkStatusOrComplain( 200, retval, status, reason )
