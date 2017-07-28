"""
This case study is about the Supernova SN 2011fe that happened on August 24, 2011 in the pinwheel galaxy
We model this event and all participants with the core concepts and ask spatial questions about them
Every content concept is included

:author: Fenja Kollasch
:date: June 2017
"""
from objects import AstroObject
from networks import AstroNetwork
from fields import AstroField
from events import AstroEvent
from events import AstroTime
from locations import SphericalCoord
from locations import Distance

###########################################################################################
# The big dipper as the constellation in which the sn happened. Modeled as a network      #
###########################################################################################
big_dipper = AstroNetwork("big dipper", constellation='Ursa Major', bounding='extend',
                          reference=SphericalCoord(lon=169.96, lat=60.8175, frame='icrs'))

# Stars of the big dipper
alkaid = AstroObject("alkaid", lon=206.27, lat=49.18, bounding='ccs', reference='icrs')
mizar = AstroObject("mizar", lon=200.75, lat=54.55, bounding='ccs', reference='icrs')
alioth = AstroObject("alioth", lon=193.5, lat=55.57, bounding='ccs', reference='icrs')
megrez = AstroObject("megrez", lon=183.75, lat=57.01, bounding='ccs', reference='icrs')
phecda = AstroObject("phecda", lon=178.25, lat=53.41, bounding='ccs', reference='icrs')
merak = AstroObject("merak", lon=165.25, lat=56.22, bounding='ccs', reference='icrs')
dubhe = AstroObject("dubhe", lon=165.75, lat=61.41, bounding='ccs', reference='icrs')

big_dipper.addNodes([alkaid, mizar, alioth, megrez, phecda, merak, dubhe])

# Connections between the stars
big_dipper.addEdge(alkaid, mizar, distance=alkaid.relation(mizar, 'distance'))
big_dipper.addEdge(mizar, alioth, distance=mizar.relation(alioth, 'distance'))
big_dipper.addEdge(alioth, megrez, distance=alioth.relation(megrez, 'distance'))
big_dipper.addEdge(megrez, dubhe, distance=megrez.relation(dubhe, 'distance'))
big_dipper.addEdge(megrez, phecda, distance=megrez.relation(phecda, 'distance'))
big_dipper.addEdge(phecda, merak, distance=phecda.relation(merak, 'distance'))
big_dipper.addEdge(merak, dubhe, distance=merak.relation(dubhe, 'distance'))

###########################################################################################
# The pinwheel galaxy and the double star system that caused the sn.                      #
# Double star system modeled as network, pinwheel galaxy as object with extended location #
###########################################################################################
white_dwarf_system = AstroNetwork("2011fe Double Star System", lon=210.75, lat=54.16, bounding='ccs', reference='icrs')
dwarf = AstroObject("2011fe Dwarf")
companion = AstroObject("2011fe Companion")
white_dwarf_system.addNodes([dwarf, companion])
white_dwarf_system.addEdge(companion, dwarf, relation="feeding")

# Pinwheel galaxy (containing the white dwarf system
m101 = AstroObject("Pinwheel Galaxy", distance=6400000, bounding='extend',
                   reference=SphericalCoord(lon=210.8025, lat=54.349, frame='icrs'),
                   members=[white_dwarf_system.bounds()])

###########################################################################################
# The Supernova event itself and the radiant field it is emitting                         #
# Uses therefore the concepts event and field                                             #
###########################################################################################

# Radio emission field, dependent on the distance to the progenitor
radio_emission = AstroField(lambda r: (10.0/13.0)**3.86 * 10**11 *
                                      (0.16 * (10.0/13.0) * (r.distance*3.086*10**13)/(5*10**4))**-3.42
                            * 0.1**1.07 * (3.00*10**9) * 0.32**((1.93*13-8.43)/13),
                            domain=Distance(1, white_dwarf_system.bounds()))


# Model Supernova as an extension from normal Astronomic events (can do this for the other cases as well)
class SnIa(AstroEvent):
    def __init__(self, id, start, progenitor, radio_emission):
        # Fitted by Zheng et al, 2017
        self.progenitor = progenitor
        self.lightcurve = lambda t: (t.value()/19.5)**2.1 * (1 + (t.value()/19.5)**(1.57 * (2.1 + 2.19)))**(-2 / 1.57)

        participants = {progenitor: self.__change_progenitor, radio_emission: self.__change_radio_emission}

        super(SnIa, self).__init__(id, participants, start=start)

    def __change_progenitor(self, p, t):
        lum = self.lightcurve(t - self.start)
        p.set_property('visual_magnitude', lum)
        return p

    def __change_radio_emission(self, e, time):
        t = (time.value() - self.start.value()) * 86400
        field = e.local(lambda l: l * (1 / t) ** -3.42 * t ** ((2.86 * 13 - 25.3) / 13.0))
        field.domain = Distance((t ** (10 / 13) * 10), self.progenitor.bounds())
        return field

# Instance of the event
sn = SnIa("SN 2011fe", AstroTime(55796.687, 2400000, 'jd'), white_dwarf_system, radio_emission)

###########################################################################################
# Now ask spatial questions about the event and its participants                          #
###########################################################################################

# Was the star system that caused the supernova part of the Pinwheel Galaxy?
part_of_m101 = white_dwarf_system.relation(m101, 'is_part')

# Is the Pinwheel Galaxy within the constellation Big Dipper? Which star of the big dipper is closest?
within_dipper = m101.relation(big_dipper, 'is_in')
nearest_star = big_dipper.nearest_node(m101)

# When did the supernova started?
start = sn.start.time

# How bright is the remnant of SN 2011fe at October 31, 2011?
brightness_prog = sn.status(white_dwarf_system, AstroTime("2011-10-31 23:00:00")).property('visual_magnitude')

# How strong is the radio emission at a radius of 0.5pc at October 31, 2011?
re = sn.status(radio_emission, AstroTime("2011-10-31 23:00:00")).value_at(Distance(0.5, white_dwarf_system.bounds()))


#######################################################################################################################
# Printing the results
print("Was the star system that caused the supernova part of the Pinwheel Galaxy?")
if part_of_m101:
    print("- Yes, it was.")
else:
    print("- No, it wasn't")
print()
print("Is the Pinwheel Galaxy within the constellation Big Dipper? Which star of the big dipper is closest?")
if within_dipper:
    print("- Yes, it is. The closest star of the Big Dipper is {0}".format(nearest_star))
else:
    print("- No, it's not. The closest star of the Big Dipper is {0}".format(nearest_star))
print()
print("When did the supernova started?")
print("- It started on {0}".format(start))
print()
print("How bright is the progenitor of SN 2011fe at October 31, 2011?")
print("- {0}".format(brightness_prog))
print()
print("How strong is the radio emission at a radius of 0.5pc at October 31, 2011?")
print("- {0}".format(re))
