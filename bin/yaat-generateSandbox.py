#!/usr/bin/env python2.6

from optparse import OptionParser
from CMSYAAT.SandboxManager import SandboxManager

# TODO: Get some common options parsing
parser = OptionParser()
parser.add_option("-w", "--workdir", dest="workdir",
                  help="CMSSW Installation to upload")
parser.add_option("-o", "--output", dest="fileName",
                  help="Target filename",
                  default=None)
(options, args) = parser.parse_args()

factory = SandboxManager()
cache   = factory.newSandbox()
print cache.makeSandbox( options.workdir, target= options.fileName )
