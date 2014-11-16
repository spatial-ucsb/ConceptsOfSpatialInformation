from coreconcepts import AFields
import numpy as np
import gdal
from gdalconst import *

def funcCaller (a, func):
    return func(a)


class GeoTiffFields(AFields):
    """
    Subclass of Abstract Fields in the GeoTiff format
    """
    @staticmethod
    def getValue( gtiff, position ):
        """
        Returns the value of a pixel at an input position
        @param gtiff the GeoTiff
        @param position the coordinate pair in GeoTiff's coordinate system
        @return the raw value of the pixel at position in GeoTiff
        """
        #Get geo-coords for transformation
        transform = gtiff.GetGeoTransform()
        #Convert geo-coords to image space
        ulx = int(transform [0])
        uly = int(transform [3])
        xQuery = position [0]
        yQuery = position [1]
        pixWidth = transform [1]
        pixHeight = transform [5]
        arrx = int((xQuery - ulx)/pixWidth)
        arry = int((yQuery - uly)/pixHeight)
        #Convert image to array
        array = gtiff.ReadAsArray(arrx,arry,1,1)
        return array

    
    @staticmethod
    def setValue ( gtiff, position, value ):
        """
        TODO: add description of function here
        @param gtiff ? 
        @param position ?
        @param value ?
        @return ?
        """
        #Get geo-coords for transformation
        transform = gtiff.GetGeoTransform()
        #Convert geo-coords to image space
        ulx = int(transform [0])
        uly = int(transform [3])
        xQuery = position [0]
        yQuery = position [1]
        pixWidth = transform [1]
        pixHeight = transform [5]
        arrx = int((xQuery - ulx)/pixWidth)
        arry = int((yQuery - uly)/pixHeight)
        #Convert image to array
        array = np.array([value], ndmin=2)
        band = gtiff.GetRasterBand(1)
        band.WriteArray(array,arrx,arry)
      

    @staticmethod
    def local (gtiff, position, func):
        """
        Assign a new value to position based on input function.
        @param gtiff ? 
        @param position ?
        @param func ?
        @return ?
        """
        #Get geo-coords for transformation
        transform = gtiff.GetGeoTransform()
        #Convert geo-coords to image space
        ulx = int(transform [0])
        uly = int(transform [3])
        xQuery = position [0]
        yQuery = position [1]
        pixWidth = transform [1]
        pixHeight = transform [5]
        arrx = int((xQuery - ulx)/pixWidth)
        arry = int((yQuery - uly)/pixHeight)
        #Convert image to array
        oldArray = gtiff.ReadAsArray(arrx,arry,1,1)
        newArray = funcCaller(oldArray, func)
        band = gtiff.GetRasterBand(1)
        band.WriteArray(newArray,arrx,arry)

    @staticmethod
    def focal (gtiff, position, func):
        """
        Assign a new value to position based on input function using neighboring values.
        Here we use a 3X3 window, but this is arbitrary.
        @param gtiff ? 
        @param position ?
        @param func ?
        @return ?
        """
        #Get geo-coords for transformation
        transform = gtiff.GetGeoTransform()
        #Convert geo-coords to image space
        ulx = int(transform [0])
        uly = int(transform [3])
        xQuery = position [0]
        yQuery = position [1]
        pixWidth = transform [1]
        pixHeight = transform [5]
        arrx = int((xQuery - ulx)/pixWidth)
        arry = int((yQuery - uly)/pixHeight)
        #Convert image to array
        oldArray = gtiff.ReadAsArray(arrx-1,arry-1,3,3) #get neighborhood window (3X3 matrix)
        newArray = funcCaller(oldArray, func)
        band = gtiff.GetRasterBand(1)
        band.WriteArray(newArray,arrx,arry)

