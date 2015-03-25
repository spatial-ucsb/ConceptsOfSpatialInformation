#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Abstract: Derive aspect values from a digital elevation model as an example of the core concept 'field'

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

sys.path = [ '.', '../..' ] + sys.path
from utils import _init_log
from fields import *

log = _init_log("aspectCalc")

# Import system modules
import arcpy
from arcpy import env
from arcpy.sa import *
import os

# Set environment settings
env.workspace = os.path.join("..","..","..","data","fields")

# Set local variables
inRaster = "CalPolyDEM.tif"
outMeasurement = "DEGREE"

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

# Execute Aspect
outAspect = Aspect(inRaster)

# Save the output 
outAspect.save(os.path.join("..","..","..","data","fields","tmp","outAspect"))