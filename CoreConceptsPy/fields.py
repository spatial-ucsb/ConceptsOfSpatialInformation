# -*- coding: utf-8 -*-

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

import numpy as np
import numpy.ma as ma
import gdal
from gdalconst import *

from utils import _init_log
from coreconcepts import CcField

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
    testField = GeoTiffField( "../data/fields/testField.tif" )
    return testField

def squareMean3( array, centerPixel ):
    """
    Kernel neighborhood function for focal map algebra. Reutrns mean of a 3x3 square array.
    @param array - array from which to retrieve the neighborhood kernel
    @param centerPixel - (i,j) corrdinates of center pixel of kernel in the array
    @return - mean of 3x3 square neighborhood around centerPixel
    """
    rows = centerPixel[0] - 1
    cols = centerPixel[1] - 1
    neighArray = array[rows:rows + 3, cols:cols + 3]
    return neighArray.mean()

def meanZonalFunc( array, position ):
    """
    Example zonal function. Returns mean zonal values based on zone layer "zone.tif," which contains
    2 zones derived from the 50x50 CalPolyDEM test field. A value of 0 represents elevation below 118m and
    a value of 1 represents elevation greater than or equal to 118 m (see README.md).
    @param array - array on which to perform zonal operation
    @param position - (i,j) coordinates for zonal operation (retrieve zonal geometry and write new value)
    @return - mean value of masked input array derived from zonal geometry of "zone.tif" at input position
    """
    zoneRast = GeoTiffField("../data/fields/zone.tif")
    zoneArr = zoneRast.gField.ReadAsArray()
    band = zoneRast.gField.GetRasterBand(1)
    ndVal = band.GetNoDataValue()
    rows = zoneArr.shape[0]
    cols = zoneArr.shape[1]
    maskArray = zoneRast.zone( (position[0], position[1]) )
    mask = ma.getmask(maskArray)
    newMaskArr = ma.masked_array(array, mask)
    meanVal = newMaskArr.mean()
    return meanVal
    

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
        @param position the coordinate pair in self's coordinate system
        @return the raw value of the pixel at input position in self
        """
        offset = getGtiffOffset( self.gField, position )
        #Convert image to array
        array = self.gField.ReadAsArray( offset[1],offset[0], 1,1 )
        return array
    
    def zone( self, position ):
        """
        Return a masked array representing the zone for the input position
        @param position - i,j coordinates from which to derive zone
        @return - NumPy masked array representing the geometry of the zone for pixel at input position
        """
        array = self.gField.ReadAsArray()
        val = array[position[0], position[1]]
        maskArray = ma.masked_not_equal( array, val )
        return maskArray

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
        newArray = np.around(newArray.astype(np.double), 3)
        outBand.WriteArray(newArray)
        outBand.FlushCache()

    def focal( self, newGtiffPath, kernFunc ):
        """
        Assign a new value to each pixel in self based on focal map algebra. Return a new GeoTiff at filepath newGtiffPath.
        @param newGtiffPath - the filepath of the output GeoTiff
        @param kernFunc - the neighborhood function which returns the kernel array
        @return N/A; write new raster to newGtiffPath
        TODO: Make newGtiffPath optional
        """

        oldArray = self.gField.ReadAsArray()
        newArray = oldArray.copy()
        rows = oldArray.shape[0]
        cols = oldArray.shape[1]
        for i in range (1, rows-1):
            for j in range (1, cols-1):
                newVal = kernFunc(oldArray,(i,j))
                newVal = np.round(newVal, 3)
                newArray.itemset((i,j), newVal)
        driver = self.gField.GetDriver()
        newRaster = driver.CreateCopy(newGtiffPath, self.gField)
        outBand = newRaster.GetRasterBand(1)
        newArray = np.around(newArray.astype(np.double), 3)
        outBand.WriteArray(newArray)
        outBand.FlushCache()
        
    def zonal( self, newGtiffPath, zoneFunc ):
        """
        Assign a new value to self based on zonal map algebra. Return a new GeoTiff at filepath newGtiffPath.
        @param newGtiffPath - the filepath of the output GeoTiff
        @param zoneFunc - the zonal function, which returns a new value for each pixel based on zonal operation
        @return N/A; write new raster to newGtiffPath
        """
        
        oldArray = self.gField.ReadAsArray()
        newArray = oldArray.copy()
        rows = oldArray.shape[0]
        cols = oldArray.shape[1]
        for i in range (0, rows):
            for j in range (0, cols):
                newVal = zoneFunc(oldArray, (i,j))
                newArray.itemset((i,j), newVal)
        driver = self.gField.GetDriver()
        newRaster = driver.CreateCopy(newGtiffPath, self.gField)
        outBand = newRaster.GetRasterBand(1)
        newArray = np.around(newArray.astype(np.double), 3)
        outBand.WriteArray(newArray)
        outBand.FlushCache()
