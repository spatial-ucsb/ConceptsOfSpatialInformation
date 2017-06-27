"""
In this file, we present a number of possible spatial questions in regard of locations
No serious data yet (copied from Wikipedia)

:author: Fenja Kollasch
"""
import sys
sys.path.append('../')
import locations as l

# Case 1: Where is Bellatrix seen from Sirius? Where is Bellatrix seen from Sirius in regard of the earth?
print("Where is Bellatrix seen from Sirius? Where is Bellatrix seen from Sirius in regard of the earth?")
bellatrix = l.SphericalCoord(lon=81.2828, lat=6.3497, frame='icrs', distance_module=(1.64-(-2.87)))
sirius = l.SphericalCoord(lon=101.2876, lat=-16.7161, frame='icrs', distance_module=(-1.47-1.42))
sirius_cart = l.translate(sirius, 'cartesian')
print("Bellatrix is {0} away from earth".format(bellatrix.distance()))
print("Bellatrix is {0} from Sirius away"
      .format(bellatrix.distance(sirius)))

print("Bellatrix is {0} from Sirius away, obtained from the earth"
      .format(bellatrix.distance(sirius_cart)))

print()

# Case 2: Can I see Vega from Santa Barbara this year at July 04, 11pm? Where?
print("Case 2: Can I see Vega from Santa Barbara this year at July 04, 11pm? Where?")
santa_barbara = [34.4208, 119.6982, 0]
vega = l.SphericalCoord(lon=279, lat=38.47, frame='icrs', distance_module=(0.026-0.582),
                        observer=santa_barbara, time='2017-7-04 23:00:00')
vega.change_frame('altaz')
if vega.lon < 0:
    print("Vega is not visible from Santa Barbara this year at July 04, 11pm")
else:
    print("Vega is visible at {0.lon}, {0.lat} from Santa Barbara this year at July 04, 11pm".format(vega))

