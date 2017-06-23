"""
An implementation for the core concept location for astronomic spaces
:author: Fenja Kollasch, 06/2017
"""

from coreconcepts import CcLocation
from astropy.coordinates import SkyCoord
from astropy.coordinates import EarthLocation
from astropy.coordinates import ICRS
from astropy.coordinates import AltAz
from astropy.coordinates import BarycentricTrueEcliptic
from astropy.coordinates import Galactic
from astropy.time import Time
from astropy import units as u
from enum import Enum
import math as m


# Types for location

class CRS(Enum):
    """
    Celestial Reference Systems
    """
    # International celestial reference system. Equivalent to equatorial coordinates
    ICRS = ('icrs', 'sosy barycenter')
    # Horizontal coordinates. Relative to observer. Often used for observation
    HORIZONTAL = ('altaz', 'observer')
    # Ecliptic coordinates. Used for objects orbiting the sun
    ECLIPTIC = ('barycentrictrueecliptic', 'sosy barycenter')
    # Galactic coordinates
    GALACTIC = ('galactic', 'sun')

    def __init__(self, sys, anchor):
        self.sys = sys
        self.anchor = anchor

    @staticmethod
    def get_by_sys(sys):
        if sys == 'icrs' or isinstance(sys, ICRS):
            return CRS.ICRS
        elif sys == 'altaz' or isinstance(sys, AltAz):
            return CRS.HORIZONTAL
        elif sys == 'barycentrictrueecliptic' or isinstance(sys, BarycentricTrueEcliptic):
            return CRS.ECLIPTIC
        elif sys == 'galactic' or isinstance(sys, Galactic):
            return CRS.GALACTIC
        else:
            raise ValueError("System {0} not supported".format(sys))


REFPOINTS = {'observer': 'altaz', 'earth': 'altaz', 'sosy barycenter': 'icrs',
             'sun': 'ecliptic', 'galactic center': 'galactic'}


