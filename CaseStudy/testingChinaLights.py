__author__ = ""
__date__ = ""
__status__ = ""

from coreconcepts import * # TODO: Package up Cc

china_boundary_filepath = r"C:\Users\lafia\Documents\GitHub\ConceptsOfSpatialInformation\CoreConceptsPy\ArcPy\data\China.shp"
china_lights_1_filepath = r"C:\Users\lafia\Documents\GitHub\ConceptsOfSpatialInformation\CoreConceptsPy\ArcPy\data\F101994.tif"
china_lights_2_filepath = r"C:\Users\lafia\Documents\GitHub\ConceptsOfSpatialInformation\CoreConceptsPy\ArcPy\data\F121994.tif"
gas_flares_filepath     = r"C:\Users\lafia\Documents\GitHub\ConceptsOfSpatialInformation\CoreConceptsPy\ArcPy\data\Flares_China_1.shp"
china_roads_filepath    = r"data/china_roads.shp"

# TODO: determine how to chain following methods when different objects return (syntax adjustment?)

# create fields & objects from file path
china_boundary = makeObject(china_boundary_filepath)
china_lights_1 = makeField(china_lights_1_filepath).restrict_domain(china_boundary, 'inside')
china_lights_2 = makeField(china_lights_2_filepath).restrict_domain(china_boundary, 'inside')
gas_flares = makeObject(gas_flares_filepath)

# average fields
average_luminosity = china_lights_1.local(china_lights_2, 'average')

# remove gas flares
luminosity = average_luminosity.restrict_domain(gas_flares, 'outside')

# create roads buffer
roads = makeObject(china_roads_filepath)
roads_buffered = roads.buffer(0.5, 'DecimalDegrees') # TODO: updated function calling convention (exclude object)

# restrict domain of luminosity to road buffer
luminosity_around_roads = luminosity.restrict_domain(roads_buffered, 'inside')

# aggregate previous information
results = luminosity_around_roads.coarsen(0.1, 0.1)
