'''
Created by Andrew Melo <andrew.melo@gmail.com> on Aug 13, 2012

Some helper functions for dealing with CMS' SCRAM tool
'''
import sys
import os.path
import subprocess

# TODO: Make cmsset_default.sh configurable
cmssetPaths = ['/uscmst1/prod/sw/cmsset_default.sh',
               '/opt/cms/cmsset_default.sh',
               '/gpfs21/grid/grid-app/cmssoft/cms/cmsset_default.sh']

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

class SCRAMWorkDirectory:
    """
    This class (when used in a with clause) will munge the current environment
    to match the result from source-ing cmsset_default.sh, and doing cmsenv in 
    the working directory
    
    This should abstract out "doing CMSSW things" to the point that users don't
    have to worry about source-ing environments and having things get mixed up
    because they used a terminal they used with a different environment
    """
    def __init__(self, path):
        self.scramPath = path
        
    def __enter__(self):
        global cmssetPaths
        self.currentScramPath = GetCMSSWRootFromPath( self.scramPath )

        # First keep track of the old environment
        self.oldEnvironment = dict(os.environ)
        self.oldPath        = sys.path[:]
        self.oldModules     = sys.modules.copy()
        
        sys.path    = []
        sys.modules = []

        for envScript in cmssetPaths:
            if os.path.exists( envScript ):

                # Then load the new environment
                cmsEnv = subprocess.Popen(\
                            'source %s ; cd %s/src ; eval `scramv1 runtime -sh` ; env ' % \
                                    (envScript, self.currentScramPath),
                            shell = True,
                            stdout = subprocess.PIPE)
                output, _ = cmsEnv.communicate()
                os.environ.clear()

                for line in output.split('\n'):
                    if len(line.split('=')) == 2:
                        k, v = line.split('=')
                        os.environ[k] = v
                # make sure we got the cms environment
                for path in os.environ['PATH'].split(os.pathsep):
                    if os.path.exists(os.path.join(path, 'cmsRun')):
                        return
                
                for path in os.environ['PYTHONPATH'].split(os.pathsep):
                    # index zero is the name of the script
                    sys.path.insert(1, path)
                # if we get here, we didn't get a valid CMS environment
                raise RuntimeError, "Couldn't find cmsRun using %s" % envScript
               
        # if we get here, we didn't find the script
        raise RuntimeError, "Couldn't find cmsset_default.sh"
    
    def __exit__(self, type, value, traceback):
        os.environ.clear()
        os.environ.update(self.oldEnvironment)
        sys.path    = self.oldPath[:]
        sys.modules = dict(self.oldModules)
        
        
        
        