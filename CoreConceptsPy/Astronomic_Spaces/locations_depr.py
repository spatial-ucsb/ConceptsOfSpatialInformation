"""
Locations in astronomic spaces
Define a location as a tuple containing relation, figure and ground
"""
# Todo: Rigth now, the three classes are pretty redundant
# Todo: Maybe AstroPlace is already enough to serve as a location
import math as m
from coreconcepts import CcLocation
from astropy import units as u
from astropy.coordinates import SkyCoord, UnitSphericalRepresentation, SphericalRepresentation, \
    CartesianRepresentation, AltAz, EarthLocation
from astropy.time import Time
from enum import Enum


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
    # Supergalactic coordinates
    SUPERGALACTIC = ('supergalactic', 'galactic center')

    def __init__(self, sys, anchor):
        self.sys = sys
        self.anchor = anchor



class AstroLocation(CcLocation):
    """
    Location in its curried form
    Nothing more than a pure relation
    """

    @staticmethod
    def resolve(ground, figure):
        """
        Locate a figure by resolving the relation between figure and ground
        :param figure: What is located?
        :param ground: 'A location'. Provides a relation and a ground
        :return: A value that is locating the figure relative to the ground
        """
        # Is my ground already a relation?
        if callable(ground):
            return ground(figure)
        # Is my ground a CRS?
        if isinstance(ground, CRS):
            figure.transform_to(ground)
            return figure
        # Elseway the ground must be AnAstroLocation
        else:
            return ground.relation(figure)


class AnAstroLocation(object):
    """
    Location in its uncurried form
    Comes with a static set of functions for astronomic use
    """

    def __init__(self, relation, ground):
        """
        'A location' is a tuple of a relation and the ground where future figures should be related to   
        :param ground: Where is it located
                       If none, the reference system center is default
        :param relation: The relation linking ground and figure. Can be either a function or a string
        """

        self.ground = ground

        if relation == "where at":
            self.relation = self.__position
        if relation == 'distance':
            self.relation = self.__distance
        elif relation == 'is at':
            self.relation = self.__is_at
        elif relation == 'is in':
            self.relation = self.__is_in
        elif relation == 'part of':
            self.relation = self.__is_part
        elif relation == 'neighbors':
            self.relation = self.__same_sys
        else:
            raise ValueError("The relation you want to resolve is not predefined.")

    def __position(self, figure):
        if isinstance(self.ground, str):
            # Todo: Mapping not yet correct
            switch_refpoint(self.ground, figure.transform_to(CRS.HORIZONTAL), figure.transform_to(CRS.HORIZONTAL),
                            figure.transform_to(CRS.ICRS), figure.transform_to(CRS.ECLIPTIC),
                            figure.transform_to(CRS.GALACTIC))
            return figure
        else:
            figure.transform_to(self.ground)
            return figure.x - self.ground.x, figure.y - self.ground.y, figure.z - self.ground.z

    def __distance(self, figure):
        """
        Calculates the distance between figure and ground
        :param figure: What is located
        :return: The distance (either angular or decimal)
        """
        if isinstance(self.ground, str):
            return figure.distance_to_refpoint(self.ground)
        if self.ground.repr == 'cartesian':
            return self.ground.distance_cartesian(figure)
        else:
            return self.ground.distance_spherical(figure)

    def __is_at(self, figure):
        """
        Obtains, if the figure is at the ground
        :param figure: What is located
        :return: True, if figure is at the ground
        """
        try:
            figure.transform_to(self.ground.frame)
            if self.ground.repr == "cartesian":
                return figure.x == self.ground.x and figure.y == self.ground.y and figure.z == self.ground.z
            return figure.lon == self.ground.lon and figure.lat == self.ground.lat
        except AttributeError:
            raise LocationError("The operation 'is at' needs a figure and a ground with coordinates")

    def __is_in(self, figure):
        """
        Obtains, if the figure is in the ground's space
        :param figure: What is located
        :return: True, if figure is in the ground
        """
        try:
            figure.transform_to(self.ground.frame)
            figure.to_cartesian_coords()
            self.ground.to_cartesian_coords()
            x = figure.x - self.ground.x
            y = figure.y - self.ground.y
            z = figure.z - self.ground.z
            return ((x / self.ground.space.a) ** 2 + (y / self.ground.space.b) ** 2 +
                    (z / self.ground.space.c) ** 2) <= 1
        except AttributeError:
            raise LocationError("The operation 'is in' needs a figure with coordinates "
                                "and a ground with a spanned space.")

    def __is_part(self, figure):
        """
        Obtains, if the figure is orbiting the ground
        :param figure: What is located
        :return: True, if figure is orbiting the ground
        """
        # Todo
        raise NotImplementedError

    def __same_sys(self, figure):
        """
        Obtains, if figure and ground are orbiting the same object
        :param figure: What is located
        :return: True, they are orbiting the same object
        """
        # Todo
        raise NotImplementedError


