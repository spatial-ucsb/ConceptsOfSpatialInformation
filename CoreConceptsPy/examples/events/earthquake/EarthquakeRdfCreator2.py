# -*- coding: utf-8 -*-
"""
 Abstract: Creates RDF for earthquake objects.
 Gets an Array of Python Earthquake objects and turns them to RDF using RDFlib.
 The RDF can either be outputted or written to a file.

 This class does not inherit from RDFCreator!
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
import json

class EarthquakeRdfCreator2():

    def __init__(self, bindings = None):
        """
        Initialize Graph and setup namespaces
        @param bindings The path to a json configuration file.
        """
        self.g = Graph()

        if bindings is not None:
            self.bindNamespaces(bindings)

    def create(self, earthquakeArr, format, destination = None, eqNamespace = None):
        """
        Create Output for an array of earthquake objects
        @param earthquakeArr An array of earthquake objects
        @param format The output format. Supported formats: ‘xml’, ‘n3’, ‘turtle’, ‘nt’, ‘pretty-xml’, trix’
        @param destination The destination for the output file
        @param eqNamespace The uri for these RDF objects
        """

        for o in earthquakeArr:
            self.add(o, eqNamespace)

        if destination is None:
            print self.g.serialize(format=format)
        else:
            self.g.serialize(destination = destination + '.' + self.getExtension(format), format=format)

    def add(self, earthquake, uri):
        """
        Add RDF for this earthquake to the graph.
        @param earthquake The earthquake object
        @param uri The uri for that earthquake
        """

        randomId = os.urandom(16).encode('hex')
        eq = URIRef(uri + randomId)

        self.g.add( (eq, RDF.type, self.eq.Earthquake) )
        self.g.add( (eq, self.geo.lat, Literal(earthquake.latitude, datatype=XSD.float) ) )
        self.g.add( (eq, self.geo.long, Literal(earthquake.longitude, datatype=XSD.float) ) )
        self.g.add( (eq, self.qudt.vectorMagnitude, Literal(earthquake.magnitude, datatype=XSD.float) ) )
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

    def bindNamespaces(self, bindings):
        """
        Binds namespaces to the graph
        @param bindings The path to a json configuration file. The json file should have an array called "bindings".
        Each object in this array should have an attribute called "prefix" for the prefix and an attribute called "namespace" for the namespace uri.
        """

        json_data = open(bindings).read()
        data = json.loads(json_data)

        for obj in data['bindings']:
            setattr(self, obj['prefix'], Namespace(obj['namespace']))
            self.g.bind(obj['prefix'], getattr(self, obj['prefix']))
