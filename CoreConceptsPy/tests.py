#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TODO: description of module
 
 General docs for UNIT TESTS:
 https://docs.python.org/2/library/unittest.html

"""
__author__ = ""
__copyright__ = "Copyright 2014"
__credits__ = ["", "Andrea Ballatore"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = ""
__email__ = ""
__date__ = "December 2014"
__status__ = "Development"

import unittest
from utils import _init_log, float_eq
import numpy as np

from coreconcepts import ALocate, AFields
from fields_impl import *
# TODO: avoid 'import *', only import used methods/classes
from objects_impl import *
from coreconcepts_oo import CcField,CcObject,CcNetwork,CcEvent
import random 

log = _init_log("tests")

class CoreConceptsTest(unittest.TestCase):
    """ Unit tests for module CoreConceptsPy """
    
    def testExamples(self):
        """ Examples of unit tests """
        self.assertEqual(1+3,4)
        self.assertNotEqual(5,1)
        self.assertTrue(float_eq(4.2,4.2))
        self.assertFalse(float_eq(4.2,4.200001))
        
    def testLocate(self):
        pass
        """
        figureA = Entity()
        figureB = Entity()
        groundA = Entity()
        groundB = Entity()
        
        self.assertTrue( ExLoc.isAt( figureA, groundA ) )
        self.assertFalse( ExLoc.isPart( figureA, groundA ) )
        """
        
    def testFields(self):
        
        # basic python list of tuples
        basicField = [((0,0),"ul"),((0,1),"ur"),((1,0),"ll"),((1,1),"lr")]
        print basicField
        
        # arrays based on Numpy
        numpyFieldChar = np.array([ ['ul', 'ur'], ['ll', 'lr'] ])
        print "numpyFieldChar\n",numpyFieldChar
        
        # array of floating points
        numpyFieldFloat = np.array([ [.5, .1], [.45, .2] ])
        print "numpyFieldFloat\n",numpyFieldFloat
        
        print "value for 0,0 =", ArrFields.getValue( numpyFieldFloat, [0, 0] )
        print "value for 1,1 =", ArrFields.getValue( numpyFieldFloat, [1, 1] )
        
        #print ArrField.setValue( numpyArr, [0, 1], "new value" )
        ArrFields.setValue( numpyFieldFloat, [0, 1], .2 )
        print "numpyFieldFloat after change\n",numpyFieldFloat
        #print ArrField.getValue( basicArr, [1, 1] )
    
    def testGeoTiffFields(self):
        """ Import DEM of CalPoly campus and test functions on upper left coords"""
        
        print "\nTest geotiff fields - getValue on CalPoly DEM\n"
        gtiffPath = "data/fields/testField.tif"
        dem = gdal.Open(gtiffPath, GA_Update) #GA_Update gives write access
        ulCoords =(711743.5, 3910110.5) #Coordinates are UTM Zone 10N
        #test getValue for upper left coords
        ulVal = GeoTiffFields.getValue(dem, ulCoords)
        print "value of upper left pixel =", round(ulVal,2)
        self.assertTrue(float_eq(ulVal, 117.36))
        
        #test setValue for upper left coords
        print "\nTest geotiff fields - setValue on CalPoly DEM\n"
        newVal = random.randrange(1,100)
        GeoTiffFields.setValue(dem, ulCoords, newVal)
        GeoTiffFields.getValue(dem, ulCoords)
        testVal = GeoTiffFields.getValue(dem, ulCoords)
        print "\nnew value of upper left pixel =", round(testVal,2)
        self.assertTrue(float_eq(testVal, newVal))

        #reset ulCoords to original value of 117.2
        print "\nresetting value to 117.36\n"
        GeoTiffFields.setValue(dem, ulCoords, 117.36)
        self.assertTrue(float_eq(GeoTiffFields.getValue(dem, ulCoords), 117.36))
    
    def testFieldsMapAlgebra(self):
        """ Import DEM of CalPoly campus and test Map Albegra functions"""
        
        print "Test Map Algebra local function"
        gtiffPath = "data/fields/testField.tif"
        newGtiffPath = "data/fields/testLocal.tif"
        dem = gdal.Open(gtiffPath, GA_Update) #GA_Update gives write access
        ulCoords =(711743.5, 3910110.5) 
        def localFunc(x):
            return x/2
        GeoTiffFields.local(dem,newGtiffPath,localFunc)
        testDEM = gdal.Open(newGtiffPath, GA_Update)
        oldVal = GeoTiffFields.getValue(dem, ulCoords)
        testVal = GeoTiffFields.getValue(testDEM, ulCoords)
        self.assertTrue(float_eq(oldVal, testVal*2))
       
        
        print "Test Map Algebra focal function"
        newGtiffPath = "data/fields/testFocal.tif"
        def focalFunc(x):
            return x.mean()
        GeoTiffFields.focal(dem, newGtiffPath, squareNeigh, 3, focalFunc)
        testCoords = (711750.8, 3910105.1)
        offset = getGtiffOffset (dem, testCoords)
        print "Offset to center pixel (i,j): ", offset
        array = dem.ReadAsArray()
        testNeighArray = squareNeigh(array, 3, offset)
        print "focalCoord start value: ", GeoTiffFields.getValue(dem, testCoords)
        print "testNeighArray: ", testNeighArray
        print "testNeighArray mean: ", testNeighArray.mean()
        testDEM = gdal.Open(newGtiffPath, GA_Update)
        testVal = GeoTiffFields.getValue(testDEM,testCoords)
        print "testVal: ", testVal
        
        self.assertTrue(float_eq(testVal, testNeighArray.mean())) #Confirm new value is mean of focal window

        
    def getTestField(self):
        # TODO: return test field. Re-use this to avoid redundancy. 
        return None
    
    def testArcShpObjects(self):
        """ Import 2 ArcMap shapefiles and test core concept functions """

        #Get objects from shapefiles
        shapefile1 = "data/objects/Rooftops.shp"
        shapefile2 = "data/objects/ViablePVArea.shp"
        layer_src1 = ogr.Open(shapefile1)
        layer_src2 = ogr.Open(shapefile2)
        lyr1 = layer_src1.GetLayer(0)
        lyr2 = layer_src2.GetLayer(0)
        roofObj = lyr1.GetFeature(0)
        pvObj = lyr2.GetFeature(236)

        #test getBounds on roof object - Poultry Science building
        print "\nTest shapefile objects - getBounds for CalPoly roof"
        roofBounds = ArcShpObjects.getBounds(roofObj)
        roofBounds = (round(roofBounds[0],2),round(roofBounds[1],2),round(roofBounds[2],2),round(roofBounds[3],2))
        print "\nBounding box coordinates, UTM Zone 10N, in form (MinX, MaxX, MinY, MaxY):\n",roofBounds,"\n"
        #TODO: never compare floats directly. use float_eq in utils
        self.assertTupleEqual(roofBounds, (710915.55, 710983.25, 3910040.96, 3910095.28))
        
        #test hasRelation for PV object within roof object
        rel = ArcShpObjects.hasRelation(pvObj,roofObj,'Within')
        self.assertEqual(rel,True)
        
        #test getProprty for Poultry Science building name
        roofName = ArcShpObjects.getProperty(roofObj, 'name')
        self.assertEqual(roofName,"Poultry Science")
    
    def testFunctionCall(self):
        """ For @Eric: Pass a function as a parameter """
        
        def myFunction(x):
            return x * 2 + 4
        
        def myFunction2(x):
            return x - 5
        
        def funcCaller( a, func ):
            # call func on parameter a
            # "func" is a function can that can be called normally
            return func(a)
        
        # call funcCaller passing myFunction and myFunction2 as parameters, checking outputs
        self.assertEquals( funcCaller( 3, myFunction ), 10 )
        self.assertEquals( funcCaller( 3, myFunction2 ), -2 )
        self.assertEquals( funcCaller( 5, myFunction ), 14 )
        self.assertEquals( funcCaller( 5, myFunction2 ), 0 )
    
    def testCoreConceptsOo(self):
        field = CcField()
        obj = CcObject()
        net = CcNetwork()
        event = CcEvent()
    
if __name__ == '__main__':
    unittest.main()