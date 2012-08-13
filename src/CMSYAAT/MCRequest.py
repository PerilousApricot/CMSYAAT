'''
Created by Andrew Melo <andrew.melo@gmail.com> on Aug 10, 2012

'''
from CMSYAAT.Request import Request

class MCRequest(Request):
    '''
    Specialisation of CMSYAAT.Request for MC-Generation requests
    
    Basically, if you don't have an input dataset, use this
    '''


    def __init__(self):
        '''
        Constructor
        '''
        Request.__init__(self)
        