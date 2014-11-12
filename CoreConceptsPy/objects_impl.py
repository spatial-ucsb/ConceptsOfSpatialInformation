from coreconcepts import AObjects
from osgeo import gdal, gdal_array
import ogr, os, osr
from gdalconst import *
import numpy as np


class ArcShpObjects(AObjects):
    """
    TODO: add description of class here
    """
    @staticmethod
    def getBounds (obj):
        #Get geometery
        geom = obj.GetGeometryRef()
        env = geom.GetEnvelope()
        #Return bounds in form (MinX, MaxX, MinY, MaxY)
        return env

    @staticmethod
    def hasRelation (obj1, obj2, relType):
        #Get geometeries
        assert relType in ['Intersects','Equals','Disjoint','Touches','Crosses','Within','Contains','Overlaps']
        geom1 = obj1.GetGeometryRef()
        geom2 = obj2.GetGeometryRef()
        #Possible relations are: Intersects, Equals, Disjoint, Touches, Crosses, Within, Contains, Overlaps
        if getattr(geom1,relType)(geom2): #getattr is equivalent to geom1.relType
            return True
        else:
            return False

    @staticmethod
    def getProperty (obj, prop):
        #Get index of property - note: index 13 is building name
        index = obj.GetFieldIndex(prop)
        #Return value as a string
        value = obj.GetFieldAsString(index)
        return value
