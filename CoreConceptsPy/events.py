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

        if period[1] is not None:
            assert period[1] >= period[0]

        self.startTime = period[0]
        self.endTime = period[1]

        assert properties

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

    def during( self, compareTo, compareAll = False ):
        """
        Check if an event is during
        - another event
        - another time period
        - any event or time period in a list
        - all events or time periods in a list
        @param compareTo an event, a time period (tuple) or a list of events and/or time periods (tuples)
        @param compareAll False: If a list is passed in the compareTo paramater, the method checks if the event is at least during one element in that list.
                          True: If a list is passed in the compareTo parameter, the method checks if the event is during all elements in that list.
        @return boolean
        """

        if isinstance(compareTo, CcEvent):
            event = compareTo
            return self.startTime >= event.startTime and (event.endTime == None or (self.endTime != None and self.endTime <= event.endTime))
        elif isinstance(compareTo, list):
            return self.compare(compareTo, compareAll)
        else:
            assert compareTo[1] >= compareTo[0]
            return self.startTime >= compareTo[0] and (self.endTime != None and self.endTime <= compareTo[1])


    def before( self, compareTo, compareAll = False ):
        """
        Check if an event is before
        - another event
        - another datetime
        - any event or datetime in a list
        - all events or time periods in a list
        @param compareTo an event, a datetime or a list of events and/or datetimes
        @param compareAll False: If a list is passed in the compareTo paramater, the method checks if the event is at least before one element in that list.
                          True: If a list is passed in the compareTo parameter, the method checks if the event is before all elements in that list.
        @return Boolean
        """

        if isinstance(compareTo, datetime.datetime):
            return self.endTime != None and self.endTime < compareTo
        elif isinstance(compareTo, CcEvent):
            return self.endTime != None and self.endTime < compareTo.startTime
        else:
            return self.compare(compareTo, compareAll)

    def after( self, eventOrDatetime ):
        """
        @param eventOrDatetime an event or a datetime object
        @return Boolean
        """

        if isinstance(eventOrDatetime, datetime.datetime):
            return self.startTime > eventOrDatetime
        else:
            return eventOrDatetime.endTime != None and self.startTime > eventOrDatetime.endTime

    def overlap( self, eventOrPeriod ):
        """
        @param eventOrPeriod an event or a time period
        @return Boolean
        """

        if not isinstance(eventOrPeriod, tuple):
            event = eventOrPeriod
            return (self.startTime < event.startTime and self.endTime != None and (event.endTime == None or self.endTime < event.endTime) and self.endTime >= event.startTime) or (self.startTime > event.startTime and event.endTime != None and self.startTime <= event.endTime and (self.endTime == None or self.endTime > event.endTime))
        else:
            startTime = eventOrPeriod[0]
            endTime = eventOrPeriod[1]
            assert endTime >= startTime
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

    def compare(self, comparisonList, compareAll):
        """
        Performs the comparison, if a list of tuples/events is passed to a time-related function (before, after, during, overlap).
        The time-related function passes the list of tuples/events and the compareAll value to this function.
        @param comparisonList A list of events, time periods (tuples) and/or datetimes
        @param compareAll Determines if at least one element in the list fulfills the time relation or all elements in the list have to fulfill the time relation
        """

        methodToCall = getattr(self, inspect.stack()[1][3])

        for el in comparisonList:
            result = methodToCall(el)
            if not compareAll:
                if result:
                    return True

            if compareAll:
                if not result:
                    return False
        return result

    @staticmethod
    def intersect(list1, list2):
        """
        @param list1 List of events
        @param list2 List of events
        """
        for l in list1:
            for m in list2:
                isIntersecting = (l.startTime <= m.startTime < l.endTime) or (m.startTime <= l.startTime < m.endTime)
                if isIntersecting:
                    return True
        return False


