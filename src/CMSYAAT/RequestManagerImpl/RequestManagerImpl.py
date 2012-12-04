"""
Internal helpers to talk to the request manager
"""

import json
import httplib
import urllib
import datetime
from httplib import HTTPException
from CMSYAAT.Utilities.Proxy import requireProxy
from CMSYAAT.Utilities import Logging
logging = Logging.getLogger('CMSYAAT.ReqMgrImpl')

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

   
    def wrapCall(self, conn, verb, uri, params = {}, header = {} ):
        logging.debug("Making %s request to %s" % (verb, uri))
        if params != {}:
            logging.debug("Params are %s" % params)
        if header != {}:
            logging.debug("Headers are %s" % header)
        try:
            retval, status, reason, cached = \
                conn.makeRequest( uri = uri, verb = verb,
                                  data = params, incoming_headers=header )
        except HTTPException, e:
            logging.error("Call threw an HTTPException")
            if hasattr(e, 'result'):
                logging.error("Call result: %s" % e.result)
            if hasattr(e, 'reason'):
                logging.error("Reason: %s" % e.reason)
                print e.reason
            raise


        logging.debug("Request status was %s" % status)
        logging.debug("Request returned %s" % retval)
        return retval, status, reason, cached

    def listRequests(self, url):
        request = JSONRequests( url )
        retval, status, reason, _ = \
                self.wrapCall( request, 'GET', '/reqMgr/requestnames' )
        return retval
    # need to require proxies only if the URL is https
    #@requireProxy
    def makeRequest(self,url,params):
        request = JSONRequests( url )
        retval, status , reason , _ = \
                self.wrapCall( request, 'PUT', 
                               '/reqMgr/request', params )

        self.checkStatusOrComplain( 200, retval, status, reason )
        return retval['RequestName']

    def approveRequest(self,url,workflow):
        request = Requests( url )
        params = {"requestName": workflow,
                  "status": "assignment-approved"}
        retval,status,reason,_ = \
                    self.wrapCall( request, 'PUT',
                                    '/reqMgr/request', params)
        self.checkStatusOrComplain( 200, retval, status, reason )

    def assignRequest(self,url,workflow,team):
        # lame
        # https://github.com/dmwm/WMCore/blob/master/src/python/WMCore/HTTPFrontEnd/RequestManager/Assign.py#L177
        params = { 'requestName' : workflow,
                   'action' : 'Approve',
                   'Team' + team : 'checked',
                   'checkbox' + workflow : 'checked'}
    
        request = Requests( url )
        retval, status, reason, _ = \
                self.wrapCall( request, 'POST',
                                '/assign/handleAssignmentPage', 
                                params, self.headers )
        self.checkStatusOrComplain( 200, retval, status, reason )
