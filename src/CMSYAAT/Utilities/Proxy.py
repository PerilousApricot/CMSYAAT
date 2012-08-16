'''
Created by Andrew Melo <andrew.melo@gmail.com> on Aug 14, 2012

'''
from WMCore.Credential.Proxy import Proxy as WMCoreProxy
from functools import wraps

def requireProxy(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        proxyHelper = Proxy()
        proxyHelper.initProxy()
    return wrapper

class Proxy(object):
    '''
    CMS uses proxies constantly. This class is a wrapper function around WMCore
    proxy handling, to allow the user to update/check/delete their proxy in
    myproxy and update/check the local proxy
    '''


    def __init__(self):
        '''
        Constructor
        '''
        pass
            
    def initProxy(self):
        helper = WMCoreProxy()
        helper.create()
        
    def deleteProxy(self):
        helper = WMCoreProxy()
        helper.destroy()
    
    def uploadToMyproxy(self, allowedDN):
        helper = WMCoreProxy()
        helper.serverDN = allowedDN
        helper.delegate( None, True )