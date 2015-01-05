# -*- coding: utf-8 -*-

"""
TODO: description of module
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

from utils import _init_log
from coreconcepts import CcField
import numpy as np
import gdal
from gdalconst import *

log = _init_log("fields")

def getGtiffOffset( gtiff, position ):
    """
    Convert GeoTiff coordinates to matrix offset. Used for getValue GeoTiffField functions.
    @param position - the input geocoordinates
    @return - the i,j pair representing position in the image matrix
    """
    transform = gtiff.GetGeoTransform()
    #Convert geo-coords to image space
    ulx = transform [0]
    uly = transform [3]
    xQuery = position [0]
    yQuery = position [1]
    pixWidth = transform [1]
    pixHeight = transform [5]
    arrx = int((xQuery - ulx)/pixWidth)
    arry = int((yQuery - uly)/pixHeight)
    return arry, arrx

def getTestField():
    testField = GeoTiffField( "data/fields/testField.tif" )
    return testField

def squareMean3( array, centerPixel ):
    """
    Kernel neighborhood function for focal map algebra. Reutrns mean of a 3x3 square array.
    @param array - array from which to retrieve the neighborhood kernel
    @centerPixel - (i,j) corrdinates of center pixel of kernel in the array
    """
    rows = centerPixel[0] - 1
    cols = centerPixel[1] - 1
    neighArray = array[rows:rows + 3, cols:cols + 3]
    return neighArray.mean()

class GeoTiffField(CcField):
    """
    Subclass of Abstract Fields in the GeoTiff format. Based on GDAL.

    Map algebra based on (TODO: specify reference. To clarify what we're doing here, it's important to
    rely on a GIS textbook.
    e.g. Local operations works on individual raster cells, or pixels.
        Focal operations work on cells and their neighbors, whereas global operations work on the entire layer.
        Finally, zonal operations work on areas of cells that share the same value.
    )
    """
    def __init__( self, filepath ):
        self.gField = gdal.Open( filepath, GA_Update )

    def getValue( self, position ):
        """
        Returns the value of a pixel at an input position
        @param position the coordinate pair in gtiff's coordinate system
        @return the raw value of the pixel at position in gtiff
        """
        offset = getGtiffOffset( self.gField, position )
        #Convert image to array
        array = self.gField.ReadAsArray( offset[1],offset[0], 1,1 )
        return array

    def local( self, newGtiffPath, func ):
        """
        Assign a new value to each pixel in gtiff based on func. Return a new GeoTiff at newGtiffPath.
        @param newGtiffPath - file path for the new GeoTiff
        @param func - the local function to be applied to each value in GeoTiff
        @return N/A; write new raster to newGtiffPath
        """
        oldArray = self.gField.ReadAsArray()
        newArray = func(oldArray)
        driver = self.gField.GetDriver()

        newRaster = driver.CreateCopy(newGtiffPath, self.gField)
        outBand = newRaster.GetRasterBand(1)
        outBand.WriteArray(newArray)
        outBand.FlushCache()

    def focal( self, newGtiffPath, kernFunc ):
        """
        Assign a new value to each pixel in gtiff based on focal map algebra. Return a new GeoTiff at newGtiffPath.
        @param newGtiffPath - the filepath of the output GeoTiff
        @param kernFunc - the neighborhood function which returns the kernel array
        @return N/A; write new raster to newGtiffPath
        """

        oldArray = self.gField.ReadAsArray()
        newArray = oldArray.copy()
        rows = oldArray.shape[0]
        cols = oldArray.shape[1]
        for i in range (1, rows-1):
            for j in range (1, cols-1):
                newVal = kernFunc(oldArray,(i,j))
                newArray.itemset((i,j), newVal)
        driver = self.gField.GetDriver()
        newRaster = driver.CreateCopy(newGtiffPath, self.gField)
        outBand = newRaster.GetRasterBand(1)
        outBand.WriteArray(newArray)
        outBand.FlushCache()
