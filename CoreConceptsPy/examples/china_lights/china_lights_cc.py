#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Abstract: Implementation of China Lights case study using Python Core Concepts

@todo: check test/fields_test.py for field logic
@todo: check object logic in test/objects_test.py
@todo: use GeoTiffField for fields. use ArcShpObject for objects, and build_object_set for object sets.
"""

__author__ = ""
__copyright__ = ""
__credits__ = ["", ""]
__license__ = ""
__version__ = ""
__maintainer__ = ""
__email__ = ""
__date__ = ""
__status__ = ""

import sys
import os
import unittest
import numpy as np
import random

sys.path = [ '.', '..', '../..' ] + sys.path
from utils import _init_log, float_eq
from fields import *

    
def load_data():
    print "loadData..."
    # PSEUDO CODE
    #      china = new object("China.shp")
    #      gas_flares = new object_set("Flares_China_1.shp") 
    #      roads = new object_set("a2010_final_proj.shp") 
    #      lights_101994 = new field("F101994", china, inside) 
    #      lights_121994 = new field("F121994", china, inside)
    
    # PYTHON CODE
    field_path = 'data/some_raster.tiff'
    objectset_path = 'data/someshapefile.shp'
    # TODO: load data here using the right classes
    # use addDomain on the fields
    
    # light_1994a_field = GeoTiffField( field_path )
    # light_1994b_field = GeoTiffField( field_path2 )
    # flare_objset = CcObjectSet( flare_path )
    # etc
    return None,None,None

def build_object_set( shpfile_path ):
    # TODO: scan through shapefile with ArcShpObject and build object set
    objs = CcObjectSet()
    # TODO: add objects
    return objs

def field_avg(field_a, field_b):
    # TODO: implement field average function
    return None
    
def compute_luminosity( light_1994a_field, light_1994b_field, flare_objset ):
    print "Compute luminosity"
    # PSEUDO CODE
    #        # What is the luminosity in year 1994 in China,
    #        # excluding gas flares?
    #        luminosity_1994 = local(lights_101994, lights_121994, average)     
    #        luminosity_excluding_flares = set_domain(luminosity_1994, gas_flares, outside)
    #        # What is the luminosity within 0.5 degrees from roads?
    #        roads_buffered = buffer(roads, 0.5) luminosity_around_roads = set_domain(luminosity_1994, roads_buffered, inside)
    #        # What is the mean luminosity in a 0.1 by 0.1 degree area?
    #        final_result = coarsen(luminosity_around_roads, 0.1, 0.1)
    
    # PYTHON CODE
    # light_1994_field = light_1994a_field.local( light_1994b_field, field_avg )
    # TODO

def main():
    print 'Running China Lights case study'
    light_1992_field, light_1994_field, flare_objset = load_data()
    luminosity_field = compute_luminosity( light_1992_field, light_1994_field, flare_objset )
    print 'OK'

if __name__ == '__main__':
    main()
