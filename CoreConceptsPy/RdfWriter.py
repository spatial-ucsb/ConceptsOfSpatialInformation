# -*- coding: utf-8 -*-
"""
 Abstract: An abstract class to turn an array of python objects into RDF.
 Gets an Array of python objects and turns them to RDF using RDFlib.
 The RDF can either be outputted or written to a file.
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

from rdflib import *
import json

class RdfWriter(object):

    def __init__(self, bindings = None):
        """
        Initialize Graph and setup namespaces
        @param bindings The path to a json configuration file.
        """
        self.g = Graph()

        if bindings is not None:
            self.bindNamespaces(bindings)

    def add(self, uri, obj):
        """
        Add a single object to the graph
        @param uri The uri of that object
        @param obj The object that should be added
        """

        raise NotImplementedError("add")

    def serialize(self, format = 'xml', destination = None):
        """
        Serializes the graph into the specified RDF format and outputs it or writes it to file
        @param format The output format. Supported formats: ‘xml’, ‘n3’, ‘turtle’, ‘nt’, ‘pretty-xml’, trix’
        @param destination The destination of the output file
        """
        if destination is None:
            print self.g.serialize(format=format)
        else:
            self.g.serialize(destination = destination + '.' + self.getExtension(format), format=format)

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