class AstroPlace(object):
    """
    An abstract place in an astronomic space
    Can act as a ground or as 'a location'
    Necessarily has a position (footprint)
    """

    def __init__(self, position, frame=CRS.ICRS, **skycoordargs):
        """
        Describe a location with a variable frame of reference
        Basically just acting as a wrapper for AstroPy SkyCoords
        :param position: A list of coordinates. Unit and representation depends on the other parameters
        :param frame: The frame of reference. ICRS by default
        Currently supported frames: ICRS, horizontal, ecliptic, galactic, supergalactic 
        :param skycoordargs: Additional arguments which might be necessary for some operations
        """

        # Pop the additional info not related to AstroPy out and save them as attributes
        # Apparent magnitude minus absolute magnitude. Type: Float
        self.distance_module = skycoordargs.pop('distance_module', None)
        # Parallax as visible from earth. Type: Float
        self.parallax = skycoordargs.pop('parallax', None)
        # The orbit this location lays on. Type: Orbit Object
        self.orbit = skycoordargs.pop('orbit', None)
        # The space spanned by this location. Type: Space Object
        self.space = skycoordargs.pop('volume', None)

        representation = skycoordargs.pop('representation', 'unitspherical')

        # Use Astropy Representations for location and time
        self.obspos = skycoordargs.pop('location', None)  # Position as value list
        self.obstime = skycoordargs.pop('obstime', None)  # true observation time
        self.__observer = self.__set_observer()  # Position as Earth location
        self.__time = self.__set_time()  # Time object in UTC

        # Save the pure skycoordargs
        self.__skycoordargs = skycoordargs
        if isinstance(frame, CRS):
            self.frame = frame
        else :
            self.frame = parse_frame(frame)

        # Create a new SkyCoord depending on reference system
        if frame == CRS.ICRS or frame == CRS.ECLIPTIC or CRS.GALACTIC or CRS.SUPERGALACTIC:
            self.__coord = self.__create_coord(position, representation, skycoordargs)
        elif frame == CRS.HORIZONTAL:
            self.__coord = self.__create_horizontal_coord(position, representation, skycoordargs)
        else:
            raise FrameError("The reference frame {0} is currently not supported. I'm sorry".format(frame))

    def __create_coord(self, position, representation, args):
        """
        Creates a coordinate by a specific representation
        :param position: The data of the coordinates. Might be longitude and latitude or a 3D vector
        :param representation: The representation form
        :param args: Additional arguments
        """
        if len(position) < 2:
            raise CoordinateError("You need at least two coordinates")
        if representation == 'unitspherical':
            return self.__create_unitspherical_coord(position, args)
        elif representation == 'spherical':
            return self.__create_spherical_coord(position, args)
        elif representation == 'cartesian':
            return self.__create_cartesian_coord(position, args)
        else:
            raise RepresentationError("The representation {0} is not yet supported".format(self.repr))

    def __create_horizontal_coord(self, position, representation, args):
        """
        Creates a coordinate specified for a horizontal coordinate frame
        :param position: Longitude and latitude of this coordinate
        :param representation: Representation form. Must be spherical
        :param args: Additional arguments
        """
        if 'obstime' not in args or 'location' not in args:
            raise CoordinateError("A horizontal representation needs an observation time and a location")
        if representation != "spherical":
            raise CoordinateError("A horizontal representation needs a spherical representation")
        self.__create_coord(position, "spherical", args)

    def __create_unitspherical_coord(self, position, args):
        """
        Creates a coordinate in unitspherical representation
        """
        lon = position[0]
        lat = position[1]
        return SkyCoord((lon+360) % 360, lat, unit=u.deg, frame=self.frame.sys, representation="unitspherical", **args)

    def __create_spherical_coord(self, position, args):
        """
        Creates a coordinate in unitspherical representation
        """
        lon = position[0]
        lat = position[1]
        if 'distance' not in args:
            d = self.distance_to_refpoint(self.frame.anchor)
        else:
            d = args.pop('distance')
        return SkyCoord(((lon+360) % 360)*u.deg, lat*u.deg, frame=self.frame.sys, representation="spherical",
                        distance=d*u.pc, **args)

    def __create_cartesian_coord(self, position, args):
        """
        Creates a coordinate in cartesian representation
        """
        if len(position) < 3:
            raise CoordinateError("A cartesian position needs three coordinates.")
        x = position[0]
        y = position[1]
        z = position[2]
        return SkyCoord(x, y, z, unit=u.pc, frame=self.frame.sys, representation="cartesian", **args)

    def __set_observer(self):
        """
        Set the observer position as EarthLocation
        :return: Geodaetic representation of a place on earth
        """
        if self.obspos is None:
            return None
        if len(self.obspos) < 3:
            raise CoordinateError("A location on earth must be described with three values:"
                                  " Longitude, latitude and height")
        return EarthLocation(lon=self.obspos[1]*u.deg, lat=self.obspos[0]*u.deg, height=self.obspos[2]*u.m)

    def __set_time(self):
        """
        Set the time in UTC depending on the location
        We assume that the time string is in correct format
        :return: The time in UTC
        """
        if self.obstime is None or self.obspos is None:
            return None
        offset = int(self.obspos[0]/15) * u.hour
        return Time(self.obstime) - offset

    @property
    def repr(self):
        if self.__coord.representation == UnitSphericalRepresentation:
            return 'unitspherical'
        elif self.__coord.representation == SphericalRepresentation:
            return 'spherical'
        elif self.__coord.representation == CartesianRepresentation:
            return 'cartesian'
        else:
            raise RepresentationError("Representation {0} is not supported".format(self.__coord.representation))

    @property
    def lon(self):
        """
        Returns the longitude of this location given by the current reference frame
        Representation is automatically shifted to spherical, if called
        :return: The longitude in the current reference frame
        """
        if self.repr == 'cartesian':
            self.to_spherical_coords()
        return switch_frame(self.frame, lambda c: c.ra.value, lambda c: c.az.value, lambda c: c.lon.value,
                            lambda c: c.l.value, lambda c: c.sgl.value, self.__coord)

    @property
    def lat(self):
        """
        Returns the latitude of this location given by the current reference frame
        Representation is automatically shifted to spherical, if called
        :return: The latitude in the current reference frame
        """
        if self.repr == 'cartesian':
            self.to_spherical_coords()

        return switch_frame(self.frame, lambda c: c.dec.value, lambda c: c.alt.value, lambda c: c.lat.value,
                            lambda c: c.b.value, lambda c: c.sgb.value, self.__coord)

    @property
    def x(self):
        """
        Returns the x coordinate of this location
        Representation is automatically shifted to cartesian, if called
        :return: The x coordinate
        """
        if self.repr != 'cartesian':
            self.to_cartesian_coords()
        return self.__coord.x.value

    @property
    def y(self):
        """
        Returns the y coordinate of this location
        Representation is automatically shifted to cartesian, if called
        :return: The y coordinate
        """
        if self.repr != 'cartesian':
            self.to_cartesian_coords()
        return self.__coord.y.value

    @property
    def z(self):
        """
        Returns the z coordinate of this location
        Representation is automatically shifted to cartesian, if called
        :return: The z coordinate
        """
        if self.repr != 'cartesian':
            self.to_cartesian_coords()
        return self.__coord.z.value

    @property
    def ra(self):
        if self.repr == 'cartesian':
            self.to_spherical_coords()
        if self.frame == CRS.ICRS:
            return self.__coord.ra.value
        return self.__coord.icrs.ra.value

    @property
    def dec(self):
        if self.repr == 'cartesian':
            self.to_spherical_coords()
        if self.frame == CRS.ICRS:
            return self.__coord.dec.value
        return self.__coord.icrs.dec.value

    @property
    def lon_ecl(self):
        if self.repr == 'cartesian':
            self.to_spherical_coords()
        if self.frame == CRS.ECLIPTIC:
            return self.__coord.lon.value
        return self.__coord.barycentrictrueecliptic.lon.value

    @property
    def lat_ecl(self):
        if self.repr == 'cartesian':
            self.to_spherical_coords()
        if self.frame == CRS.ECLIPTIC:
            return self.__coord.lat.value
        return self.__coord.barycentrictrueecliptic.lat.value

    @property
    def gl(self):
        if self.repr == 'cartesian':
            self.to_spherical_coords()
        if self.frame == CRS.GALACTIC:
            return self.__coord.l.value
        return self.__coord.galactic.l.value

    @property
    def gb(self):
        if self.repr == 'cartesian':
            self.to_spherical_coords()
        if self.frame == CRS.GALACTIC:
            return self.__coord.b.value
        return self.__coord.galactic.b.value

    @property
    def sgl(self):
        if self.repr == 'cartesian':
            self.to_spherical_coords()
        if self.frame == CRS.SUPERGALACTIC:
            return self.__coord.sgl.value
        return self.__coord.supergalactic.sgl.value

    @property
    def sgb(self):
        if self.repr == 'cartesian':
            self.to_spherical_coords()
        if self.frame == CRS.SUPERGALACTIC:
            return self.__coord.sgb.value
        return self.__coord.supergalactic.sgb.value

    def __setattr__(self, key, value):
        if key == 'coord':
            raise CoordinateError("Don't change the SkyCoord. Trust me. It's not fun...")
        else:
            super(AstroPlace, self).__setattr__(key, value)

    def __str__(self):
        coord = str(self.__coord)
        # Additional arguments not captured in SkyCoord
        if self.distance_module is not None:
            coord += "\nDistance module: {0}".format(self.distance_module)
        if self.parallax is not None:
            coord += "\nDParallax: {0}".format(self.parallax)
        return coord

    """
    Transformation methods to shift reference frames and representations
    """
    def transform_to(self, frame):
        switch_frame(frame, self.to_icrs, self.to_horizontal, self.to_ecliptic,
                     self.to_galactic, self.to_supergalactic)

    def to_icrs(self):
        self.__coord = self.__coord.transform_to('icrs')
        self.frame = CRS.ICRS

    def to_ecliptic(self):
        self.__coord = self.__coord.transform_to('barycentrictrueecliptic')
        self.frame = CRS.ECLIPTIC

    def to_galactic(self):
        self.__coord = self.__coord.transform_to('galactic')
        self.frame = CRS.GALACTIC

    def to_supergalactic(self):
        self.__coord = self.__coord.transform_to('supergalactic')
        self.frame = CRS.SUPERGALACTIC

    def to_horizontal(self):
        if self.__observer is None or self.__time is None:
            raise FrameError("A horizontal representation needs an observer location and a time.")
        self.__coord = self.__coord.transform_to(AltAz(location=self.__observer, obstime=self.__time))
        self.frame = CRS.HORIZONTAL

    def to_spherical_coords(self):
        """
        Translates the coordinates into a spherical representation
        If coordinates are unitspherical, a distance calculation is necessary
        """
        if self.repr == 'spherical':
            return
        if self.repr == 'unitspherical':
            self.__coord = self.__create_spherical_coord([self.lon, self.lat], self.__skycoordargs)
        else:
            self.__coord.representation = 'spherical'

    def to_cartesian_coords(self):
        """
        Translates the spherical coordinates of this location into cartesian coordinates
        The center of this coordinate system will be the earth (for now)
        """
        if self.repr == 'cartesian':
            return
        self.to_spherical_coords()
        self.__coord.representation = 'cartesian'

    """
    Distances to common reference points
    """
    def distance_to_refpoint(self, refpoint):
        """
        Calculates the distance to common astronomic reference points
        :param refpoint: The reference point
        :return: the distance in parsec
        """
        # Todo: Just rudimentary implemented. Not 100% correct yet
        return switch_refpoint(refpoint, self.distance_to_earth, self.distance_to_earth,
                               self.distance_to_sun, self.distance_to_sun, self.distance_to_sun)

    def distance_to_earth(self):
        """
        Calculates the distance to earth
        :return: Distance to earth in parsec
        """
        if self.distance_module is not None:
            return 10 ** ((self.distance_module + 5) / 5)
        elif self.parallax is not None:
            return 1/self.parallax
        else:
            raise ValueError("There is no way to find out the distance to earth for this location.")

    def distance_to_sun(self):
        """
        Calculates the distance to the sun
        :return: Distance to sun in parsec
        """
        return m.sqrt(0.000004848**2 + self.distance_to_earth()**2)

    def distance_cartesian(self, place):
        """
        Calculates the cartesian distance between this place and another one
        :param place: The other place
        :return: The distance in pc
        """
        return self.__coord.separation_3d(place.__coord)

    def distance_spherical(self, place):
        """
        Calculates the spherical distance between this place and another one
        :param place: The other place
        :return: The angular distance
        """
        return self.__coord.separation(place.__coord)

