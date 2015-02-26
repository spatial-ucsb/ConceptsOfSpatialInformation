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

import dateutil.parser
from datetime import *
from earthquake import *
from EarthquakeRdfCreator import *
from EarthquakeRdfCreator2 import *
import csv

f = open('../../../../data/events/earthquake-data.csv')
csv_f = csv.reader(f)

earthquakes = []

for row in csv_f:
    dt = dateutil.parser.parse(row[0], fuzzy = True, ignoretz = True)
    properties = {  'latitude': row[1],
                    'longitude': row[2],
                    'mag': row[4],
                    'place': row[13],
                    'atTime': dt}

    earthquakes.append(Earthquake(properties))

earthquakes = earthquakes[1:]

# use initial EarthquakeRdfCreator that does not inherit from RdfCreator
"""
rdf = EarthquakeRdfCreator2('bindings.json')
rdf.create(earthquakes, 'xml', '../../../../CoreConceptsRdf/examples/events/earthquake/test', 'http://myearthquakes.com/earthquakes/')
"""

#use EarthquakeRdfCreator that inherits from RdfCreator
rdf = EarthquakeRdfCreator('bindings.json')

for e in earthquakes:
    earthquakeid = os.urandom(16).encode('hex')
    uri = "http://myearthquakes.com/earthquakes/" + earthquakeid
    rdf.add(uri, e)

rdf.serialize('xml', '../../../../CoreConceptsRdf/examples/events/earthquake/test')
