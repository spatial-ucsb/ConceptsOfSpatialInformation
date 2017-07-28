"""
These components implement the core concept 'Field' as defined in coreconcepts.py
:author: Fenja Kollasch, 06/2017
"""
from coreconcepts import CcField
from locations import AstroExtent


class AstroField(CcField):
    """
    A field of data among an astronomic space
    """

    def __init__(self, interpol, domain,  data=None):
        """
        Initialize with a set of data and an interpolation function
        :param data: A map of positions and values.
        :param interpol: A function to interpolate between the positions
        :param domain: The domain of the interpolation function
        """
        self.__data = data
        self.__interpol = interpol
        self.__mask = dict()
        self.__domain = domain

    def value_at(self, position):
        if self.__data:
            return self.__interpol(self.__data, position)
        elif position.is_in(self.__domain):
            return self.__interpol(position)
        else:
            raise FieldError("This position is out of the specified domain.")

    def domain(self):
        return self.__domain

    def values(self):
        return [self.value_at(key) for key in self.__data]

    def mask(self, condition):
        for key in self.__data:
            if not condition(key):
                self.__mask[key] = self.__data[key]
        self.__data = dict(set(self.__data.items()) - set(self.__mask.items()))

    def unmask(self):
        self.__data = dict(**self.__data, **self.__mask)
        self.__mask = dict()

    def neighborhood(self, position):
        neighbors = []
        for key in self.__data:
            if position.is_neighbor(key):
                neighbors.append(key)
        return AstroExtent(position, neighbors)

    def zone(self, position, zone_attr=None):
        zone = []
        for key in self.__data:
            if zone_attr:
                try:
                    if key.zone_attr == position.zone_attr:
                        zone.append(key)
                except AttributeError:
                    pass
            else:
                if self.__data[key] == self.value_at(position):
                    zone.append(key)
        return AstroExtent(position, zone)

    def local(self, fun):
        if self.__data:
            new_data = {key: fun(self.__data[key], key) for key in self.__data}
            return AstroField(lambda d, p: fun(self.__interpol(d, p), p), new_data.keys(), new_data)
        return AstroField(lambda x: fun(self.__interpol(x)), self.__domain)

    def focal(self, fun):
        new_data = {key: fun(self.neighborhood(key), key) for key in self.__data}
        return AstroField(new_data, lambda d, p: fun(self.neighborhood(p)))

    def zonal(self, fun, zone_attr=None):
        new_data = {key: fun(self.zone(key, zone_attr), key) for key in self.__data}
        return AstroField(new_data, lambda d, p: fun(self.zone(p, zone_attr)))

    def __str__(self):
        s = ""
        for key in sorted(self.__data.keys()):
            s += "{0}: {1}".format(key, self.value_at(key))
            s += '\n'
        return s


class FieldError(Exception):
    def __init__(self, message):
        super(FieldError, self).__init__(message)




