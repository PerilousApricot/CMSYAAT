'''
Created by Andrew Melo <andrew.melo@gmail.com> on Aug 14, 2012

'''
from WMCore.Credential.Proxy import Proxy as WMCoreProxy
from functools import wraps
import os
import logging


def requireProxy(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        proxyHelper = Proxy()
        proxyHelper.initProxy()
        os.environ['X509_USER_PROXY'] = proxyHelper.getProxyFilename()
        return f(*args, **kwds)
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
        self.helper = WMCoreProxy({'logger' : logging})

    def getProxyFilename(self):
        return self.helper.getProxyFilename()
            
    def initProxy(self):
        self.helper.create()
        
    def deleteProxy(self):
        self.helper.destroy()
    
    def uploadToMyproxy(self, allowedDN):
        self.helper.serverDN = allowedDN
        self.helper.delegate( None, True )
