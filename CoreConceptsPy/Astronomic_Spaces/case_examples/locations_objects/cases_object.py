"""
Some example cases for spatial questions in astronomy with objects
Data taken from the Vizier Sky catalogues
:author: Fenja Kollasch, 06/2017
"""

import csv
from objects import AstroObject
from objects import AstroObjectSet


# Model a cepheid as a specific AstroObject:
class Cepheid(AstroObject):

    def _calc_app_mag(self):
        if "F475W" not in self._data and "F814W" not in self._data:
            raise ValueError("Your data contains not enough bands for a proper estimation of the apparent magnitude.")

        # Wesenheit magnitude
        return float(self._data["F814W"]) - 0.879 * (float(self._data["F475W"]) - float(self._data["F814W"]))

    def _calc_distance_module(self):
        if "F160W" in self._data and "F110W" in self._data:
            m_inf = float(self._data["F160W"]) - 1.54 * (float(self._data["F110W"]) - float(self._data["F160W"]))
            return (super(Cepheid, self)._calc_distance_module() + (m_inf - self.property('abs_mag'))) / 2
        return super(Cepheid, self)._calc_distance_module()

# Read in catalogue
cepheids = AstroObjectSet()
with open("wk_cepheids.csv") as file:
    reader = csv.DictReader(file)
    id = 1
    for row in reader:
        obj = Cepheid("WKCeph " + str(id), **row)
        cepheids.add(obj)
        id += 1

# Case 1: Which cepheid around M31 is the brightest (apparent and absolute)?
print("Case 1: Which cepheid around M31 is the brightest (apparent and absolute)?")
brightest_app = None
brightest_abs = None
for cepheid in cepheids:
    if brightest_app is None or brightest_app.property('app_mag') > cepheid.property('app_mag'):
        brightest_app = cepheid
    if brightest_abs is None or brightest_abs.property('abs_mag') > cepheid.property('abs_mag'):
        brightest_abs = cepheid

print("{0.id} is the apparently brightest cepheid.".format(brightest_app))
print("{0.id} is the absolutely brightest cepheid.".format(brightest_abs))

# Case 2: How far are the cepheids away from earth (in average)?
print("Case 2: How far are the cepheids away from earth (in average)?")
dis_m31 = sum(c.relation("earth", "distance") for c in cepheids) / cepheids.len()
print("The cepheids are averagely {0} parsecs away. This is also estimately the distance to M31 ;)".format(dis_m31))
