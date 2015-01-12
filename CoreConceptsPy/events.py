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

    def __init__(self, period, properties):
        """
        @param period a tuple of datetime objects
        @param properties a dictionary of key-value pairs
        """

        if isinstance(period, tuple):
            if len(period) != 2:
                raise RuntimeError('Tuple must be of length 2, length is ' + str(len(period)))
            elif not isinstance(period[0], datetime.datetime):
                raise TypeError('Expected <type \'datetime.datetime\'> as start time, got ' + str(type(period[0])))
            elif not (isinstance(period[1], datetime.datetime) or period[1] == None):
                raise TypeError('Expected <type \'datetime.datetime\'> or \'None\' as end time, got ' + str(type(period[1])))
            elif period[1] != None and period[1] < period[0]:
                raise ValueError('End time must be equal or later than start time')

        self.startTime = period[0]
        self.endTime = period[1]

        if not (isinstance(properties, dict)):
            raise TypeError('Expected <type \'dict\'> for properties, got ' + str(type(properties)))

        if not properties:
            raise RuntimeError('Properties dictionary can not be empty.')

        self.properties = properties

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

    def during( self, eventOrPeriod ):
        """
        @param eventOrPeriod an event or a time period
        @return boolean
        """

        # Check if parameter is correct
        if isinstance(eventOrPeriod, tuple):
            if len(eventOrPeriod) != 2:
                raise RuntimeError('Tuple must be of length 2, length is ' + str(len(eventOrPeriod)))
            elif not isinstance(eventOrPeriod[0], datetime.datetime):
                raise TypeError('Expected <type \'datetime.datetime\'> as start time, got ' + str(type(eventOrPeriod[0])))
            elif not isinstance(eventOrPeriod[1], datetime.datetime):
                raise TypeError('Expected <type \'datetime.datetime\'> as end time, got ' + str(type(eventOrPeriod[1])))
            elif eventOrPeriod[1] < eventOrPeriod[0]:
                raise ValueError('End time must be equal or later than start time')
        elif not isinstance(eventOrPeriod, CcEvent):
            raise TypeError('Expected <type \'CcEvent\'> or <type \'Tuple\'>, got ' + str(type(eventOrPeriod)))

        if not isinstance(eventOrPeriod, tuple):
            event = eventOrPeriod
            return self.startTime >= event.startTime and (event.endTime == None or (self.endTime != None and self.endTime <= event.endTime))
        else:
            return self.startTime >= eventOrPeriod[0] and (self.endTime != None and self.endTime <= eventOrPeriod[1])

    def before( self, eventOrDatetime ):
        """
        @param eventOrDatetime an event or a datetime object
        @return Boolean
        """

        if isinstance(eventOrDatetime, datetime.datetime):
            return self.endTime != None and self.endTime < eventOrDatetime
        elif isinstance(eventOrDatetime, CcEvent):
            return self.endTime != None and self.endTime < eventOrDatetime.startTime
        else:
            raise TypeError('Expected <type \'CcEvent\'> or <type \'datetime.datetime> as parameter, got ' + str(type(eventOrDatetime)))

    def after( self, eventOrDatetime ):
        """
        @param eventOrDatetime an event or a datetime object
        @return Boolean
        """

        if isinstance(eventOrDatetime, datetime.datetime):
            return self.startTime > eventOrDatetime
        elif isinstance(eventOrDatetime, CcEvent):
            return eventOrDatetime.endTime != None and self.startTime > eventOrDatetime.endTime
        else:
            raise TypeError('Expected <type \'CcEvent\'> or <type \'datetime.datetime> as parameter, got ' + str(type(eventOrDatetime)))

    def overlap( self, eventOrPeriod ):
        """
        @param eventOrPeriod an event or a time period
        @return Boolean
        """

        # Check if parameter is correct
        if isinstance(eventOrPeriod, tuple):
            if len(eventOrPeriod) != 2:
                raise RuntimeError('Tuple must be of length 2, length is ' + str(len(eventOrPeriod)))
            elif not isinstance(eventOrPeriod[0], datetime.datetime):
                raise TypeError('Expected <type \'datetime.datetime\'> as start time, got ' + str(type(eventOrPeriod[0])))
            elif not isinstance(eventOrPeriod[1], datetime.datetime):
                raise TypeError('Expected <type \'datetime.datetime\'> as end time, got ' + str(type(eventOrPeriod[1])))
            elif eventOrPeriod[1] < eventOrPeriod[0]:
                raise ValueError('End time must be equal or later than start time')
        elif not isinstance(eventOrPeriod, CcEvent):
            raise TypeError('Expected <type \'CcEvent\'> or <type \'Tuple\'>, got ' + str(type(eventOrPeriod)))

        if not isinstance(eventOrPeriod, tuple):
            event = eventOrPeriod
            return (self.startTime < event.startTime and self.endTime != None and (event.endTime == None or self.endTime < event.endTime) and self.endTime >= event.startTime) or (self.startTime > event.startTime and event.endTime != None and self.startTime <= event.endTime and (self.endTime == None or self.endTime > event.endTime))
        else:
            startTime = eventOrPeriod[0]
            endTime = eventOrPeriod[1]
            return (self.startTime < startTime and self.endTime != None and self.endTime < endTime and self.endTime >= startTime) or (self.startTime > startTime and self.startTime <= endTime and self.endTime > endTime)

    def get( self, key ):
        """
        @param key a key of the event's properties
        @return value
        """
        try:
            return self.properties[key]
        except KeyError:
            print "Event does not have property '" + key + "'"
            return None

    def set( self, key, value ):
        """
        @param key a key of the event's properties
        @param value the value for that key
        """

        self.properties[key] = value
