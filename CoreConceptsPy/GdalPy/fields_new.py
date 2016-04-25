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

import types

import numpy as np
import numpy.ma as ma
import gdal
from gdalconst import *

from utils import _init_log
from coreconcepts import CcField

VALID_LOCAL_OPS = ('average', 'min', 'max')

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

def _copy_and_update_dataset(raster, data, in_memory=True, filepath=None):
    """
    Copies input raster but replaces data (preserving transform, projection, etc)

    @param raster - Original raster to be copied
    @param data - Array of data that will overwrite original data
    @param in_memory - Boolean to indicate if new raster will be in memory (instead of saved to disk)
    @param filepath - Location of new raster if being saved to disk

    @return - The new gdal dataset (ie, raster)
    """

    if in_memory:
        driver = gdal.GetDriverByName('MEM')
        newRaster = driver.CreateCopy('', raster)
    elif filepath:
        driver = raster.GetDriver()
        newRaster = driver.CreateCopy(filepath, raster)
        
    #assuming only 1 band (incorrect?)    
    outBand = newRaster.GetRasterBand(1)
    outBand.WriteArray(newArray)
    outBand.FlushCache()

    return newRaster


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
    def __init__(self, data, projection, transform, nodata=None, domain=None):
        """
        @param filepath path to the GeoTiff field
        @param geometry domain of the field 
        @param operation 'inside' or 'outside' 
        """
        self.data = data
        self.projection = projection
        self.transform = transform
        self.nodata = nodata
        self.domain = domain
        
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
        """
        Restricts current instance's domain based on object's domain
        @param object an object to be subtracted to the current domain
        @param operation an operation to be performed based on the object
        """
        # TODO: implement
        # add [geometry,operation] to self.domain_geoms
        
        #use gdal.RasterizeLayer(arr, [1], layer, None, None, [1], ['ALL_TOUCHED=TRUE'])
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
        

    @classmethod
    def local(cls, fields, func, newGtiffPath=None):
        """
        Assign a new value to each pixel in gtiff based on func. Return a new GeoTiff at newGtiffPath.

        "Local operations

        A local operation acts upon one or more spatial fields to produce a new field. The distinguishing feature
        of a local operation is that the value is dependent only on the values of the input field functions at that location.
        Local operations may be unary (transforming a single field), binary (transforming two fields), or n-ary (transforming
        any number of fields).

        1. For each location x, h(x) = f(x) dot g(x)" (Worboys & Duckham 148)

        @param fields - List of input fields (assuming all fields have same projection and transform)
        @param func - The local function (can be either an actual function or string (eg, 'average', 'min', 'max'))

        @return - A new GeoTiffField object that 
        """

        if isinstance(func, types.FunctionType):
            #if @func is function, use np.vectorize to make sure it's a universal function
            func = np.vectorize(func)
        elif func in VALID_LOCAL_OPS:
            #if @func is a string specifying a numpy function (eg, 'min')
            func = getattr(np, func)
        else:
            raise ValueError("Error: @func must be either a function or one of the following strings: %s" 
                % ', '.join(VALID_LOCAL_OPS))

        #stack the rasters
        stacked = np.dstack([f.data for f in fields])

        #apply function along stacked axis (note: this assumes 2d raster with only 1 band)
        newArray = func(stacked, axis=2)

        #necessary?  causing memory errors...
        #newArray = np.around(newArray.astype(np.double), 3)

        projection = fields[0].projection
        transform = fields[0].transform
        nodata = fields[0].nodata

        return cls(newArray, projection, transform, nodata)

    def to_file(self, filepath):
        nrows, ncols = self.data.shape

        #assuming we are saving a GeoTIFF...
        driver = gdal.GetDriverByName('GTiff')
        dataset = driver.Create(filepath, ncols, nrows, 1, gdal.GDT_Byte)

        dataset.SetProjection(self.projection)
        dataset.SetGeoTransform(self.transform)
        
        band = dataset.GetRasterBand(1)

        if self.nodata:
            band.SetNoDataValue(self.nodata)

        band.WriteArray(self.data)
        band.FlushCache()

        #should clean up on its own, but delete just in case
        del dataset

    @classmethod 
    def from_file(cls, filepath):
        return cls.from_gdal_dataset(gdal.Open(filepath))

    @classmethod
    def from_gdal_dataset(cls, dataset):
        data = dataset.ReadAsArray()
        projection = dataset.GetProjection()
        transform = dataset.GetGeoTransform()
        nodata = dataset.GetRasterBand(1).GetNoDataValue()

        return cls(data, projection, transform, nodata)


if __name__ == '__main__':
    #example usage:

    #should these input methods be part of 'fields' (ie, fields.from_file()?)
    field1 = GeoTiffField.from_file('chinaLights1.tif')
    field2 = GeoTiffField.from_file('chinaLights2.tif')

    average = GeoTiffField.local([field1, field2], 'average')

    average.to_file('chinaLights_average.tif')

