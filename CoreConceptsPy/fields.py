# -*- coding: utf-8 -*-

"""
 Abstract: These classes are implementations of the core concept 'field', as defined in coreconcepts.py
           The class is written in an object-oriented style.
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
    Convert GeoTiff coordinates to matrix offset. Used for getValue GeoTiffField method and focal mean function.
    @param position - the input geocoordinates in coordinate system of gtiff
    @return - the i,j pair representing input position in the image matrix
    """
    transform = gtiff.GetGeoTransform()
    #Convert geo-coords to (i,j) image space coordinates
    ulx = transform [0]
    uly = transform [3]
    xQuery = position [0]
    yQuery = position [1]
    pixWidth = transform [1]
    pixHeight = transform [5]
    arrx = int((xQuery - ulx)/pixWidth)
    arry = int((yQuery - uly)/pixHeight)
    return arry, arrx

def FieldGranularity(CcGranularity):
    # TODO: 
    def __init__( self, x, y ):
        pass

class GeoTiffField(CcField):
    """
    Subclass of Abstract Fields (core concept 'field') in the GeoTiff format. Based on GDAL.

    Map algebra based on Worboys & Duckham (2004), precise definitions from the text are included with each function.

    Worboys, Michael, and Matt Duckham. GIS : a computing perspective. Boca Raton, Fla: CRC Press, 2004. Print.

    """
    def __init__( self, filepath, geometry, operation ):
        """
        @param filepath path to the GeoTiff field
        @param geometry domain of the field 
        @param operation 'inside' or 'outside' 
        """
        assert operation in ['inside','outside']
        self.gField = gdal.Open( filepath, GA_Update )
        # set the initial domain of the field
        # TODO: add the geometry to the domain_geoms tuple
        self.domain_geoms = () # tuple [geometry, 'inside'|'outside']

    def value_at( self, position ):
        """
        Returns the value of a raster pixel at an input position.
        
        @param position the coordinate pair in self's coordinate system
        @return the raw value of the pixel at input position in self or None if it is outside of the domain
        """
        if self._is_in_domain(position):
            offset = getGtiffOffset( self.gField, position )
            array = self.gField.ReadAsArray( offset[1],offset[0], 1,1 ) #Convert image to NumPy array
            return array
        else: return None
    
    def _is_in_domain(self, position ):
        """
        @param position 
        @return True if position is in the current domain or False otherwise 
        """
        # TODO: implement using self.domain_geoms

    def zone( self, position ):
        """
        Return a masked array representing the zone for the input position
        @param position - i,j coordinates from which to derive zone
        @return - NumPy masked array representing the geometry of the zone for pixel at input position
        """
        array = self.gField.ReadAsArray()
        val = array[position[0], position[1]]
        maskArray = ma.masked_not_equal( array, val )  #All values not equal to zone value of input are masked
        return maskArray

    def local( self, fields, func, newGtiffPath ):
        """
        Assign a new value to each pixel in gtiff based on func. Return a new GeoTiff at newGtiffPath.

        "Local operations

        A local operation acts upon one or more spatial fields to produce a new field. The distinguishing feature
        of a local operation is that the value is dependent only on the values of the input field functions at that location.
        Local operations may be unary (transforming a single field), binary (transforming two fields), or n-ary (transforming
        any number of fields).

        1. For each location x, h(x) = f(x) dot g(x)" (Worboys & Duckham 148)

        @param fields - other input fields 
        @param func - the local function to be applied to each value in GeoTiff
        @param newGtiffPath - file path for the new GeoTiff
        @return N/A; write new raster to newGtiffPath
        """
        oldArray = self.gField.ReadAsArray()
        newArray = func(oldArray)
        # TODO: update to handle input fields
        driver = self.gField.GetDriver()
        newRaster = driver.CreateCopy(newGtiffPath, self.gField)
        outBand = newRaster.GetRasterBand(1)
        newArray = np.around(newArray.astype(np.double), 3)
        outBand.WriteArray(newArray)
        outBand.FlushCache()

    def focal( self, fields, kernFunc, newGtiffPath ):
        """
        Assign a new value to each pixel in self based on focal map algebra. Return a new GeoTiff at filepath newGtiffPath.

        "Focal operations

        For a focal operation the attribute value derived at a location x may depend not only on the attributes of the input
        spatial field functions at x, but also on the attributes of these functions in the neighborhood n(x) of x. Thus, the
        value of the derived field at a location may be influenced by the values of the input field nearby that location.

        For each location x:
        1. Compute n(x) as the set of neighborhood points of x (usually including x itself).
        2. Compute the values of the field function f applied to appropriate points in n(x).
        3. Derive a single value phi(x) of the derived field from the values computed in step 2, possibly taking special account
        of the value of the field at x." (Ibid. 148-9)

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

    def zonal( self, fields, zoneFunc, newGtiffPath ):
        """
        Assign a new value to self based on zonal map algebra. Return a new GeoTiff at filepath newGtiffPath.

        "Zonal operations

        A zonal operation aggregates values of a field over each of a set of zones (arising in general from another field function)
        in the spatial framework. A zonal operation zeta derives a new field based on a spatial framework F, a spatial field f, and
        set of k zones {Z1,…,Zk} that partitions F.

        For each location x:
        1. Find the zone Zi in which x is contained.
        2. Compute the values of the field function f applied to each point in Zi.
        3. Derive a single value zeta(x) of the new field from the values computed in step 2." (Ibid. 149-50)

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
        
    def domain(self):
        # TODO: implement
        raise NotImplementedError("domain")
    
    def restrict_domain(self, geometry, operation ):
        # TODO: implement
        # add [geometry,operation] to self.domain_geoms
        pass 
    
    def coarsen(self, granularity, func ):
        """
        Constructs new field with lower granularity.
        
        Default strategy: mean
        @param granularity a FieldGranularity
        @param aggregation strategy func
        @return a new coarser field
        """
        pass
        # TODO: implement with 'aggregate' in GDAL
        # default strategy: mean
        # http://gis.stackexchange.com/questions/110769/gdal-python-aggregate-raster-into-lower-resolution 
        
        