class SphericalCoord(CcLocation):
    """
    A spherical pair of coordinates specified by a reference frame
    """

    def __init__(self, **args):
        """
        Wrapping up SkyCoord in a spherical or unitspherical representation
        :param args: Arguments forming the SkyCoord. Must have at least a longitude,
         a latitude and a frame, or a Skycoord-Object
        """
        self.representation = 'spherical'
        self.__args = args
        # Pop the additional info not related to AstroPy out and save them as attributes
        # Apparent magnitude minus absolute magnitude. Type: Float
        self.distance_module = args.pop('distance_module', None)
        # Parallax as visible from earth. Type: Float
        self.parallax = args.pop('parallax', None)

        # Observer's position on earth.
        self.observer = args.pop('observer', None)
        if self.observer:
            self.__observer = EarthLocation(lon=self.observer[1] * u.deg, lat=self.observer[0] * u.deg,
                                            height=self.observer[2] * u.m)
        # Time this position was observed, depending on the observer's time zone
        self.time = args.pop('time', None)
        if self.time:
            offset = int(self.observer[0] / 15) * u.hour
            self.__time = Time(self.time) - offset

        if 'skycoord' in args:
            self.__coord = args['skycoord']
        else:
            try:
                lon = args.pop('lon')
                lat = args.pop('lat')
                frame = args.pop('frame')
                if frame == 'altaz':
                    self.__coord = self.__create_horizontal(lon, lat, **args)
                else:
                    self.__coord = self.__create_skycoord(lon, lat, frame, **args)
            except KeyError:
                raise LocationError("A 2d Position needs a longitude, a latitude and a reference system.")

    @property
    def lon(self):
        return switch_frame(self.frame, lambda c: c.ra.value, lambda c: c.az.value, lambda c: c.lon.value,
                            lambda c: c.l.value, self.__coord)

    @property
    def lat(self):
        return switch_frame(self.frame, lambda c: c.dec.value, lambda c: c.alt.value, lambda c: c.lat.value,
                            lambda c: c.b.value, self.__coord)

    @property
    def frame(self):
        return CRS.get_by_sys(self.__coord.frame)

    def __eq__(self, other):
        return other.lon == self.lon and other.lat == self.lat and other.frame == self.frame

    def __hash__(self):
        return hash(self.frame) + hash(self.lon + self.lat)

    def __create_skycoord(self, lon, lat, frame, **args):
        try:
            distance = args.pop('distance', distance_to_refpoint(self, CRS.get_by_sys(frame).anchor))
            return SkyCoord(((lon + 360) % 360) * u.deg, lat * u.deg, frame=frame,
                            representation="spherical", distance=distance * u.pc, **args)
        except ValueError:
            return SkyCoord(((lon + 360) % 360) * u.deg, lat * u.deg, frame=frame,
                            representation="unitspherical")

    def __create_horizontal(self, lon, lat, **args):
        if not self.__observer or not self.__time:
            raise ValueError("A horizontal representation needs an observer's location and an observation time.")
        args['location'] = self.__observer
        args['obstime'] = self.__time
        return self.__create_skycoord(lon, lat, 'altaz', **args)

    def distance(self, ground=None):
        if not ground:
            try:
                return self.__coord.distance
            except AttributeError:
                return 1
        if ground in REFPOINTS:
            return distance_to_refpoint(self, ground)
        if ground.representation == 'extend':
            return ground.distance(self)
        if ground.representation != self.representation:
            return translate(self, ground.representation).distance(ground)
        else:
            return self.__coord.separation(ground.__coord)

    def is_at(self, ground):
        try:
            self.change_frame(ground.frame)
            return self.lon == ground.lon and self.lat == ground.lat
        except ValueError:
            return False

    def is_in(self, ground):
        return self.__coord.get_constellation() == ground.constellation

    def is_part(self, ground):
        try:
            return self in ground.members
        except AttributeError:
            return False

    def is_neighbor(self, ground):
        try:
            return self.neighborhood == ground.neighborhood
        except AttributeError:
            return False

    def change_frame(self, frame):
        """
        Changes the reference frame to the given one
        :param frame: A new reference frame
        :return: 
        """
        if frame == 'altaz':
            try:
                self.__coord = self.__coord.transform_to(AltAz(location=self.__observer, obstime=self.__time))
            except AttributeError:
                raise LocationError("A horizontal representation needs an observer location and a time.")
        elif frame in ['icrs', 'barycentrictrueecliptic', 'galactic']:
            self.__coord.transform_to(frame)
        else:
            raise LocationError("The frame {0} is currently not supported".format(frame))

    def make_extend(self, a, b, c):
        if self.__coord.representation == 'spherical':
            return AstroExtent(self, a, b, c)
        else:
            raise LocationError("A distance is necessary to extend a 2dPosition.")

    def voronoi_set(self, points):
        """
        Calculate the voronoi space of this location
        :param points: A set of points
        :return: The voronoi space based on a set of points
        """
        voronoi = []
        for p in points:
            nearest = True
            for q in (points - p):
                if p.distance(self) > p.distance(q):
                    nearest = False
                    break
            if nearest:
                voronoi.append(p)

        return AstroExtent(self, voronoi)

    def translate_to_cartesian(self):
        self.__coord.representation = 'cartesian'
        return CartesianCoord(skycoord=self.__coord)

    def translate_to_distance(self):
        if self.__coord.representation == 'unitspherical':
            raise LocationError("No distance available.")
        else:
            return Distance(self.__coord.distance, self.frame.anchor, **self.__args)


