#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Abstract: Calculate area for 3 zones of study for a solar panel site-suitability analysis. Zone 1 is rooftops, zone 2 parking 
lots and zone 3 sloping grassland. This is an example of the zonal function from the core concept 'field.'

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

log = _init_log("slopeCalc")

# Import system modules
import arcpy
from arcpy import env
from arcpy.sa import *
import os

# Set environment settings
env.workspace = os.path.join("..","..","..","data","fields")

# Set local variables
inZoneData = "zonalRast.tif"
zoneField = "Value"
cellSize = 1 

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

# Execute ZonalStatistics
outZonalGeometry = ZonalGeometry(inZoneData, zoneField, "AREA", cellSize)  

# Save the output 
outZonalGeometry.save(os.path.join("..","..","..","data","fields","tmp","zonalArea.tif"))