"""
Helper functions
"""


def switch_frame(frame, f_icrs, f_hor, f_ecl, f_gal, f_sgal, *params):
    """
    Differ between the reference frames
    :param frame: The reference frame that is switched
    :param f_icrs: Transformation function for ICRS
    :param f_hor: Transformation function for horizontal frame
    :param f_ecl: Transformation function for ecliptic frame
    :param f_gal: Transformation function for galactic frame
    :param f_sgal: Transformation function for supergalactic frame
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
    elif frame == CRS.SUPERGALACTIC:
        return f_sgal(*params)
    else:
        raise FrameError("The reference frame {0} is currently not supported. I'm sorry".format(frame))


def parse_frame(frame):
    """
    Parses the input string and evaluates it to the respective CRS
    :param frame: The reference frame as a string
    :return: The CRS
    """
    if frame == 'horizontal':
        return CRS.HORIZONTAL
    elif frame == 'icrs':
        return CRS.ICRS
    elif frame == 'ecliptic':
        return CRS.ECLIPTIC
    elif frame == 'galactic':
        return CRS.GALACTIC
    elif frame == 'supergalactic':
        return CRS.SUPERGALACTIC
    else:
        raise FrameError("The reference frame {0} is currently not supported. I'm sorry".format(frame))


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


class CoordinateError(Exception):
    def __init__(self, message):
        super(CoordinateError, self).__init__(message)


class FrameError(Exception):
    def __init__(self, message):
        super(FrameError, self).__init__(message)


class RepresentationError(Exception):
    def __init__(self, message):
        super(RepresentationError, self).__init__(message)
