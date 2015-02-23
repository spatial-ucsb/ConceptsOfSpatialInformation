# -*- coding: utf-8 -*-
"""
 Abstract: Turns earthquake objects from RDF into python objects.
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

class RDFReader():

    def __init__(self):
        self.g = Graph()

        self.geo = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")
        self.dbpprop = Namespace("http://dbpedia.org/property/")
        self.lode = Namespace("http://linkedevents.org/ontology/")
        self.eq = Namespace("http://myearthquakes.com/")

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
            'mag': self.g.value(subject, self.dbpprop.magnitude),
        }

        return Earthquake(properties)