class CartesianCoord(CcLocation):

    def __init__(self, **args):
        """
        AstroPosition in three dimensional cartesian coordinates
        :param args: Arguments for coordinate creation. Contains at least x,y,z and 
        an origin which is either a reference point or coordinates
        """
        self.representation = 'cartesian'
        self.__args = args
        if 'skycoord' in args:
            self.__coord = args['skycoord']
        else:
            try:
                x = args.pop('x')
                y = args.pop('y')
                z = args.pop('z')
                origin = args.pop('origin')
                if origin in REFPOINTS:
                    self.__coord = SkyCoord(x, y, z, representation='cartesian', frame=REFPOINTS[origin], **args)
                else:
                    self.__coord = SkyCoord(x - self.origin.__coord.x, y - self.origin.__coord.y,
                                            z - self.origin.__coord.z, frame=origin.__coord.frame,
                                            representation='cartesian', **args)
                self.origin = origin
            except KeyError:
                raise LocationError("A 3d position needs at least three coordinates and an origin")

    @property
    def x(self):
        return self.__coord.x + self.origin.__coord.x

    @property
    def y(self):
        return self.__coord.y + self.origin.__coord.y

    @property
    def z(self):
        return self.__coord.z + self.origin.__coord.z

    def distance(self, ground=None):
        if not ground:
            try:
                return self.__coord.separation_3d(self.origin)
            except AttributeError:
                return 1
        if ground.representation == 'extend':
            return ground.distance(self)
        if ground.representation != self.representation:
            return translate(self, ground.representation).distance(ground)
        else:
            return self.__coord.separation_3d(ground.__coord)

    def is_at(self, ground):
        if ground.representation == 'extend':
            return ground.is_at(self)
        try:
            if self.origin != ground.origin:
                self.change_origin(ground.origin)
            return self.x == ground.x and self.y == ground.y and self.z == ground.z
        except AttributeError:
            return False

    def is_in(self, ground):
        try:
            self.change_origin(ground.footprint)
            if ((self.x / ground.a) ** 2 + (self.y / ground.b) ** 2 + (self.z / ground.c) ** 2) <= 1:
                return True
            for subspace in ground.members:
                if self.is_in(subspace):
                    return True
            return False
        except AttributeError:
            return False

    def is_part(self, ground):
        try:
            return self in ground.members
        except AttributeError:
            return False

    def is_neighbor(self, ground):
        try:
            return self.neighborhood == ground.neighborhood
        except AttributeError:
            return False

    def change_origin(self, origin):
        if origin in REFPOINTS:
            self.__coord.transform_to(REFPOINTS[origin])
            self.origin = origin
        else:
            self.__coord.transform_to(origin.__coord.frame)
            self.__coord = SkyCoord(self.__coord.x - origin.__coord.x, self.__coord.y - origin.__coord.y,
                                    self.__coord.z - origin.__coord.z, frame=origin.__coord.frame,
                                    representation='cartesian', **self.__args)
            self.origin = origin

    def make_extend(self, a, b, c):
        return AstroExtent(self, a, b, c)

    def translate_to_spherical(self):
        self.__coord.representation = 'spherical'
        return SphericalCoord(skycoord=self.__coord)

    def translate_to_distance(self):
        if self.__coord.representation == 'unitspherical':
            raise LocationError("No distance available.")
        else:
            return Distance(self.__coord.distance, self.origin, **self.__args)


