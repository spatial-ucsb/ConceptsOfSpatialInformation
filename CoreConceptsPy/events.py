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

    def during( self, eventOrStartTime, endTime = None ):
        """
        @param event an event
        @return boolean
        """

        # Check if types are correct
        if endTime != None:
            if not isinstance(eventOrStartTime, datetime.datetime):
                raise ValueError('Expected <type \'datetime.datetime\'> for eventOrStartTime, because endTime was passed, got ' + str(type(eventOrStartTime)))
            elif not isinstance(endTime, datetime.datetime):
                raise ValueError('Expected <type \'datetime.datetime\'> for endTime, got ' + str(type(endTime)))
        elif not isinstance(eventOrStartTime, CcEvent):
            raise ValueError('Expected <type \'CcEvent\'> for eventOrStartTime, because endTime was not passed, got ' + str(type(eventOrStartTime)))

        if endTime == None:
            return self.startTime >= eventOrStartTime.startTime and (eventOrStartTime.endTime == None or (self.endTime != None and self.endTime <= eventOrStartTime.endTime))
        else:
            return self.startTime >= eventOrStartTime and (self.endTime != None and self.endTime <= endTime)

    def before( self, eventOrDatetime ):
        """
        @param event an event
        @return Boolean
        """

        if isinstance(eventOrDatetime, datetime.datetime):
            return self.endTime != None and self.endTime < eventOrDatetime
        elif isinstance(eventOrDatetime, CcEvent):
            return self.endTime != None and self.endTime < eventOrDatetime.startTime
        else:
            raise ValueError('Expected <type \'CcEvent\'> or <type \'datetime.datetime> as parameter, got ' + str(type(eventOrDatetime)))

    def after( self, eventOrDatetime ):
        """
        @param event an event
        @return Boolean
        """

        if isinstance(eventOrDatetime, datetime.datetime):
            return self.startTime > eventOrDatetime.endTime
        elif isinstance(eventOrDatetime, CcEvent):
            return eventOrDatetime.endTime != None and self.startTime > eventOrDatetime.endTime
        else:
            raise ValueError('Expected <type \'CcEvent\'> or <type \'datetime.datetime> as parameter, got ' + str(type(eventOrDatetime)))

    def overlap( self, eventOrStartTime, endTime = None ):
        """
        @param event an event
        @return Boolean
        """

        # Check if types are correct
        if endTime != None:
            if not isinstance(eventOrStartTime, datetime.datetime):
                raise ValueError('Expected <type \'datetime.datetime\'> for eventOrStartTime, because endTime was passed, got ' + str(type(eventOrStartTime)))
            elif not isinstance(endTime, datetime.datetime):
                raise ValueError('Expected <type \'datetime.datetime\'> for endTime, got ' + str(type(endTime)))
        elif not isinstance(eventOrStartTime, CcEvent):
            raise ValueError('Expected <type \'CcEvent\'> for eventOrStartTime, because endTime was not passed, got ' + str(type(eventOrStartTime)))

        if endTime == None:
            event = eventOrStartTime
            return (self.startTime < event.startTime and self.endTime != None and (event.endTime == None or self.endTime < event.endTime) and self.endTime >= event.startTime) or (self.startTime > event.startTime and event.endTime != None and self.startTime <= event.endTime and (self.endTime == None or self.endTime > event.endTime))
        else:
            startTime = eventOrStartTime
            return (self.startTime < startTime and self.endTime != None and self.endTime < endTime and self.endTime >= startTime) or (self.startTime > startTime and self.startTime <= endTime and self.endTime > endTime)
