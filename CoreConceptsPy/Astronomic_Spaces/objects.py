"""
Implementation of the coreconecpt 'Object' as written in coreconcepts.py
:author: Fenja Kollasch, 06/2017
"""


from coreconcepts import CcObject
from coreconcepts import CcObjectSet
import locations as l
import math


VALID_ARGS = ['representation', 'location', 'obstime', 'equinox', 'distance_module', 'parallax', 'orbit', 'space']


# Todo: More abstract. Doesn't have to stand alone
class AstroObject(CcObject):
    """
    Subclass of the abstract Object
    This class is simulating an astronomic object
    it is assumed that such an object as a declination, a right ascension and a luminosity
    All spatial information remains relative to the earth
    """
    
    def __init__(self, identity, **data):

        self.id = identity

        # Save all properties of this object as a dictionary
        self._data = data

        try:
            rel = self._data.pop('bounding')
            ref = self._data.pop('reference')
            args = dict()
            for attr in VALID_ARGS:
                try:
                    value = self.property(attr)
                    args[attr] = value
                except AttributeError:
                    pass
            self.__location = l.locate(rel, ref, self, **args)
        except (KeyError, ObjectError):
            self.__location = None

    def bounds(self):
        """
        The initial bounds of this object (if possible)
        :return: The location bounded to this object
        """
        return self.__location

    def rebound(self, relation, reference):
        """
        Change the location bounds into another representation
        :param relation: The relation describing the location
        :param reference: The reference object
        """
        args = dict()
        for attr in VALID_ARGS:
            try:
                value = self.property(attr)
                args[attr] = value
            except ObjectError:
                pass
        self.__location = l.locate(relation, reference, self)

    def relation(self, obj, relType):
        try:
            return l.resolve(relType, self.bounds(), obj.bounds())
        except AttributeError:
            return l.resolve(relType, self.bounds(), obj)

    def property(self, prop):
        """
        Get any additional property from this object
        :param prop: The property name
        :return: The value of the property
        """
        if prop in self._data:
            return self._data[prop]
        else:
            try:
                self._data[prop] = getattr(self, '_calc_' + prop)()
                return self._data[prop]
            except AttributeError:
                raise AttributeError("This object doesn't own a property named {0}.".format(prop))

    def set_property(self, prop, value):
        self._data[prop] = value

    def identity(self, obj):
        return self.id == obj.id

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.identity(other)

    def __str__(self):
        return self.id

    """
    Some additional functions that might be useful when it comes to spatial reasoning in astronomy
    """
    def _calc_distance_module(self):
        try:
            app_mag = self.property('app_mag')
            abs_mag = self.property('abs_mag')

            return app_mag - abs_mag
        except ValueError:
            return None

    def _calc_abs_mag(self):
        if "period" not in self._data:
            raise ValueError("Your object should be a cepheid with a measured period.")

        # Leavitt's Law
        return -3.6 * math.log(float(self._data["period"]), 10) - 2.401


class AstroObjectSet(CcObjectSet):

    def __iter__(self):
        return iter(self.obj_set)

    def len(self):
        return len(self.obj_set)


class ObjectError(Exception):
    def __init__(self, message):
        super(ObjectError, self).__init__(message)