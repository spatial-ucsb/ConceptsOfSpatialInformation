"""
An implementation of the core concept event for astronomic spaces
:author: Fenja Kollasch, 06/2017
"""

from coreconcepts import CcEvent
from astropy.time import Time


class AstroTime(object):
    """
    A simple wrapper for AstroPy's Time class.
    Accepts any format as Input, but returns it as ISO
    """
    def __init__(self, value, add_value=None, form='iso'):
        self.__time = Time(value, add_value, format=form)

    @property
    def time(self):
        return self.__time.iso

    def __sub__(self, other):
        return AstroTime(self.__time - other.__time, form=other.__time.format)

    def value(self):
        return float(self.__time.jd)


class AstroEvent(CcEvent):

    def __init__(self, identity, participants=None, **props):
        """
        A happening with a fix timestamp that is not always know
        Other components can participate in this event
        :param identity: The identity of this event
        :param participants: The participants mapped to the functions changing them
        :param props: Properties of this event
        """
        self.id = identity
        self.start = props.pop('start', None)
        self.end = props.pop('end', None)
        self.participants = participants

        self.__props = props

    def when(self):
        return self.start

    def within(self):
        return self.end - self.start

    def during(self, event):
        return event.start <= self.start and self.end <= event.end

    def before(self, event):
        return self.end < event.start

    def after(self, event):
        return event.end < self.start

    def overlap(self, event):
        return self.end < event.start or event.end < self.start

    def property(self, prop):
        return self.__props[prop]

    def participant(self, participant):
        for p in self.participants.keys():
            if p == participant:
                return p
        raise EventError("{0} is not participating in this event.".format(participant))

    def status(self, participant, timestamp):
        """
        Returns the status of a participant during this event at a specific time
        :param participant: The participating component
        :param timestamp: The timestamp
        :return: The component with its properties at this time
        """
        try:
            return self.participants[participant](participant, timestamp)
        except KeyError:
            raise EventError("The component {0} is not participating in the event.".format(participant))


class EventError(Exception):
    def __init__(self, message):
        super(EventError, self).__init__(message)
