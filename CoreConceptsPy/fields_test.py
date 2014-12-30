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
import numpy as np
from fields_oo import *
from coreconcepts_oo import CcField
import random 

log = _init_log("tests")


class TestGeoTiffField(unittest.TestCase):
    
    def test_getValue( self ):
        """ Import DEM of CalPoly campus and test getValue method on upper left coords"""
        
        print "\nTest geotiff fields - getValue on CalPoly DEM\n"
        dem = getTestField()
        ulCoords = ( 711743.5, 3910110.5 ) #Coordinates are UTM Zone 10N
        #test getValue for upper left coords
        ulVal = dem.getValue( ulCoords )
        self.assertTrue( float_eq( ulVal, 117.36 ) )
    
    def test_local( self ):
        """ Import DEM of CalPoly campus and test Map Albegra local function"""
        
        print "\nTest Map Algebra local function\n"
        dem = getTestField()
        newGtiffPath = "data/fields/testLocal.tif"
        ulCoords =( 711743.5, 3910110.5 ) 
        def localFunc( x ):
            return x/2
        dem.local( newGtiffPath, localFunc )
        testDem = GeoTiffField( newGtiffPath )
        oldVal = dem.getValue( ulCoords )
        testVal = testDem.getValue( ulCoords )
        self.assertTrue( float_eq( oldVal, testVal*2 ) )
       
    def test_focal( self ):
        """ Import DEM of CalPoly campus and test Map Albegra focal function"""   
        print "Test Map Algebra focal function"
        dem = getTestField()
        newGtiffPath = "data/fields/testFocal.tif"
        dem.focal( newGtiffPath, squareMean3 )
        testCoords = ( 711750.8, 3910105.1 )
        offset = getGtiffOffset ( dem.gField, testCoords )
        array = gdal.Open( "data/fields/testField.tif" ).ReadAsArray()
        testNeighArray = squareMean3( array, offset )
        testDem = GeoTiffField( newGtiffPath )
        testVal = testDem.getValue( testCoords )
        self.assertTrue( float_eq( testVal, testNeighArray ) ) #Confirm new value is mean of focal window   
    
if __name__ == '__main__':
    unittest.main()