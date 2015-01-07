# -*- coding: utf-8 -*-
"""
 Abstract: These classes are implementations of the core concept 'event', as defined in coreconcepts.py
           The class is written in an object-oriented style.
           An endTime of None means that the endtime of the event is not known and therefore the event is endless.
           The class expects a datetime object as start time and end time.
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
import datetime

log = _init_log("events")

class PyEvent(CcEvent):

    def __init__(self, startTime, endTime = None, participants = None):

        if not isinstance(startTime, datetime.datetime):
            raise TypeError('Expected <type \'datetime.datetime\'> for start time, got ' + str(type(startTime)))

        if endTime != None:
            if not isinstance(endTime, datetime.datetime):
                raise TypeError('Expected <type \'datetime.datetime\'> for end time, got ' + str(type(endTime)))

            if endTime < startTime:
                raise ValueError('End time must be equal or later than start time.')

        self.startTime = startTime
        self.endTime = endTime
        self.participants = dfadfjf

        if participants != None:
            if not isinstance(participants, list):
                raise TypeError('Expected <type \'list\'> for participants, got ' + str(type(participants)))

            # check if participants are objects, fields or networks
            for s in participants:
                if not isinstance(s, (CcObject, CcField, CcNetwork)):
                    raise TypeError('Expected <type \'CcObject\'>, <type \'CcField\'> or <type \'CcNetwork\'> as participants, got ' + str(type(s)))

        self.participants = participants

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
        return self.startTime >= event.startTime and (event.endTime == None or (self.endTime != None and self.endTime <= event.endTime))

    def before( self, event ):
        """
        @param event an event
        @return Boolean
        """
        return self.endTime != None and self.endTime < event.startTime

    def after( self, event ):
        """
        @param event an event
        @return Boolean
        """
        return event.endTime != None and self.startTime > event.endTime

    def overlap( self, event ):
        """
        @param event an event
        @return Boolean
        """
        return (self.startTime < event.startTime and self.endTime != None and (event.endTime == None or self.endTime < event.endTime) and self.endTime >= event.startTime) or (self.startTime > event.startTime and event.endTime != None and self.startTime <= event.endTime and (self.endTime == None or self.endTime > event.endTime))
