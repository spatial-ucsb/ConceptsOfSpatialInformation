from coreconcepts import AEvents, Event, Period

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

class SomeConcreteEvents(AEvents):

	@staticmethod
    def within( ev ):
        """
        @ev an event
        @return a Period 
        """
        return ev.period
    
    @staticmethod
    def when( ev ):
        """
        @ev an event
        @return a Period 
        """
        return ev.period
    
    @staticmethod
    def during( ev, otherEv ):
        """
        @ev an event
        @ev otherEvent another event
        @return boolean
        """
        return ev.getStartTime >= otherEv.getStartTime and ev.getEndTime <= otherEv.getEndTime
    
    @staticmethod
    def before( ev, otherEv ):
        """
        @ev an event
        @ev otherEvent another event
        @return boolean
        """
        return ev.getEndTime < otherEv.getStartTime
    
    @staticmethod
    def after( ev, otherEv ):
        """
        @ev an event
        @ev otherEvent another event
        @return boolean
        """
        return ev.getStartTime > otherEv.getEndTime
    
    @staticmethod
    def overlap( ev, otherEv ):
        """
        @ev an event
        @ev otherEvent another event
        @return boolean
        """
        return (ev.getStartTime < otherEv.getStartTime and ev.getEndTime < otherEv.getEndTime and ev.getEndTime >= otherEv.getStartTime) or (ev.getStartTime > otherEv.getStartTime and ev.getStartTime <= otherEv.getEndTime and ev.getEndTime > otherEv.getEndTime)
    
class Event(object):
    """ Simple event class. TODO: implement"""
    
    __init__(self, period):
    	self.period = period

    def getStartTime(self):
    	return self.period.startTime

    def getEndTime(self):
    	return self.period.endTime

class Period(object):
    """ Simple period class. TODO: implement"""
    
    __init__(self, startTime, endTime):
    	self.startTime = startTime
    	self.endTime = endTime