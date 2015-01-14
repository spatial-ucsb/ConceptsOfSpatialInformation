#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO: don't use print (use log instead)

"""
TODO: description of module
"""

__author__ = "Eric Ahlgren"
__copyright__ = "Copyright 2014"
__credits__ = ["Eric Ahlgren", "Andrea Ballatore"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = ""
__email__ = ""
__date__ = "December 2014"
__status__ = "Development"

import sys
import unittest
import numpy as np
import random

sys.path = [ '.', '..' ] + sys.path
from utils import _init_log, float_eq
from fields import *

log = _init_log("fields_test")

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
        newGtiffPath = "../data/fields/testLocal.tif"
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
        newGtiffPath = "../data/fields/testFocal.tif"
        dem.focal( newGtiffPath, squareMean3 )
        testCoords = ( 711750.8, 3910105.1 )
        offset = getGtiffOffset ( dem.gField, testCoords )
        array = gdal.Open( "../data/fields/testField.tif" ).ReadAsArray()
        testNeighArray = squareMean3( array, offset )
        testNeighArray = np.round(testNeighArray, 3)
        testDem = GeoTiffField( newGtiffPath )
        testVal = testDem.getValue( testCoords )
        self.assertTrue( float_eq( testVal, testNeighArray ) ) #Confirm new value is mean of focal window
        
    def test_zonal( self ):
        """
        Import DEM of CalPoly campus and test Map Algebra zonal function.
        Returns mean zonal values based on zone layer "zone.tif," which contains
        2 zones derived from the 50x50 CalPolyDEM test field. A value of 0 represents elevation below 118m and
        a value of 1 represents elevation greater than or equal to 118 m (see README.md).
        
        Zonal mean values are calculated and written to "testZonal.tif," then compared with values derived from
        ArcMap (contained in "zonaltable").
        """
        
        newGtiffPath = "../data/fields/testZonal.tif"
        dem = getTestField()
        dem.zonal( newGtiffPath, meanZonalFunc )
        
        zonePath = "../data/fields/zone.tif"
        zoneRast = GeoTiffField(zonePath)
        newRast = GeoTiffField(newGtiffPath)
        testCoord1 = ( 711750.8, 3910105.1 )
        zoneVal = zoneRast.getValue(testCoord1)
        newVal = newRast.getValue(testCoord1)
        self.assertTrue(zoneVal == 0 and newVal == 116.836)
        
        testCoord2 = ( 711748, 3910085 )
        zoneVal = zoneRast.getValue(testCoord2)
        newVal = newRast.getValue(testCoord2)
        self.assertTrue(zoneVal == 1 and newVal == 120.557)
    
if __name__ == '__main__':
    unittest.main()
