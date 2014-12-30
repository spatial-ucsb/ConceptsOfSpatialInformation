#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TODO: description of module
 
 General docs for UNIT TESTS:
 https://docs.python.org/2/library/unittest.html

"""
__author__ = "Eric Ahlgren"
__copyright__ = "Copyright 2014"
__credits__ = ["Eric Ahlgren"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = ""
__email__ = ""
__date__ = "December 2014"
__status__ = "Development"

import unittest
from utils import _init_log, float_eq
from objects_oo import *
from coreconcepts_oo import CcObject 

log = _init_log("tests")


class TestArcShpObject(unittest.TestCase):
    
    def test_bounds( self ):
        #Get objects from shapefiles
        shapefile1 = "data/objects/Rooftops.shp"
        shapefile2 = "data/objects/ViablePVArea.shp"
        roofObj = ArcShpObject( shapefile1, 0 )
        pvObj = ArcShpObject( shapefile2, 236 )
        #test getBounds on roof object - Poultry Science building
        print "\nTest shapefile objects - getBounds for CalPoly roof"
        roofObj = ArcShpObject ( shapefile1, 0 )
        roofBounds = roofObj.bounds()
        roofBounds = ( round( roofBounds[0],2 ),round( roofBounds[1],2 ),round( roofBounds[2],2 ),round( roofBounds[3],2 ) )
        print "\nBounding box coordinates, UTM Zone 10N, in form (MinX, MaxX, MinY, MaxY):\n",roofBounds,"\n"
        self.assertTupleEqual( roofBounds, ( 710915.55, 710983.25, 3910040.96, 3910095.28 ) )
        
    def test_relation( self ):
        #Get objects from shapefiles
        shapefile1 = "data/objects/Rooftops.shp"
        shapefile2 = "data/objects/ViablePVArea.shp"
        roofObj = ArcShpObject( shapefile1, 0 )
        pvObj = ArcShpObject( shapefile2, 236 )
        #test hasRelation for PV object within roof object
        rel = pvObj.relation( roofObj,'Within' )
        self.assertEqual( rel, True )
          
    def test_property( self ):
        #Get objects from shapefiles
        shapefile1 = "data/objects/Rooftops.shp"
        roofObj = ArcShpObject( shapefile1, 0 )
        #test getProprty for Poultry Science building name
        roofName = roofObj.property( 'name' )
        self.assertEqual( roofName, "Poultry Science" )