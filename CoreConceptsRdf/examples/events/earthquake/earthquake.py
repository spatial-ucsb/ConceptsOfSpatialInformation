# -*- coding: utf-8 -*-
"""
Earthquake Event Class
"""
__author__ = "Marc Tim Thiemann"
__copyright__ = "Copyright 2015"
__credits__ = ["Marc Tim Thiemann"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = ""
__email__ = ""
__date__ = "Febuary 2015"
__status__ = "Development"

import sys
sys.path.insert(1,'../../../../CoreConceptsPy')

from coreconcepts import CcEvent
from rdflib import Graph, BNode, Namespace, RDF, XSD, Literal, URIRef
import os.path

class Earthquake(CcEvent):
    """ This earthquake class models earthquakes. Each earthquake has a latitude, longitude, magnitude, place and a time. """

    def __init__(self, properties):
        self.latitude = properties['latitude']
        self.longitude = properties['longitude']
        self.magnitude = properties['mag']
        self.place = properties['place']
        self.atTime = properties['atTime']

    def toRDF(self, format, filename = None, eqNamespace = None):
        '''
        @param format The output format. Supported formats: ‘xml’, ‘n3’, ‘turtle’, ‘nt’, ‘pretty-xml’, trix’
        @param filename The filename for the output file
        '''

        extension = format
        if format == "xml":
            extension = "rdf"
        elif format == "turtle":
            extension = "ttl"
        elif format == "pretty-xml":
            extension = "xml"

        filenameAndExtension = filename + '.' + extension

        g = Graph()

        if filename is not None and os.path.isfile(filenameAndExtension):
            g.parse(filenameAndExtension, format=format)

        # define and bind namespaces

        #lat, long
        geo = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")
        g.bind('geo', geo)

        # magnitude
        dbpprop = Namespace("http://dbpedia.org/property/")
        g.bind('dbpprop', dbpprop)

        # atPlace, atTime
        lode = Namespace("http://linkedevents.org/ontology/")
        g.bind('lode', lode)

        # earthquake class
        eq = Namespace("http://myearthquakes.com/")
        g.bind('eq', eq)

        earthquake = ""
        if eqNamespace is not None:
            randomId = os.urandom(16).encode('hex')
            earthquake = URIRef(eqNamespace + randomId)
        else:
            earthquake = BNode()

        g.add( (earthquake, RDF.type, eq.Earthquake) )
        g.add( (earthquake, geo.lat, Literal(self.latitude, datatype=XSD.float) ) )
        g.add( (earthquake, geo.long, Literal(self.longitude, datatype=XSD.float) ) )
        g.add( (earthquake, dbpprop.magnitude, Literal(self.magnitude, datatype=XSD.float) ) )
        g.add( (earthquake, lode.atPlace, Literal(self.place) ) )
        g.add( (earthquake, lode.atTime, Literal(self.atTime.isoformat(), datatype=XSD.dateTime) ) )

        if filename is None:
            print g.serialize(format=format)
        else:
            g.serialize(destination = filenameAndExtension, format=format)
