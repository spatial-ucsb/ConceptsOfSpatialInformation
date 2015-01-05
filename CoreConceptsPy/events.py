# -*- coding: utf-8 -*-

"""
TODO: description of module
"""

__author__ = "Marc Tim Thiemann"
__copyright__ = "Copyright 2014"
__credits__ = ["Marc Tim Thiemann", "Andrea Ballatore"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = ""
__email__ = ""
__date__ = "December 2014"
__status__ = "Development"

from utils import _init_log
from coreconcepts import CcEvent

log = _init_log("events")

class PyEvent(CcEvent):

    def __init__(self, startTime, endTime = 0):
        # TODO: endTime default value should be 'None' (unless there's a good reason to set it to 0).
        # TODO: assert that endTime >= startTime
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
        return self.startTime >= event.startTime and self.endTime <= event.endTime

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
