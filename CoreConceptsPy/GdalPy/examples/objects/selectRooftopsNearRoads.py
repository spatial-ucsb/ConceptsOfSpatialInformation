#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Abstract: Select all rooftops within 50 m of a road and create a new shapefile. This is an example of the relation function 
from the core concept 'objects.'

"""

__author__ = "Eric Ahlgren"
__copyright__ = "Copyright 2015"
__credits__ = ["Eric Ahlgren"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = ""
__email__ = ""
__date__ = "March 2015"
__status__ = "Development"

import sys
import os

sys.path = [ '.', '../..' ] + sys.path
from utils import _init_log

# Import arcpy and set path to data
import arcpy
from arcpy import env

env.workspace = os.path.join("..","..","..","data","objects")
env.overwriteOutput = True

# Make a layer and select rooftops within 50 m of roads
arcpy.MakeFeatureLayer_management('rooftops_pv.shp', 'rooftops_lyr') 
arcpy.SelectLayerByLocation_management('rooftops_lyr', 'WITHIN_A_DISTANCE', 'roads.shp',50)

# If features matched criteria write them to a new feature class
matchcount = int(arcpy.GetCount_management('rooftops_lyr').getOutput(0))
outfile = os.path.join("..","..","..","data","objects","tmp","roofs_within50mroads.shp")
if matchcount == 0:
    print('no features matched spatial and attribute criteria')
else:
    arcpy.CopyFeatures_management('rooftops_lyr',outfile )
    print('{0} rooftops that matched criteria written to {1}'.format(
                                                  matchcount, outfile))