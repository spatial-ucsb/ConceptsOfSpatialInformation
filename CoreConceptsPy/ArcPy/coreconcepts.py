# -*- coding: utf-8 -*-
import os

# TODO: refactor so that following arc implementations aren't called unless arc processing is needed
import arcpy
from arcpy import env
from arcpy.sa import *

# Set working directory
env.workspace = "C:\Users\lafia\Desktop\chinalights_data" # TODO: set workspace determined by filepath locations
workspace = env.workspace
arcpy.env.overwriteOutput = True
# Check out any necessary licenses
arcpy.CheckOutExtension("spatial")


class CcField(object):
    """
    Class defining abstract field.
    Based on Field.hs
    """
    def __init__(self, filepath, geo_object):
        self.filepath = filepath
        self.domain = geo_object
        # TODO: restrict value pairs to geoObject
        pass

    def value_at(self, position):
        """
        :param: grid cell position
        :returns: the value of field at position, or None if it is outside of the domain.
        """
        # TODO: check if position falls within value
        raise NotImplementedError("value_at")

    def domain(self):
        """
        :returns: current domain of the field
        """
        return self.domain

    def restrict_domain(self, domain_obj, operation):
        """
        :param domain_obj: restricting domain object
        :param operation: inside | outside object
        :return:
        """
        raise NotImplementedError("restrict_domain")

    def local(self, fields, fun):
        """
        :param fields: array of fields
        :param fun: specific local function
        :return:
        """
        # TODO: make a general funtion for more than two fields
        raise NotImplementedError("local")


class CcObject(object):
    """
    Abstract class for core concept 'object'
    Based on Object.hs
    """
    def __init__(self, filepath, obj_index, geo_object):
        """
        :param filepath: data file path
        :param obj_index:
        :param geo_object:
        """
        self.filepath = filepath
        self.sObj = obj_index
        self.domain = geo_object

    def bounds(self):
        raise NotImplementedError("bounds")

    def relation(self, obj, rel_type):
        """
        :param obj:
        :param rel_type:
        :returns: true if self and obj are in a relationship of type relType
        """
        raise NotImplementedError("relation")

    def property(self, prop):
        """
        :param: prop the property name
        :returns: value of property in obj
        """
        raise NotImplementedError("property")

    def identity(self, obj):
        """
        :param obj: an object
        :returns: true if self and obj are identical
        """
        raise NotImplementedError("identity")


class CcGranularity(object):
    """
        Abstract class for core concept 'object'
        Based on Granularity.hs
    """
    def __init__(self):
        # TODO: cell_size_x, cell_size_y
        raise NotImplementedError("CcGranularity")
