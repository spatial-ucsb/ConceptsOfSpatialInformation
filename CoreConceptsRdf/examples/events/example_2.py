#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Example 2:
Earthquake events

Use Cases:
- get all earthquakes which origin is 100 m or deeper
- get all earthquakes from 12/01/2014 00:00:00 - 12/6/2014 23:59:59
- get all earthquakes in Alaska

Provided data:
CSV file with all global earthquake events for December 2014.
The fields for each earthquake are:
time,latitude,longitude,depth,mag,magType,nst,gap,dmin,rms,net,id,updated,place,type

Output data format:
RDF
"""

__author__ = "Marc Tim Thiemann"
__copyright__ = "Copyright 2015"
__credits__ = ["Marc Tim Thiemann"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = ""
__email__ = ""
__date__ = "February 2015"
__status__ = "Development"

import sys
sys.path.insert(1,'../../../CoreConceptsPy')
sys.path.insert(1, '../../../CoreConceptsRDF')
print sys.path
from events import *
import dateutil.parser
from datetime import *
import csv
from RDFCreator import *

f = open('../../../data/events/earthquake-data.csv')
csv_f = csv.reader(f)

events = []

for row in csv_f:
    properties = {  'latitude': row[1],
                    'longitude': row[2],
                    'depth': row[3],
                    'mag': row[4],
                    'magType': row[5],
                    'nst': row[6],
                    'gap': row[7],
                    'dmin': row[8],
                    'rms': row[9],
                    'net': row[10],
                    'id': row[11],
                    'updated': row[12],
                    'place': row[13],
                    'type': row[14]}
    dt = dateutil.parser.parse(row[0], fuzzy = True, ignoretz = True)

    events.append(PyEvent((dt, dt), properties))


'''
print 'Get all locations of earthquakes with a magnitude of 4 or higher during December 2014'

locations = []
for e in events:
    if(e.get('mag') >= 4):
        locations.append((e.get('latitude'), e.get('longitude')))

'''

print 'Get all earthquakes from 12/01/2014 00:00:00 - 12/6/2014 23:59:59'

earthquakesFirstSevenDays = []
for e in events:
    if(e.during((datetime(2014, 12, 01, 0, 0, 0), datetime(2014, 12, 6, 23, 59, 59)))):
        earthquakesFirstSevenDays.append(e)

rdf = RDFCreator()
rdf.create(earthquakesFirstSevenDays, 'xml', 'test')

'''

print 'Get all earthquakes in Alaska during December 2014'

earthquakesInAlaska = []
for e in events:
    if "Alaska" in e.get('place'):
        earthquakesInAlaska.append(e)



print 'Get all earthquakes which origin is 100 m or deeper'

deepEarthQuakes = []
for e in events:
    depth = 0.0
    try:
        depth = float(e.get('depth'))
    except:
        print 'Not a Number!'

    if(depth >= 100):
        deepEarthQuakes.append(e) '''
