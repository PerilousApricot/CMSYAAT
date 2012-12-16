"""
Internal helpers to talk to the request manager
"""

import json
import httplib
import urllib
import datetime
import pprint
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

    def getJobSummary(self,url,requestNames):
        request = JSONRequests( url )
        retval = {}
        # get the ID(s) of the latest status doc(s)
        for oneReq in requestNames:
            startkey = urllib.quote_plus('["%s"]' % oneReq)
            endkey   = urllib.quote_plus('["%s",{}]' % oneReq)
            jobstatus, status, reason, _ = \
                self.wrapCall( request, 'GET',
                                '/_design/WMStats/_view/jobsByStatusWorkflow?reduce=true&group=true&startkey=%s&endkey=%s' % ( startkey, endkey ) )
            self.checkStatusOrComplain( 200, jobstatus, status, reason )
            retval[oneReq] = jobstatus
        return retval

    def getRequestInfo(self,url,requestNames):
        request = JSONRequests( url )
        
        # get the static docs
        alldocs = requestNames[:]
        # get the ID(s) of the latest status doc(s)
        for oneReq in requestNames:
            startkey = urllib.quote_plus('["%s",{}]' % oneReq)
            endkey   = urllib.quote_plus('["%s"]' % oneReq)
            statusids, status, reason, _ = \
                self.wrapCall( request, 'GET',
                                '/_design/WMStats/_view/latestRequest?descending=true&reduce=true&group=true&startkey=%s&endkey=%s' % ( startkey, endkey ) )
            self.checkStatusOrComplain( 200, statusids, status, reason ) 
            for row in statusids['rows']:
                alldocs.append(row['value']['id'])

        # get the updated docs
        reqinfo, status, reason, _ = \
                self.wrapCall( request, 'POST',
                                '/_all_docs?include_docs=true',
                                {'keys':alldocs} )
        self.checkStatusOrComplain( 200, reqinfo, status, reason )

        retval = {}
        for onereq in requestNames:
            retval[onereq] = {}
            for onedoc in reqinfo['rows']:
                if not onereq == onedoc['doc']['workflow']:
                    continue
                if onedoc['doc']['type'] == 'reqmgr_request':
                    retval[onereq]['request'] = onedoc['doc']
                elif onedoc['doc']['type'] == 'agent_request':
                    retval[onereq]['agent-'+onedoc['doc']['agent_url']] = \
                            onedoc['doc']
                else:
                    raise RuntimeError, "Got an unknown document type!"
        return retval

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
        return retval

    def approveRequest(self,url,workflow):
        request = Requests( url )
        params = {"requestName": workflow['RequestName'],
                  "status": "assignment-approved"}
        retval,status,reason,_ = \
                    self.wrapCall( request, 'PUT',
                                    '/reqMgr/request', params)
        self.checkStatusOrComplain( 200, retval, status, reason )

    def assignRequest(self,url,workflow,team):
        # lame
        # https://github.com/dmwm/WMCore/blob/master/src/python/WMCore/HTTPFrontEnd/RequestManager/Assign.py#L177
        params = workflow
        params.update( { 'requestName' : workflow['RequestName'],
                   'action' : 'Approve',
                   'Team' + team : 'checked',
                   'checkbox' + workflow['RequestName'] : 'checked',
                   'AcquisitionEra' : 'v1',
                   'ProcessingVersion' : 'v1'})
        params['WorkloadSpec'] = None
        request = Requests( url )
        retval, status, reason, _ = \
                self.wrapCall( request, 'POST',
                                '/assign/handleAssignmentPage', 
                                params, self.headers )
        self.checkStatusOrComplain( 200, retval, status, reason )
