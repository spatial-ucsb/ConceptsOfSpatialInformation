# -*- coding: utf-8 -*-
"""
 Abstract: Creates RDF for core concept objects.
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


from rdflib import Graph, BNode, Namespace, RDF, XSD, Literal, URIRef
import os.path

class RDFCreator():

    def __init__(self):
        self.g = Graph()

        #lat, long
        self.geo = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")
        self.g.bind('geo', self.geo)

        # magnitude
        self.dbpprop = Namespace("http://dbpedia.org/property/")
        self.g.bind('dbpprop', self.dbpprop)

        # atPlace, atTime
        self.lode = Namespace("http://linkedevents.org/ontology/")
        self.g.bind('lode', self.lode)

        # earthquake class
        self.eq = Namespace("http://myearthquakes.com/")
        self.g.bind('eq', self.eq)

    def create(self, ccobjects, format, filename = None, eqNamespace = None):
        """
        Create Output for an array of objects
        @param ccobjects An array of core concept objects
        @param format The output format. Supported formats: ‘xml’, ‘n3’, ‘turtle’, ‘nt’, ‘pretty-xml’, trix’
        @param filename The filename for the output file
        """

        for o in ccobjects:
            self.add(o, eqNamespace)

        if filename is None:
            print self.g.serialize(format=format)
        else:
            self.g.serialize(destination = filename + '.' + self.getExtension(format), format=format)

    def add(self, earthquake, uri = None):
        """
        Add RDF for this event to the current graph.
        """

        eq = ""
        if uri is not None:
            randomId = os.urandom(16).encode('hex')
            eq = URIRef(uri + randomId)
        else:
            eq = BNode()

        self.g.add( (eq, RDF.type, self.eq.Earthquake) )
        self.g.add( (eq, self.geo.lat, Literal(earthquake.latitude, datatype=XSD.float) ) )
        self.g.add( (eq, self.geo.long, Literal(earthquake.longitude, datatype=XSD.float) ) )
        self.g.add( (eq, self.dbpprop.magnitude, Literal(earthquake.magnitude, datatype=XSD.float) ) )
        self.g.add( (eq, self.lode.atPlace, Literal(earthquake.place) ) )
        self.g.add( (eq, self.lode.atTime, Literal(earthquake.atTime.isoformat(), datatype=XSD.dateTime) ) )

    def getExtension(self, format):
        """
        Get the file extension for a given format
        @param format The format
        """
        if format == "xml":
            return "rdf"
        elif format == "turtle":
            return "ttl"
        elif format == "pretty-xml":
            return "xml"
        else:
            return format
