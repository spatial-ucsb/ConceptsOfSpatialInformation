# -*- coding: utf-8 -*-
"""
 Abstract: Turns earthquake objects from RDF into python objects.
 Using RDFlib it parses a RDF file and turns each Earthquake RDF object in that file to a Python Earthquake objects.
 The Python Earthquake objects will be returned as an array.

 This class inherits from RdfReader!
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

from earthquake import *
from RdfReader import *

class EarthquakeRdfReader(RdfReader):

    def getObjs(self):
        """
        Turns RDF to earthquake objects
        @return An array of earthquake objects
        """

        earthquakes = []

        for subject, predicate, obj in self.g.triples( (None, RDF.type, self.eq.Earthquake) ):
            properties = {
                'latitude': self.g.value(subject, self.geo.lat),
                'longitude': self.g.value(subject, self.geo.long),
                'place': self.g.value(subject, self.lode.atPlace),
                'atTime': self.g.value(subject, self.lode.atTime),
                'mag': self.g.value(subject, self.qudt.vectorMagnitude)
            }

            earthquakes.append(Earthquake(properties))

        return earthquakes
