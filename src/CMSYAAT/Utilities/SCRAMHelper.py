'''
Created by Andrew Melo <andrew.melo@gmail.com> on Aug 13, 2012

Some helper functions for dealing with CMS' SCRAM tool
'''
import os.path

def GetCMSSWRootFromPath(workdir):
    original = workdir
    x = 0
    while x < 100: # sanity check
        if os.path.exists(os.path.join(workdir, ".SCRAM")):
            return os.path.abspath(workdir)
        else:
            x = x + 1
            workdir = os.path.normpath( workdir + "/.." )
    raise RuntimeError, "The path %s doesn't appear to be a CMSSW installation" % original
