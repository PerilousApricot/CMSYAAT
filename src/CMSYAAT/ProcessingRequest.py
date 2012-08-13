'''
Created by Andrew Melo <andrew.melo@gmail.com> on Aug 10, 2012

'''
from CMSYAAT.Request import Request

class ProcessingRequst(Request):
    '''
    Specialization of CMSYAAT.Request for processing requests
    
    Basically, if you take an input dataset, run CMSSW on it and get files
    back, use this
    '''


    def __init__(self):
        '''
        Constructor
        '''
        Request.__init__(self)