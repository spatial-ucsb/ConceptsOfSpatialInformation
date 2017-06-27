from events import AstroEvent
from events import AstroTime
from objects import AstroObject
from networks import AstroNetwork
from fields import AstroField
from locations import Distance

"""
Case study: The impacts of Supernova 2011fe
Sources:
http://cdsarc.u-strasbg.fr/viz-bin/Cat?J/other/NewA/20.30
https://arxiv.org/pdf/1612.02097.pdf
https://arxiv.org/pdf/1705.04204.pdf

:author: Fenja Kollasch
:date: 06/02/2017
"""


class SnIa(AstroEvent):
    def __init__(self, id, start, progenitor, radio_emission):
        # Fitted by Zheng et al, 2017
        self.progenitor = progenitor
        self.lightcurve = lambda t: (t.value() / 19.5) ** 2.1 * (1 + (t.value() / 19.5) ** (1.57 * (2.1 + 2.19))) ** (
        -2 / 1.57)

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

# The white dwarf double star system that caused the supernova
white_dwarf_system = AstroNetwork("2011fe Double Star System", lon=210.75, lat=54.16, bounding='ccs', reference='icrs')
dwarf = AstroObject("2011fe Dwarf")
companion = AstroObject("2011fe Companion")
white_dwarf_system.addNode(dwarf)
white_dwarf_system.addNode(companion)
white_dwarf_system.addEdge(companion, dwarf, relation="feeding")


# Radio emission field, dependent on the distance to the progenitor
radio_emission = AstroField(lambda r: (10.0/13.0)**3.86 * 10**11 *
                                      (0.16 * (10.0/13.0) * (r.distance*3.086*10**13)/(5*10**4))**-3.42
                            * 0.1**1.07 * (3.00*10**9) * 0.32**((1.93*13-8.43)/13),
                            domain=Distance(1, white_dwarf_system.bounds()))


# The supernova event
sn = SnIa("SN 2011fe", AstroTime(55796.687, 2400000, 'jd'), white_dwarf_system, radio_emission)

# Now ask questions about the event and its participants
print("Brightness at October 31, 2011: {0}".format(
    sn.status(white_dwarf_system, AstroTime("2011-10-31 23:00:00")).property('visual_magnitude')))
print("Radio emission at a radius of 0.5pc at October 31, 2011: {0}".format(
    sn.status(radio_emission, AstroTime("2011-10-31 23:00:00")).value_at(Distance(0.5, white_dwarf_system.bounds()))))

