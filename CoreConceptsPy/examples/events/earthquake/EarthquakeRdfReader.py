# -*- coding: utf-8 -*-
"""
 Abstract: Turns earthquake objects from RDF into python objects.
 Using RDFlib it parses a RDF file and turns each Earthquake RDF object in that file to a Python Earthquake objects.
 The Python Earthquake objects will be returned as an array.
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

from rdflib import Graph, Namespace, RDF
from earthquake import *
import json

class EarthquakeRdfReader():

    def __init__(self, bindings = None):
        self.g = Graph()

        self.setNamespaces(bindings)

    def read(self, destination, format):
        """
        Read RDF file and turn it into core concept objects
        @param destination The destination of the file that contains the RDF data
        @param format The input format. Supported formats: ‘xml’, ‘n3’, ‘turtle’, ‘nt’, ‘pretty-xml’, trix’
        """

        self.g.parse(destination, format=format)

        earthquakes = []

        for subject, predicate, obj in self.g.triples( (None, RDF.type, self.eq.Earthquake) ):
            earthquakes.append(self.parse(subject))

        return earthquakes

    def parse(self, subject):
        """
        Determine the class of the given object and call the corresponding method.
        """

        properties = {
            'latitude': self.g.value(subject, self.geo.lat),
            'longitude': self.g.value(subject, self.geo.long),
            'place': self.g.value(subject, self.lode.atPlace),
            'atTime': self.g.value(subject, self.lode.atTime),
            'mag': self.g.value(subject, self.qudt.vectorMagnitude),
        }

        return Earthquake(properties)

    def setNamespaces(self, bindings):
        json_data = open(bindings).read()
        data = json.loads(json_data)

        for obj in data['bindings']:
            setattr(self, obj['prefix'], Namespace(obj['namespace']))
