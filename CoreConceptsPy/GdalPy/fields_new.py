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

VALID_LOCAL_OPS = ('average', 'mean', 'median', 'min', 'minimum', 'max', 'maximum')
VALID_DOMAIN_OPS = ('inside', 'outside')

log = _init_log("fields")

#put these utility functions in utils.py?
def _pixel_to_coords(col, row, transform):
    """Returns the geographic coordinate pair (lon, lat) for the given col, row, and geotransform."""

    lon = transform[0] + (col * transform[1]) + (row * transform[2])
    lat = transform[3] + (col * transform[4]) + (row * transform[2])

    return lon, lat

def _coords_to_pixel(y, x, transform):
    """Returns raster coordinate pair (col, row) for the given lon, lat, and geotransform."""

    col = int((y - transform[0]) / transform[1])
    row = int((x - transform[3]) / transform[5])

    return col, row


def local(fields, func, domain=None):
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
    unique_projections = set(field.projection for field in fields)
    unique_transforms = set(field.transform for field in fields)

    if len(unique_projections) > 1:
        raise ValueError("Error: each field in @fields must have the same projection.") 

    if len(unique_transforms) > 1:
        raise ValueError("Error: each field in @fields mut have the same geotransform.")

    if isinstance(func, types.FunctionType):
        #if @func is function, use np.vectorize to make sure it's a universal function
        func = np.vectorize(func)
    elif func in VALID_LOCAL_OPS:
        #if @func is a string specifying a numpy function (eg, 'min')
        func = getattr(np, func)
    else:
        raise ValueError("Error: @func must be either a function or one of the following strings: %s" 
            % ', '.join(VALID_LOCAL_OPS))

    #stack the rasters (is this less memory-efficient than a loop? need to build an extra array)
    stacked = np.dstack([f.data for f in fields])

    #apply function along stacked axis (note: this assumes 2d raster with only 1 band)
    newArray = func(stacked, axis=2)

    #necessary?  causing memory errors...
    #newArray = np.around(newArray.astype(np.double), 3)

    #assuming all fields have the same projection, transform, and nodata (check for this earlier?)
    projection = fields[0].projection
    transform = fields[0].transform
    domain = fields[0].domain
    nodata = fields[0].nodata

    return GeoTiffField(newArray, projection, transform, nodata)


def from_file(filepath, converter=None):
    return from_gdal_dataset(gdal.Open(filepath), converter)