class Distance(CcLocation):
    def __init__(self, distance, reference, **args):
        """
        A location described by the distance to a reference object
        """
        self.representation = 'distance'
        self.distance = distance
        self.reference = reference
        self.__args = args
        for arg in args:
            self.__setattr__(arg, args[arg])

    def __lt__(self, other):
        return self.distance < other.distance

    def __le__(self, other):
        return self.distance <= other.distance

    def __eq__(self, other):
        return self.distance == other.distance and self.reference == other.reference

    def __ge__(self, other):
        return self.distance >= other.distance

    def __gt__(self, other):
        return self.distance > other.distance

    def __hash__(self):
        return hash(self.reference + str(self.distance))

    def __str__(self):
        return "{a} kpc from {b} away".format(a=self.distance, b=self.reference)

    def distance(self, ground=None):
        if not ground or ground == self.reference:
            return self.distance
        try:
            # If possible, calculate spherical distance with harvesine formular
            phi = 2*self.distance * m.asin(m.sqrt(m.sin((ground.lat - self.lat)/2)**2 +
                                                  m.cos(self.lat) * m.cos(ground.lat) *
                                                  m.sin((ground.lon - self.lon)/2)**2))
            d = ground.distance(self.reference)
            # Then use pythagoras to get the distance between the objects
            return m.sqrt(self.distance**2 + d**2 - 2 * self.distance * d * m.cos(phi))
        except AttributeError:
            raise LocationError("The distance between these two locations can't be computed.")

    def is_at(self, ground):
        if ground.representation == 'distance':
            return self.distance == ground.distance
        return False

    def is_in(self, ground):
        if ground.representation == 'distance':
            return self.distance <= ground.distance
        try:
            self.distance <= ground.half_axis
        except AttributeError:
            return False

    def is_part(self, ground):
        try:
            return self in ground.members
        except AttributeError:
            return False

    def make_extend(self, a, b):
        try:
            return AstroExtent(self.reference, self.distance, a, b)
        except AttributeError:
            raise LocationError("Can't make an extend from this distance. There are no coordinates for the footprint.")

    def is_neighbor(self, ground):
        try:
            return self.neighborhood == ground.neighborhood
        except AttributeError:
            return False

    def translate_to_spherical(self):
        try:
            return SphericalCoord(**self.__args)
        except LocationError:
            raise LocationError("The distance holds not enough arguments to create a 2d position")

    def translate_to_cartesian(self):
        try:
            return CartesianCoord(**self.__args)
        except LocationError:
            raise LocationError("The distance holds not enough arguments to create a 3d position")


class AstroExtent(CcLocation):

    def __init__(self, footprint, members=[], constellation=None,  a=0, b=0, c=0):
        """
        An area based on a three dimensional footprint position
        Can include other locations.
        May be bounded (usually as an ellipsoid space)
        :param footprint: Footprint position. Can be any kind of location except distance
        :param members: Other locations that are part of this location
        :param constellation: The boundary of this extend is defined by this constellation
        :param a: radius 1
        :param b: radius 2
        :param c: radius 3
        """
        self.representation = 'extend'
        self.footprint = footprint
        self.members = members
        self.constellation = constellation
        self.a = a
        self.b = b
        self.c = c

    @property
    def half_axis(self):
        if self.a >= self.b and self.a >= self.c:
            return self.a
        elif self.b >= self.a and self.b >= self.c:
            return self.b
        else:
            return self.c

    def add_member(self, member):
        self.members.append(member)
        member.neighborhood = self

    def distance(self, ground):
        return self.footprint.distance(ground)

    def is_at(self, ground):
        return self.footprint.is_at(ground)

    def is_in(self, ground):
        return self.footprint.is_in(ground)

    def is_part(self, ground):
        try:
            return self in ground.members
        except AttributeError:
            return False

    def is_neighbor(self, ground):
        try:
            return self.neighborhood == ground.neighborhood
        except AttributeError:
            return False

    def distance_to_refpoint(self, refpoint):
        return self.footprint.distance_to_refpoint(refpoint)


# Module functions for location


def locate(relation, ground, figure, **args):
    """
    Locate an object relative to another phenomena
    :param relation: The relation that indicates the location
    :param ground: The phenomena that is used to ground the object
    :param figure: The object that is being located
    :param args: Additional information about the location
    :return: A location such as a coordinate, a distance or an extent
    """
    # Todo: Not yet generic enough
    if relation == 'ccs':
        return SphericalCoord(lon=float(figure.property('lon')), lat=float(figure.property('lat')),
                              frame=ground, **args)
    elif relation == 'cartesian':
        return CartesianCoord(x=float(figure.property('x')), y=float(figure.property('y')),
                              z=float(figure.property('z')), origin=ground, **args)
    elif relation == 'distance':
        return Distance(figure.distance, ground, **args)
    elif relation == 'extend':
        try:
            members = figure.property('members')
        except AttributeError:
            members = []
        try:
            constellation = figure.property('constellation')
        except AttributeError:
            constellation = []
        return AstroExtent(ground, members=members, constellation=constellation)
    else:
        raise LocationError("The relation '{0}' is currently not supported.".format(relation))


