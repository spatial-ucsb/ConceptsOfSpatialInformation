from coreconcepts import AFields
import numpy as np
import gdal
from gdalconst import *


# TODO: document it. What does it do? Call it something like "getGtiffOffset"  
def getGtiffOffset ( gtiff, position ):
    """ 
    Convert GeoTiff coordinates to matrix offset. Used for getValue and setValue GeoTiffField functions. 
    @param gtiff - the geotiff
    @param position - the input geocoordinates
    @return - the i,j pair representing position in the image matrix
    """
        
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
    return arrx, arry

class ArrFields(AFields):
    """ Implementation of AField with Python arrays. """
        
    @staticmethod
    def getValue( field, position ):
        x = position[0]
        y = position[1]
        return field[x,y]
    
    @staticmethod
    def setValue( field, position, value ):
        """ @return the position of new value in field """
        x = position[0]
        y = position[1]
        field[x,y] = value
        return field, position, value
     
    @staticmethod
    def domain( field, position, value ):
        """ @return Domains can be described as intervals, rectangles, corner points, convex hulls or boundaries """
        raise NotImplementedError("domain")

class GeoTiffFields(AFields):
    """
    Subclass of Abstract Fields in the GeoTiff format. Based on GDAL.
    
    Map algebra based on (TODO: specify reference. To clarify what we're doing here, it's important to 
    rely on a GIS textbook.
    e.g. Local operations works on individual raster cells, or pixels.
        Focal operations work on cells and their neighbors, whereas global operations work on the entire layer. 
        Finally, zonal operations work on areas of cells that share the same value.
    )
    """
    @staticmethod
    def getValue( gtiff, position ):
        """
        Returns the value of a pixel at an input position
        @param gtiff the GeoTiff
        @param position the coordinate pair in gtiff's coordinate system
        @return the raw value of the pixel at position in gtiff
        """
        offset = getGtiffOffset( gtiff, position )
        #Convert image to array
        array = gtiff.ReadAsArray( offset[0],offset[1], 1,1 )
        return array

    @staticmethod
    #TODO: style: be consistent with "func (" or "func(". "func(" is more common.
    def setValue ( gtiff, position, value ):
        """
        Updates the value of a pixel at an input position
        @param gtiff the GeoTiff
        @param position the coordinate pair in GeoTiff's coordinate system
        @param value the new value for pixel at position in GeoTiff
        @return n/a; write to gtiff
        """
        offset = getGtiffOffset( gtiff, position )
        #Convert input value to numpy array
        array = np.array([value], ndmin=2)   #Array has to be 2D in order to write
        band = gtiff.GetRasterBand(1)
        band.WriteArray( array, offset[0],offset[1] )
      
    @staticmethod
    def local (gtiff, newGtiffPath, func):
        """
        Assign a new value to each pixel in gtiff based on func. Return a new GeoTiff at newGtiffPath.
        @param gtiff - the GeoTiff 
        @param newGtiffPath - file path for the new GeoTiff
        @param func - the local function to be applied to each value in GeoTiff
        @return array of new GeoTiff values; write new raster to newGtiffPath
        TODO: update with new specs. return new field. read whole field as array and then apply func on it.
        """
        oldArray = gtiff.ReadAsArray()
        newArray = func(oldArray)
        driver = gtiff.GetDriver()
        newRaster = driver.CreateCopy(newGtiffPath, gtiff)
        outBand = newRaster.GetRasterBand(1)
        outBand.WriteArray(newArray)
        outBand.FlushCache()
        return newArray

    @staticmethod
    def focal (gtiff, position, func):
        """
        Assign a new value to position based on input function using neighboring values
        (Here we use a 3X3 window, but this is arbitrary)
        @param gtiff the GeoTiff
        @param position the coordinate pair of the center of the window, in gtiff's coordinate system
        @param func the function to be applied to the matrix and return new value for pixel at position
        @return original matrix for testing; write to gtiff
        TODO: update with new specs. return new field. read whole field as array and then apply func on it.     
        """
        offset = getGtiffOffset( gtiff, position )
        #Convert image to array
        oldArray = gtiff.ReadAsArray( offset[0]-1,offset[1]-1, 3,3 )    #get neighborhood window (3X3 matrix)
        newArray = func(oldArray)
        newArray = np.array([newArray], ndmin = 2)
        band = gtiff.GetRasterBand(1)
        band.WriteArray( newArray, offset[0],offset[1] )
        return oldArray

