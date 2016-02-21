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
from coreconcepts import CcObject

log = _init_log("objects")

class ArcShpObject(CcObject):
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
        #Get geometeries
        assert relType in ['Intersects','Equals','Disjoint','Touches','Crosses','Within','Contains','Overlaps']
        geom1 = self.sObj.GetGeometryRef()
        geom2 = obj.sObj.GetGeometryRef()
        if getattr(geom1,relType)(geom2): #getattr is equivalent to geom1.relType
            return True
        else:
            return False

    def property( self, prop ):
        #Get index of property - note: index 13 is building name
        index = self.sObj.GetFieldIndex(prop)
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
        if self.relation( obj, 'Equals' ):
            return True
        else:
            return False
        
    class ArcShpObjectSet(CcObjectSet):
        def __init__( self, shp_filepath, objIndex ):
            # TODO: load the objects from the shapefile and add them to self.obj_set