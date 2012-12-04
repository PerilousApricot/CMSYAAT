"""
Configuration/convenience functions for CMSYAAT logging
"""

import logging

def initLogging():
    logging.basicConfig()

def getLogger(logName = 'root'):
    return logging.getLogger(logName)