def resolve(relation, figure, ground):
    """
    Resolves the given relation between two locations.
    :param relation: The relation that needs to be resolved.
    :param figure: The first location
    :param ground: Another location
    :return: The result of the relation between them
    """
    if callable(relation):
        return relation(figure, ground)
    elif relation == 'distance':
        return figure.distance(ground)
    elif relation == 'is_at':
        return figure.is_at(ground)
    elif relation == 'is_in':
        return figure.is_in(ground)
    elif relation == 'is_part':
        return figure.is_part(ground)
    elif relation == 'is_neighbor':
        return figure.is_neighbor(ground)
    else:
        return LocationError("The relation {0} is currently not supported".format(relation))


def translate(location, representation):
    """
    Translate the given location into an other representation
    :param location: A location
    :param representation: The new representation
    :return: The translated location
    """
    if location.representation == representation:
        return location
    if representation == "spherical":
        return location.translate_to_spherical()
    elif representation == "cartesian":
        return location.translate_to_cartesian()
    elif representation == "distance":
        return location.translate_to_distance()
    elif representation == "extend":
        raise LocationError("No instant transformation into extend. Use make_extend instead.")
    else:
        raise LocationError("The representation '{0}' is currently not supported.".format(representation))


def distance_to_refpoint(location, refpoint):
    """
    Calculates the distance to common astronomic reference points
    :param location: The location
    :param refpoint: The reference point
    :return: the distance in parsec
    """
    # Todo: Just rudimentary implemented. Not 100% correct yet
    return switch_refpoint(refpoint, distance_to_earth, distance_to_earth,
                           distance_to_sun, distance_to_sun, distance_to_sun, location)


def distance_to_earth(location):
    """
    Calculates the distance to earth
    :param location: The location
    :return: Distance to earth in parsec
    """
    try:
        if location.distance_module is not None:
            return 10 ** ((location.distance_module + 5) / 5)
        elif location.parallax is not None:
            return 1 / location.parallax
        else:
            raise ValueError("There is no way to find out the distance to earth for this location.")
    except AttributeError:
        raise ValueError("There is no way to find out the distance to earth for this location.")


def distance_to_sun(location):
    """
    Calculates the distance to the sun
    :param location: The location
    :return: Distance to sun in parsec
    """
    return m.sqrt(0.000004848 ** 2 + distance_to_earth(location) ** 2)


def switch_frame(frame, f_icrs, f_hor, f_ecl, f_gal, *params):
    """
    Differ between the reference frames
    :param frame: The reference frame that is switched
    :param f_icrs: Transformation function for ICRS
    :param f_hor: Transformation function for horizontal frame
    :param f_ecl: Transformation function for ecliptic frame
    :param f_gal: Transformation function for galactic frame
    :param params: Parameters for the functions
    :return: The expected value returned by the functions depending on the reference frame
    """
    if frame == CRS.ICRS:
        return f_icrs(*params)
    elif frame == CRS.HORIZONTAL:
        return f_hor(*params)
    elif frame == CRS.ECLIPTIC:
        return f_ecl(*params)
    elif frame == CRS.GALACTIC:
        return f_gal(*params)
    else:
        raise LocationError("The reference frame {0} is currently not supported. I'm sorry".format(frame))


def switch_refpoint(refpoint, f_obs, f_earth, f_bar, f_sun, f_gal, *params):
    if refpoint == 'observer':
        return f_obs(*params)
    elif refpoint == 'earth':
        return f_earth(*params)
    elif refpoint == 'sosy barycenter':
        return f_bar(*params)
    elif refpoint == 'sun':
        return f_sun(*params)
    elif refpoint == 'galactic center':
        return f_gal(*params)
    else:
        raise ValueError("Unknown reference point: {0}".format(refpoint))


"""
Exceptions
"""


class LocationError(Exception):
    def __init__(self, message):
        super(LocationError, self).__init__(message)
