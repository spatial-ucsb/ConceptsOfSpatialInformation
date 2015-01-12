#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Example 2:
Earthquake events

Use Cases:
- get the locations of all earthquakes with a magnitude of 4 or higher
- get all earthquakes which origin is ... m or deeper
- get all earthquakes from 12/01/2014 - 12/7/2014

Provided data:
CSV file with all global earthquake events for December 2014.
The fields for each earthquake are:
time,latitude,longitude,depth,mag,magType,nst,gap,dmin,rms,net,id,updated,place,type
"""

__author__ = "Marc Tim Thiemann"
__copyright__ = "Copyright 2014"
__credits__ = ["Marc Tim Thiemann"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = ""
__email__ = ""
__date__ = "December 2014"
__status__ = "Development"

import sys

sys.path = [ '.', '../..' ] + sys.path
from utils import _init_log
from events import *
import dateutil.parser
from datetime import *

log = _init_log("example-2")

p = PyEvent(datetime(2015, 1, 7, 10, 48, 15), datetime(2015, 1, 7, 10, 48, 15))

'''
Read CSV
- create object for each line
    - spatial properties: longitude, latitude, depth
    - thematic properties: magnitude, magnitudeType, nst, gap, dmin, rms, net, id, updated, place, type
- create event for each line and assign corresponding earthquake object as participant
'''
