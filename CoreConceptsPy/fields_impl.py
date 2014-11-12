from coreconcepts import AFields
from osgeo import gdal, gdal_array
import ogr, os, osr
from gdalconst import *
import numpy as np
from gdal_calculations import *


class GeoTiffFields(AFields):
    """
    Subclass of Abstract Fields in the GeoTiff format
    """
    @staticmethod
    def getValue( gtiff, position ):
        """
        Returns the value of a pixel at an input position
        @param gtiff ? 
        @param position ?
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
        TODO: add description of function here
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
        oldArray = gtiff.ReadAsArray(arrx,arry,1,1) #get value at position
        try:
            newArray = np.array([eval(str(float(oldArray))+func)], ndmin=2) #perform func on value
        except SyntaxError:
            newArray = np.array([eval(func)(oldArray)], ndmin=2)
        band = gtiff.GetRasterBand(1)
        band.WriteArray(newArray,arrx,arry)

    @staticmethod
        # assign a new value to position based on input function
        # we use here the mean of a 3X3 window
    def focal (gtiff, position, func):
        """
        TODO: add description of function here
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
        try:
            # TODO: I've added an example of this call in the tests, called "testFunctionCall" (AB) 
            newArray = np.array([eval(str(float(oldArray))+func)], ndmin=2) #perform func on value
        except TypeError:
            newArray = np.array([eval(func)(oldArray)], ndmin=2)
        band = gtiff.GetRasterBand(1)
        band.WriteArray(newArray,arrx,arry)

