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
        @param position the coordinate pair in gtiff's coordinate system
        @return the raw value of the pixel at position in gtiff
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
        Updates the value of a pixel at an input position
        @param gtiff the GeoTiff
        @param position the coordinate pair in GeoTiff's coordinate system
        @param value the new value for pixel at position in GeoTiff
        @return n/a; write to gtiff
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
        Assign a new value to a pixel at position based on input function
        @param gtiff the GeoTiff 
        @param position the coordinate pair in GeoTiff's coordinate system
        @param func the function to be applied to the pixel at position
        @return n/a; write to gtiff
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
        Assign a new value to position based on input function using neighboring values
        (Here we use a 3X3 window, but this is arbitrary)
        @param gtiff the GeoTiff
        @param position the coordinate pair of the center of the window, in gtiff's coordinate system
        @param func the function to be applied to the matrix and return new value for pixel at position
        @return n/a; write to gtiff
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

