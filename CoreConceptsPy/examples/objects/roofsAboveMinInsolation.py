#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Abstract: Select all rooftops that recieve a minimum average of 3.5 kWh of insolation per day and create a new shapefile. This is an example of the property function 
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


# Set local variables
in_features = "rooftops_pv.shp"
out_feature_class = os.path.join("..","..","..","data","objects","tmp","roofs_aboveMinInsol.shp")
where_clause = '"pvrooftop_solar2014.SUM" >= 1277500'

# Execute Select
arcpy.Select_analysis(in_features, out_feature_class, where_clause)