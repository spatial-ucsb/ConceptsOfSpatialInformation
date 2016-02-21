#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Abstract: Turns earthquake RDF objects into earthquake python objects

Reads RDF earthquake objects from a file that contains earthquakes of December 2014 and turns them into Earthquake python objects.
Prints the first 3 Python earthquakes in the list to check if the Earthquake objects are valid.
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

sys.path = [ '.', '../../..' ] + sys.path
from earthquake import *
from EarthquakeRdfReader import *
from EarthquakeRdfReader2 import *

#EarthquakeRdfReader2 does not inherit from RdfReader
"""
rdf = EarthquakeRdfReader2('examples/events/earthquake/bindings.json')
earthquakes = rdf.read('tmp/testEarthquake.rdf', format="xml")
"""

rdf = EarthquakeRdfReader('examples/events/earthquake/bindings.json')
earthquakes = rdf.read('tmp/testEarthquake.rdf', format="xml")

for x in range(0,3):
    print earthquakes[x].latitude
    print earthquakes[x].longitude
    print earthquakes[x].place
    print earthquakes[x].atTime
    print earthquakes[x].magnitude
