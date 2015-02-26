# -*- coding: utf-8 -*-
"""
 Abstract: Turns RDF into python objects.
 Using RDFlib it parses a RDF file and turns each RDF object in that file to a python object.
 The python objects will be returned as an array.
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

class RdfReader(object):

    def __init__(self, bindings = None):
        """
        Initialize Graph and setup namespaces
        @param bindings The path to a json configuration file.
        """
        self.g = Graph()

        self.setNamespaces(bindings)

    def read(self, destination, format):
        """
        Parse RDF file into rdflib graph
        @param destination The destination of the file that contains the RDF data
        @param format The input format. Supported formats: ‘xml’, ‘n3’, ‘turtle’, ‘nt’, ‘pretty-xml’, trix’
        """

        self.g.parse(destination, format=format)

        return self.getObjs()

    def getObjs(self):
        """
        Turns RDF to python objects
        @return An array of python objects
        """

        raise NotImplementedError('getObjs')

    def setNamespaces(self, bindings):
        """
        Sets up the namespaces
        @param bindings The path to a json configuration file. The json file should have an array called "bindings".
        Each object in this array should have an attribute called "prefix" for the prefix and an attribute called "namespace" for the namespace uri.
        """

        json_data = open(bindings).read()
        data = json.loads(json_data)

        for obj in data['bindings']:
            setattr(self, obj['prefix'], Namespace(obj['namespace']))
