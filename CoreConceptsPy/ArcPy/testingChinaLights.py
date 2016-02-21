__author__ = ""
__date__ = ""
__status__ = ""


from coreConcepts.coreconcepts import * # TODO: Refactor so user just imports coreconcepts package

# TODO: determine how to chain following methods when different objects return (syntax adjustment?)

# create fields & objects from file path
china_boundary = makeObject("C:\Users\lafia\Desktop\chinalights_data\China.shp")
china_lights_1 = makeField("C:\Users\lafia\Desktop\chinalights_data\F101994.tif")
china_lights_1.restrict_domain(china_boundary, 'inside')
china_lights_2 = makeField("C:\Users\lafia\Desktop\chinalights_data\F121994.tif")
china_lights_2.restrict_domain(china_boundary, 'inside')
gas_flares = makeField('C:\Users\lafia\Desktop\chinalights_data\china_flares.shp') #test creation

# average fields
average_luminosity = china_lights_1.local(china_lights_2, 'average')

# # TODO: finish backend computation for the following procedures (as written in paper)
# # remove gas flares
# luminosity.restrict_domain(gas_flares, 'outside')
#
# # create roads buffer
# roads = makeObject('data/china_roads.shp')
# roads_buffered = buffer(roads, 0.5)
#
# # restrict domain of luminosity to road buffer
# luminosity_around_roads = luminosity.restrict_domain(roads_buffered, 'inside')
#
# # aggregate previous information
# results = luminosity_around_roads.coarsen(0.1, 0.1)