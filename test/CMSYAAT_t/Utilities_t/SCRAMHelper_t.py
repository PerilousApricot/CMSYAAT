'''
Created by Andrew Melo <andrew.melo@gmail.com> on Aug 14, 2012

'''
import unittest
import os.path
import shutil
import subprocess
import tempfile
from CMSYAAT.Utilities.SCRAMHelper import SCRAMWorkDirectory, cmssetPaths

class ScramProjectMaker:
    """
    helper class to make scram projects
    
    """
    def makeProject(self, install_path):
        global cmssetPaths
        projectCommand = """source %(source_dir)s 
VERSION=$(scramv1 list CMSSW | egrep 'CMSSW\s*CMSSW' | head -n1 | awk '{ print $2; }')
cd %(install_path)s
echo $VERSION
scram p $VERSION
"""     
        for envScript in cmssetPaths:
            if os.path.exists(envScript):
                cmsEnv = subprocess.Popen(\
                    projectCommand % { 'source_dir' : envScript,
                                       'install_path' : install_path},
                    shell = True,
                    stdout = subprocess.PIPE)
                output, _ = cmsEnv.communicate()
                versionLine = output.split('\n')[0]
                return versionLine
                
class testSCRAMHelper_t(unittest.TestCase):
    '''
    Testing scram helper
    '''
    
    def setUp(self):
        """
        set up a CMS project for this test
        """
        self.cmsProject = tempfile.mkdtemp()
        maker = ScramProjectMaker()
        self.version = maker.makeProject(self.cmsProject).strip(' \t\n\r')
        self.scramDir = os.path.join(self.cmsProject, self.version)
    
    def tearDown(self):
        if hasattr(self, 'cmsProject') and self.cmsProject:
            shutil.rmtree( self.cmsProject, True )
            

    def testEnvironmentHelper(self):
        with SCRAMWorkDirectory( self.scramDir ) as scramDir:
            pass
        
if __name__ == '__main__':
    import nose
    nose.run(defaultTest ="_t")