def from_gdal_dataset(dataset, converter=None):
    """
    QUESTIONS:
    * If converting multi-band raster into single-band field, read entire thing into memory?
    """
    data = dataset.ReadAsArray()
    projection = dataset.GetProjection()
    transform = dataset.GetGeoTransform()
    nodata = dataset.GetRasterBand(1).GetNoDataValue()

    if converter:
        data = converter(data)

    return GeoTiffField(data, projection, transform, nodata)


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
    def __init__(self, data, projection, transform, domain=None, nodata=None):
        """
        @param data - 2-dimensional numpy array representing the raster data
        @param projection - projection information in WKT format
        @param transform - 6-dimensional tuple representing the geotransform in GDAL format
        @param domain - GEOMETRIES?
        @param nodata - no data value

        QUESTIONS: 
        * Should @domain be a mask or geometries?
        * Is it asking too much to store the full array in memory?
        """
        self.projection = projection
        self.transform = transform
        self.nodata = nodata or -1
        self.domain = domain or np.ones(data.shape)
        self.data = ma.array(data, mask=domain==1)
        
    def value_at(self, col, row):
        """
        Returns the value of a raster pixel at an input position.
        
        @param position the coordinate pair in self's coordinate system
        @return the raw value of the pixel at input position in self or None if it is outside of the domain
        """
        if self._is_in_domain(position):
            col, row = _coords_to_pixel(x, y, self.transform)
            val = self.data[col, row]
            
            return val
        
        return None
    
    def _is_in_domain(self, col, row):
        """
        @param position 
        @return True if position is in the current domain or False otherwise 
        """
        
        return bool(self.data[col, row])

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

        oldArray = self.data
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
        """
        Return mask or actual geometries?
        """
        # TODO: implement
        raise NotImplementedError("domain")
    
    def restrict_domain(self, layer, operation='inside'):
        """
        Restricts current instance's domain based on object's domain

        NOTES: Should @layer be a single Object or a set of Objects? How to handle the fact that we need an OGR
        object to call RasterizeLayer?  Implement layer.to_ogr_object()? 

        @param layer - The layer (allow objects?) that defines the domain
        @param operation - inside or outside
        """

        if operation not in VALID_DOMAIN_OPS:
            raise ValueError("Error: %s is not a valid operation on restrict_domain." % operation)

        nrows, ncols = self.data.shape

        mask_raster = gdal.GetDriverByName('MEM').Create('', nrows, ncols, 1, gdal.GDT_Byte)
        mask_raster.SetProjection(self.projection)
        mask_raster.SetGeoTransform(self.transform)
        mask_raster.GetRasterBand(1).Fill(0)

        #this function burns the polygons onto the raster
        #NOTE: this freezes with in memory raster (use temp file?)
        gdal.RasterizeLayer(mask_raster, [1], layer, None, None, [1], ['ALL_TOUCHED=TRUE'])

        self.data.mask = mask_raster.ReadAsArray()

        if operation == 'outside': 
            self.data.mask = np.absolute(self.domain_mask - 1)

    def coarsen(self, pixel_size, func='average'):
        """
        Constructs new field with lower granularity.

        NOTES: 

        1) Should this technically be called "resample"?

        2) Resampling seems unnecessarily complicated using the GDAL python wrapper.
        The command-line 'gdalwarp' is the C++ option, but there is no similar function in 
        python.  This approach is inspired by:

        http://gis.stackexchange.com/questions/139906/replicating-result-of-gdalwarp-using-gdal-python-bindings
        
        @param pixel_size - the desired pixel size (use FieldGranularity in future?)
        @param func - the name of the function used t aggergate
        @return - a new coarser field
        """
        
        if func in ('average', 'mean'):
            func = gdal.GRA_Average
        elif func == 'bilinear':
            func = gdal.GRA_Bilinear
        elif func == 'cubic':
            func = gdal.GRA_Cubic
        elif func == 'cubic_spline':
            func = gdal.GRA_CubicSpline
        elif func == 'lanczos': 
            func = gdal.GRA_Lanczos
        elif func == 'mode':
            func = gdal.GRA_Mode
        elif func == 'nearest_neighbor':
            func = gdal.GRA_NearestNeighbour
        else:
            raise ValueError("Error: 'func' not a valid value.")

        #get bounds of current raster
        minx, miny, maxx, maxy = self.bounds()

        dst_nrows = abs(int((maxx - minx) / float(pixel_size)))
        dst_ncols = abs(int((maxy - miny) / float(pixel_size)))

        #note: seems like there is a maximum number of rows X columns (if exceeded, will return None)
        driver = gdal.GetDriverByName('MEM')
        dst = driver.Create('', dst_nrows, dst_ncols, 1, gdal.GDT_Byte)

        dst_transform = (minx, pixel_size, 0, maxy, 0, -pixel_size)
        dst.SetGeoTransform(dst_transform)
        dst.SetProjection(self.projection)
        
        orig_dataset = self.to_gdal_dataset()

        gdal.ReprojectImage(orig_dataset, dst, self.projection, self.projection, func)

        return from_gdal_dataset(dst)

    def bounds(self):
        """
        Returns the bounds (in defined units) of the current object.

        @return - Bounds of current object in format: (minx, maxy, maxx, miny)
        """

        minx, pixelx, _, maxy, _, pixely = self.transform
        nrows, ncols = self.data.shape
        maxx, miny = minx + (ncols * pixelx), maxy - (nrows * pixely)

        return (minx, miny, maxx, maxy)

    def local(self, func):
        """
        Unary local operation.
        """

        if isinstance(func, types.FunctionType):
            #if @func is function, use np.vectorize to make sure it's a universal function
            func = np.vectorize(func)
        else:
            raise ValueError("Error: @func must be a function.")


        #NOTE: How to deal with pixels outside the domain?  Perform local function but keep domain?
        newArray = func(self.data)
        projection = self.projection
        transform = self.transform
        domain = self.domain
        nodata = self.nodata

        return GeoTiffField(newArray, projection, transform, nodata)

    def to_gdal_dataset(self):
        """
        Returns a GDAL DataSet object.
        """

        nrows, ncols = self.data.shape

        #assuming we are saving a GeoTIFF...
        driver = gdal.GetDriverByName('MEM')
        dataset = driver.Create('', ncols, nrows, 1, gdal.GDT_Byte)

        dataset.SetProjection(self.projection)
        dataset.SetGeoTransform(self.transform)
        
        band = dataset.GetRasterBand(1)

        if self.nodata:
            band.SetNoDataValue(self.nodata)

        band.WriteArray(self.data)
        band.FlushCache()

        return dataset

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




if __name__ == '__main__':
    #example usage:

    import os, objects

    cur_path = os.path.dirname(os.path.realpath(__file__))

    #should these input methods be part of 'fields' (ie, fields.from_file()?)
    china_lights1 = from_file(china_lights1_filepath)
    china_lights2 = from_file(china_lights2_filepath)
    china_boundary = objects.from_file(china_boundary_filepath)
    gas_flares = objects.from_file(gas_flares_filepath)

    china_lights1 = china_lights1.restrict_domain(china_boundary, 'inside')    
    china_lights2 = china_lights2.restrict_domain(china_boundary, 'inside')

    average_luminosity = fields.local([china_lights1, china_lights2], 'average')

    #remove gas flares
    luminosity = average_luminosity.restrict_domain(gas_flares, 'outside')

    #create roads buffer
    roads = objects.from_file(china_roads_filepath)

    #buffer roads
    roads_buffered = roads.buffer(0.5, 'DecimalDegrees') # TODO: updated function calling convention (exclude object)

    # restrict domain of luminosity to road buffer
    luminosity_around_roads = luminosity.restrict_domain(roads_buffered, 'inside')

    # aggregate previous information
    results = luminosity_around_roads.coarsen(0.1, 0.1)







