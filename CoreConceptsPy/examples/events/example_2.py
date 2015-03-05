#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Example 2:
US weather data from 1 January 2015

Use Cases:
- get all weather events before 12am
- when did it snow on 1 January?
- get all weather events after 6 pm


Provided data:
text file. each row includes: datetime, latitude, longitude, weather type
"""

__author__ = "Marc Tim Thiemann"
__copyright__ = "Copyright 2014"
__credits__ = ["Marc Tim Thiemann"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = ""
__email__ = ""
__date__ = "January 2015"
__status__ = "Development"

import sys

sys.path = [ '.', '../..' ] + sys.path
from utils import _init_log
from events import *
import dateutil.parser
from datetime import *

log = _init_log("example-2")

file = open('../../../data/events/weather_data.txt', 'r')

events = []

for line in file:
    fields = line.split(' ')

    properties = {
        'number': fields[0][:-1],
        'latitude': fields[3][:-1],
        'longitude': fields[4],
        'type': ' '.join(fields[5:len(fields)])
    }

    dt = dateutil.parser.parse(fields[1] + ' ' + fields[2], fuzzy = True, ignoretz = True)

    events.append(PyEvent((dt, dt), properties))


print 'Get all weather events before 12am'

forenoonEvents = []

for e in events:
    if e.before(datetime(2015, 1, 1, 12, 0, 0)):
        forenoonEvents.append(e)


print 'Get all weather events after 6pm'

eveningEvents = []

for e in events:
    if e.after(datetime(2015, 1, 1, 18, 0, 0)):
        eveningEvents.append(e)


print 'When and where did it snow on 1 January 2015?'

snowEvents = []

for e in events:
    if 'Snow' in e.get('type'):
        snowEvents.append(e)

for e in snowEvents:
    print 'Time: ' + str(e.when()) + ', Location: ' + e.get('latitude') +', ' + e.get('longitude')
