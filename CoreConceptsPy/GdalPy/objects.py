# -*- coding: utf-8 -*-

"""
 Abstract: These classes are implementations of the core concept 'object', as defined in coreconcepts.py
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

import ogr

from utils import _init_log
from coreconcepts import CcObject, CcObjectSet

log = _init_log("objects")

VALID_RELATIONS = ('Intersects','Equals','Disjoint','Touches','Crosses','Within','Contains','Overlaps')

def from_file(filepath):
    shp = ogr.Open(filepath)
    layer = shp.GetLayer(0)

    return OgrShpObjectSet(layer)


class OgrShpObject(CcObject):
    """
    Subclass of Abstract Object (CcObject) in the ArcMap Shapefile format
    """
    def __init__( self, filepath, objIndex ):
        shpfile =  ogr.Open(filepath)
        layer = shpfile.GetLayer(0)
        self.sObj = layer.GetFeature(objIndex)

    def bounds( self ):
        #Get geometery
        geom = self.sObj.GetGeometryRef()
        env = geom.GetEnvelope()
        #Return bounds in form (MinX, MaxX, MinY, MaxY)
        return env

    def relation( self, obj, relType ):
        
        if relType not in VALID_RELATIONS:
            raise ValueError("{0} is not a valid value for 'relType'.".format(relType))
        
        #Get geometeries
        geom1 = self.sObj.GetGeometryRef()
        geom2 = obj.sObj.GetGeometryRef()
        return getattr(geom1,relType)(geom2) #getattr is equivalent to geom1.relType

    def property( self, prop ):
        #Get index of property - note: index 13 is building name
        index = self.sObj.GetFieldIndex(prop)

        if index == -1:
            raise ValueError("{0} is not a valid property.".format(prop))

        propDefn = self.sObj.GetFieldDefnRef(index)
        propType = propDefn.GetType()
        #Return value as a propType
        if propType == "OFTInteger":
            value = self.sObj.GetFieldAsInteger(index)
        elif propType == "OFTReal":
            value = self.sObj.GetFieldAsDouble(index)
        elif propType == "OFTString":
            value = self.sObj.GetFieldAsString(index)
        elif propType == "OFTBinary":
            value = self.sObj.GetFieldAsBinary(index)
        elif propType == "OFTDateTime":
            value = self.sObj.GetFieldAsDateTime(index)
        else:
            value = self.sObj.GetFieldAsString(index)
        return value

    def identity( self, obj ):
        return self.relation( obj, 'Equals' )

    def buffer(self, val, units=None):
        """
        NOTES:
        * Not dealing with units yet. OGR doesn't perform geodesic buffering, so need to reproject
        if data is in unprojected coordinate system (eg, WGS84) in order to specify miles, kilometers, etc.?
        """

        geom = self.sObj.GetGeometryRef()

        return geom.Buffer(val)

    def to_ogr_datasource(self):
        pass


        
class OgrShpObjectSet(CcObjectSet):
    def __init__(self, layer):
        """
        NOTE: Should this class contain a list of ArcShpObjects, or just refer to the ogr layer?
        """
        self.layer = layer
        
    def bounds(self):
        """ 
        Return bounds of entire ObjectSet in form of (MinX, MaxX, MinY, MaxY) 
        """
        
        return self.layer.GetExtent()

    def buffer(self, val):
        """
        Buffer all objects in this set.

        NOTES: 
        * Return self or new ObjectSet?
        * Not dealing with units yet. OGR doesn't perform geodesic buffering, so need to reproject
        if data is in unprojected coordinate system (eg, WGS84) in order to specify miles, kilometers, etc.?
        """

        for indx in xrange(self.layer.GetFeatureCount()):
            feature = self.layer.GetFeature(indx)
            geom = feature.GetGeometryRef()
            buffered = geom.Buffer(val)
            feature.SetGeometry(buffered)

