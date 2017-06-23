"""
Test if my location implementation shows correct results
:author: Fenja Kollasch, 06/2017
"""
import sys
sys.path.append('../')
import locations_depr as l

alpha_centauri = l.AstroPlace([219.75, -60.5], l.CRS.ICRS, representation="spherical", distance_module=(1.33 - 4.38))

sirius = l.AstroPlace([101.25, -16.42], distance_module=(-1.46-1.42))

prox_icrs = l.AstroPlace([217.25, -62.5], l.CRS.ICRS, representation='unitspherical', distance_module=11.13 - 15.60)
prox_ecl = l.AstroPlace([217.25, -62.5], l.CRS.ECLIPTIC, representation='spherical', distance_module=11.13 - 15.60)
prox_gal = l.AstroPlace([217.25, -62.5], l.CRS.GALACTIC, representation='spherical', distance_module=11.13 - 15.60)
prox_super = l.AstroPlace([217.25, -62.5], l.CRS.ICRS, representation='spherical', distance_module=11.13 - 15.60)
"""
print(prox_icrs)
print(prox_ecl)
print(prox_gal)
print(prox_super)
"""
print("Unitspherical: {0}".format(prox_icrs))
prox_icrs.to_cartesian_coords()
print("To cartesian: {0}".format(prox_icrs))
prox_icrs.to_spherical_coords()
print("To spherical: {0}".format(prox_icrs))
print("ICRS: {0}".format(prox_icrs))
prox_icrs.to_cartesian_coords()
print("ICRS cartesian: {0}".format(prox_icrs))
prox_icrs.to_spherical_coords()

prox_icrs.to_ecliptic()
print("Ecliptic: {0}".format(prox_icrs))
prox_icrs.to_cartesian_coords()
print("Ecliptic cartesian: {0}".format(prox_icrs))
prox_icrs.to_spherical_coords()

prox_icrs.to_galactic()
print("Galactic: {0}".format(prox_icrs))
prox_icrs.to_cartesian_coords()
print("Galactic cartesian: {0}".format(prox_icrs))
prox_icrs.to_spherical_coords()

prox_icrs.to_supergalactic()
print("Supergalactic: {0}".format(prox_icrs))
prox_icrs.to_icrs()
prox_icrs.to_cartesian_coords()
print("Supergalactic cartesian: {0}".format(prox_icrs))
prox_icrs.to_spherical_coords()

print("ICRS: {0}".format(prox_icrs))

dist_earth = l.AnAstroLocation('distance', 'earth')
prox_icrs.to_cartesian_coords()
distance_prox_earth = l.AstroLocation.resolve(dist_earth, prox_icrs)
distance_prox_sir_spherical = l.AstroLocation.resolve(l.AnAstroLocation('distance', sirius), prox_icrs)
sirius.to_cartesian_coords()
distance_prox_sir = l.AstroLocation.resolve(l.AnAstroLocation('distance', sirius), prox_icrs)


print("Proxima: Distance to earth: {0}".format(distance_prox_earth))
print(prox_icrs)
print("Sirius: Distance to earth {0}".format(l.AstroLocation.resolve(dist_earth, sirius)))
print(sirius)
print("Distance between Proxima Centauri and Sirius (in pc): {0}".format(distance_prox_sir))
print("Distance between proxima centauri and Sirius (in deg): {0}".format(distance_prox_sir_spherical))


ra = prox_icrs.ra
dec = prox_icrs.dec
lon = prox_icrs.lon_ecl
lat = prox_icrs.lat_ecl
l = prox_icrs.gl
b = prox_icrs.gb
sgl = prox_icrs.sgl
sgb = prox_icrs.sgb

prox_icrs.to_ecliptic()
try:
    assert round(lon, 5) == round(prox_icrs.lon, 5) and round(lat, 5) == round(prox_icrs.lat, 5)
except AssertionError:
    print('Assertion error: {l} bs {tl} and {b} vs {tb}'.format(l=lon, tl=prox_icrs.lon, b=lat, tb=prox_icrs.lat))
prox_icrs.to_galactic()
try:
    assert round(l, 5) == round(prox_icrs.lon, 5) and round(b, 5) == round(prox_icrs.lat, 5)
except AssertionError:
    print('Assertion error: {l} bs {tl} and {b} vs {tb}'.format(l=l, tl=prox_icrs.b, b=lat, tb=prox_icrs.lat))
prox_icrs.to_supergalactic()
try:
    assert round(sgl, 5) == round(prox_icrs.lon, 5) and round(sgb, 5) == round(prox_icrs.lat, 5)
except AssertionError:
    print('Assertion error: {l} bs {tl} and {b} vs {tb}'.format(l=sgl, tl=prox_icrs.lon, b=sgb, tb=prox_icrs.lat))
prox_icrs.to_icrs()
try:
    assert round(ra, 5) == round(prox_icrs.lon, 5) and round(dec, 5) == round(prox_icrs.lat, 5)
except AssertionError:
    print('Assertion error: {l} bs {tl} and {b} vs {tb}'.format(l=ra, tl=prox_icrs.lon, b=dec, tb=prox_icrs.lat))




