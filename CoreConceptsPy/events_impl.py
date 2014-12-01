from coreconcepts_oo import CCEvent

"""
 Module abstract goes here.
"""

__author__ = "Werner Kuhn and Andrea Ballatore"
__copyright__ = "Copyright 2014"
__credits__ = ["Werner Kuhn", "Andrea Ballatore"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = ""
__email__ = ""
__date__ = "August 2014"
__status__ = "Development"

from utils import _init_log

log = _init_log("networks_impl")

class CCEvent(Object):

    def __init__(self, startTime, endTime = 0):
        self.startTime = startTime;
        self.endTime = startTime if endTime == 0 else endTime;
    
    def within( self ):
        """
        @return a Period 
        """
        return (self.startTime, self.endTime)
    
    def when( self ):
        """
        @return a Date 
        """
        return self.startTime;
    
    def during( self, event ):
        """
        @param event an event
        @return boolean
        """
        return self.startTime >= event.startTime and self.endndTime <= event.endTime
    
    def before( self, event ):
        """
        @param event an event
        @return Boolean
        """
        return self.endTime < event.startTime
    
    def after( self, event ):
        """
        @param event an event
        @return Boolean
        """
        return self.startTime > event.endTime
    
    def overlap( self, event ):
        """
        @param event an event
        @return Boolean
        """
        return (self.startTime < event.startTime and self.endTime < event.endTime and self.endTime >= event.startTime) or (self.startTime > event.startTime and self.startTime <= event.endTime and self.endTime > event.endTime)