##################
## Clean Lights ##
##################

# Import arcpy module
import arcpy
from arcpy import env
from arcpy.sa import * 
# Set working directory
env.workspace = "H:/Research/Data/Lights/china.gdb"

# Check out any necessary licenses
arcpy.CheckOutExtension("spatial")

# Input files (all in "H:/Research/Data/Lights/china.gdb")
# (1) Lights (F101992, F101993, F101994, F121994)
# (2) Countries less gas-flare shapefile (countries_nogas.shp)
# (3) China Roads (a2010_final_proj)

# Output files
# (1) lXX.dbf file for each year 19XX containing (i) grid cell ID, (ii) average light DN and area etc.
# (2) china_grid.shp with coordinates of nearest road (can get centroids using shp2dta later)

# Variables
ctryg = "countries_nogas"
road = "a2010_final_proj"

print "Cleaning lights data." 
try:

# Avg any years for which we have two satellites (F101994 and F121994 in this case)  
    inRaster1 = "F101994"
    inRaster2 = "F121994"
    outRaster = (Float(inRaster1)+Float(inRaster2))/2
    outRaster.save("FXX1994")
    print "Done averaging rasters"
    
# Delete old 1994 files
    arcpy.Delete_management("F101994")
    arcpy.Delete_management("F121994")

# Get China less gas flares polygon
    arcpy.Select_analysis(ctryg, "china1.shp", "\"NAME\" = 'China'")

# Use buffer tool and roads to make polygon of China close to roads, then clip china1 to this
# Process: Buffer
    arcpy.Buffer_analysis(road, "roadbuff.shp", "0.5 DecimalDegrees", "FULL", "ROUND", "ALL", "")
# Process: Clip
    arcpy.Clip_analysis("H:/Research/Data/Lights/china1.shp", "H:/Research/Data/Lights/roadbuff.shp", "china2.shp", "")
    print "china2 polygon ready to clip to"

# Clip each lights raster to extent of china2
    rasterList = arcpy.ListRasters("F*")
    for raster in rasterList:
        arcpy.Clip_management(raster, "-179.9999999999 -90.0000000187858 180.0000000001 83.6274185353372",
                              "G"+str(raster[1:]), "H:/Research/Data/Lights/china2.shp", "", "ClippingGeometry")
        print raster + " clipped"

    arcpy.Delete_management("H:/Research/Data/Lights/china1.shp")
    arcpy.Delete_management("H:/Research/Data/Lights/china2.shp")
    arcpy.Delete_management("H:/Research/Data/Lights/roadbuff.shp")

# Create grid to extent of one of new light rasters
    arcpy.CreateFishnet_management("ch_grid.shp", "73.55416565245 18.15416689405", "73.55416565245 28.15416689405",
                                   "0.1", "0.1", "0", "0", "134.77916540755 53.56250008575", "NO_LABELS", "G101992", "POLYGON")
    print "Got grid"
# Process: Raster to Polygon
    arcpy.RasterToPolygon_conversion("G101992", "G101992p.shp", "NO_SIMPLIFY", "Value")
# Process: Clip grid to perimeter of polygon
    arcpy.Clip_analysis("H:/Research/Data/Lights/ch_grid.shp", "H:/Research/Data/Lights/G101992p.shp", "china_grid.shp", "")

# Zonal statistics on each year (plus delete intermediate files)
    rasterList = arcpy.ListRasters("G*")
    for raster in rasterList:
        arcpy.gp.ZonalStatisticsAsTable_sa("H:/Research/Data/Lights/china_grid.shp", "FID", raster, "l"+str(raster[5:])+".dbf", "DATA", "MEAN")
        arcpy.Delete_management(raster)
        print "Got zonal stats for " + str(raster[5:])

    arcpy.Delete_management("H:/Research/Data/Lights/ch_grid.shp")
    arcpy.Delete_management("H:/Research/Data/Lights/G101992p.shp")

    print "Calculating nearest roads." 
# Process: Near
    arcpy.Near_analysis("H:/Research/Data/Lights/china_grid.shp", road, "", "LOCATION", "NO_ANGLE")
    print "Found nearest roads"

except:
    print arcpy.GetMessages()

# Check in the Spatial Analyst extension now that you're done
arcpy.CheckInExtension("Spatial")

## Finish ##
print "Job done."
del arcpy
