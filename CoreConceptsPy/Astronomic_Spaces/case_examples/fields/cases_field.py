"""
Some cases for the core concept 'field' in astronomy.
Data based on the observations and calculations of Brand and Blitz about the velocity field of the galaxy
http://cdsarc.u-strasbg.fr/viz-bin/Cat?J/A%2bA/275/67
:author: Fenja Kollasch, 06/2017
"""
import csv
import math as m
from fields import AstroField
from locations import Distance

# Parse data file
velo_map = dict()

with open("velocity_field.csv") as file:
    reader = csv.DictReader(file)
    for row in reader:
        galactic_distance = (float(row['dist'])**2 * m.cos(float(row['glat']))**2 + 8.5**2 - 2*8.5 * float(row['dist'])
                             * m.cos(float(row['glat'])) * m.cos(float(row['glon'])))**0.5
        pos = Distance(galactic_distance, 'galactic center', lon=float(row['glon']), lat=float(row['glat']))
        velo_map[pos] = float(row['Vlsr'])

r_sun = 8.5
theta_sun = 220


# Interpolation based on the Chi Square fitting routine
velocity_galaxy = AstroField(lambda d, p: ((1.00767 * (((p.distance/r_sun)**0.0394 + 0.00712) * theta_sun)
                                                    * r_sun)/p.distance - theta_sun) * m.sin(p.lon) * m.cos(p.lat),
                             velo_map.keys(), data=velo_map)
# Mask problem areas
velocity_galaxy.mask(lambda x: (30 < x.lon < 150 or 210 < x.lon < 330) and x.distance >= 1)

# Calculate circular velocities for every cell position
rotation_curve = velocity_galaxy.local(lambda v, p: (v/(m.sin(p.lon)*m.cos(p.lat)) + theta_sun) * p.distance/r_sun)

print("The rotation velocity in a distance of 20kpc from the galactic center is: {0}.".format(
    rotation_curve.value_at(Distance(20, 'galactic center', lon=90, lat=90))))

print(rotation_curve)
