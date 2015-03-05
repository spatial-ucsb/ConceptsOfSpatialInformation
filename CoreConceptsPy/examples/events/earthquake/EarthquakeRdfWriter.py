# -*- coding: utf-8 -*-
"""
 Abstract: Creates RDF for earthquake objects.
 Gets an Array of Python Earthquake objects and turns them to RDF using RDFlib.
 The RDF can either be outputted or written to a file.

 This class inherits from RdfWriter!
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
sys.path.insert(1,'../../../../CoreConceptsPy')
from RdfWriter import *

class EarthquakeRdfWriter(RdfWriter):

    def add(self, uri, earthquake):
        """
        Add RDF for this earthquake to the graph.
        """
        eq = URIRef(uri)

        self.g.add( (eq, RDF.type, self.eq.Earthquake) )
        self.g.add( (eq, self.geo.lat, Literal(earthquake.latitude, datatype=XSD.float) ) )
        self.g.add( (eq, self.geo.long, Literal(earthquake.longitude, datatype=XSD.float) ) )
        self.g.add( (eq, self.qudt.vectorMagnitude, Literal(earthquake.magnitude, datatype=XSD.float) ) )
        self.g.add( (eq, self.lode.atPlace, Literal(earthquake.place) ) )
        self.g.add( (eq, self.lode.atTime, Literal(earthquake.atTime.isoformat(), datatype=XSD.dateTime) ) )
