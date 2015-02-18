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

import sys
sys.path.insert(1,'../CoreConceptsPy')
from coreconcepts import *
from rdflib import Graph, BNode, Namespace, RDF, XSD, Literal

class RDFCreator():

    def __init__(self):
        self.g = Graph()

        self.namespace = "http://www.core-concepts.com/cc/"
        self.cc = Namespace(self.namespace)
        self.g.bind('cc', self.namespace)

    def create(self, ccobjects, format, filename = None):
        """
        Create Output for an array of objects
        @param ccobjects An array of core concept objects
        @param format The output format. Supported formats: ‘xml’, ‘n3’, ‘turtle’, ‘nt’, ‘pretty-xml’, trix’
        @param filename The filename for the output file
        """

        for o in ccobjects:
            self.add(o)

        if filename is None:
            print self.g.serialize(format=format)
        else:
            self.g.serialize(destination = filename + '.' + self.getExtension(format), format=format)

    def add(self, ccobject):
        """
        Determine the class of the given object and call the corresponding method.
        """
        if isinstance(ccobject, CcEvent):
            self.addEvent(ccobject)
        elif isinstance(ccobject, CcNetwork):
            self.addNetwork(ccobject)
        elif isinstance(ccobject, CcObject):
            self.addObject(ccobject)
        elif isinstance(ccobject, CcField):
            self.addField(ccobject)
        elif isinstance(ccobject, CcLocation):
            self.addLocation(ccobject)

    def addEvent(self, event):
        """
        Add RDF for this event to the current graph.
        """

        ev = BNode()
        self.g.add( (ev, RDF.type, self.cc.Event) )
        self.g.add( (ev, self.cc.startTime, Literal(event.startTime.isoformat(), datatype=XSD.dateTime) ) )
        if event.endTime is not None:
            self.g.add ( (ev, self.cc.endTime, Literal(event.endTime.isoformat(), datatype=XSD.dateTime) ) )

        # TODO: check the graph and setup temporal relations for this event and update temporal relations for other events

        for k, v in event.properties.iteritems():

            # add attribute to graph
            attr = BNode()
            self.g.add( (attr, RDF.type, self.cc.Attribute) )
            self.g.add( (attr, self.cc.hasKey, Literal(k) ) )
            self.g.add( (attr, self.cc.hasValue, Literal(v) ) )

            # assign attribute to event
            self.g.add( (ev, self.cc.hasAttribute, attr) )

    def addNetwork(self, network):
        """
        Add RDF for this network to the current graph.
        """

    def addObject(self, object):
        """
        Add RDF for this object to the current graph.
        """

    def addField(self, field):
        """
        Add RDF for this field to the current graph.
        """

    def addLocation(self, location):
        """
        Add RDF for this location to the current graph.
        """

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
