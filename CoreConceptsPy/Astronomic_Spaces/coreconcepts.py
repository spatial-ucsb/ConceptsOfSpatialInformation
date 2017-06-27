# -*- coding: utf-8 -*-

"""
 Abtract: These classes are the specifications of the core concepts, adapted from the Haskell.
          The classes are written in an object-oriented style.
"""

__author__ = "Werner Kuhn and Andrea Ballatore"
__copyright__ = "Copyright 2014"
__credits__ = ["Werner Kuhn", "Andrea Ballatore"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Andrea Ballatore"
__email__ = ""
__date__ = "August 2014"
__status__ = "Development"

from utils import _init_log

log = _init_log("coreconcepts")


class CcLocation(object):
    """
    Class defining abstract location relations
    Modified by Fenja Kollasch, 05/18/2017
    """
    def distance(self, ground):
        """
        Calculates the distance between two location
        :param ground: The other location
        :return: The distance between this location and the ground
        """
        raise NotImplementedError("distance")

    def is_at(self, ground):
        """
        Is this location at the ground?
        :param ground: Another landmark (star, galaxy, etc)
        :return: True or False
        """
        raise NotImplementedError("is_at")

    def is_in(self, ground):
        """
        Is this location in the ground space?
        :param ground: Another landmark (solar system, galaxy, etc)
        :return: True or False
        """
        raise NotImplementedError("is_in")

    def is_part(self, ground):
        """
        Is this location part of an other space?
        :param ground: 
        :return: 
        """
        raise NotImplementedError("is_part")

    def is_neighbor(self, ground):
        """
        Are these two locations part of the same neighborhood?
        :param ground: 
        :return: 
        """
        raise NotImplementedError("is_neighbor")


class CcField(object):
    """
    Class defining abstract field.
    Based on Field.hs
    """

    def __init__(self):
        """ Define appropriate parameters for construction of the concrete object """
        pass

    def value_at( self, position ):
        """ 
        @return the value of field at position, or None if it is outside of the domain.
        """
        raise NotImplementedError("valueAt")

    def domain(self):
        """
        @return current domain of the field
        """
        raise NotImplementedError("domain")

    def mask(self, condition):
        """
        Mask out positions of the field that doesn't fit a condition
        :param condition: Which positions should be cut out?
        """
        raise NotImplementedError("mask")

    def neighborhood(self, position):
        """
        :param position: A position in the field
        :return: The neighborhood of this position
        """
        raise NotImplementedError("neighborhood")

    def zone(self, position, zone_attr=None):
        """
        Map algebra: zone function
        :param position: The position modeling the zone
        :param zone_attr: A specific attribute whose value defines the zone
        :return: An extend with all positions sharing the same value at some attribute
        """
        raise NotImplementedError("zone")

    def local(self, fun):
        """
        Map algebra's local operations, with a function to compute the new values
        :param fun: A function: value -> value to recalculate the values
        :return: The field with the new data
        """
        raise NotImplementedError("local")

    def focal(self, fun):
        """
        Map algebra's focal operations, with a kernel function to compute the new values based on the neighborhood of the position
        @return new CcField field
        """
        raise NotImplementedError("focal")

    def zonal(self, fun, zone_attr=None):
        """
        Map algebra's zonal operations, with a function to compute the new values based on zones containing the positions.
        :param fun: A function: Extend -> value applied to every position
        :param zone_attr: A specific attribute whose value defines the zone
        :return: new CcField field
        """
        raise NotImplementedError("zonal")


class CcObject(object):
    """
    Abstract class for core concept 'object'
    Based on Object.hs
    """

    def bounds( self ):
        raise NotImplementedError("bounds")

    def relation( self, obj, relType ):
        """ @return Boolean True if self and obj are in a relationship of type relType
                    False otherwise
        """
        raise NotImplementedError("relation")

    def property( self, prop ):
        """
        @param prop the property name
        @return value of property in obj
        """
        raise NotImplementedError("property")

    def identity( self, obj ):
        """
        @param an object
        @return Boolean True if self and obj are identical
        """
        raise NotImplementedError("identity")

class CcObjectSet(object):
    """
    Set class for object sets
    """
    def __init__(self):
        self.obj_set = set()
    
    def add(self, obj ):
        assert obj is not None
        self.obj_set.add(obj)
    
    def remove(self, obj):
        self.obj_set.remove(obj)
        

class CcNetwork(object):
    """
    Abstract class for core concept 'network'
    Based on Network.hs
    
    Modified by Fenja Kollasch 5/16/2017
    """

    def __init__(self):
        pass

    def nodes(self):
        """ @return a copy of the graph nodes in a list """
        raise NotImplementedError("nodes")

    def edges(self):
        """ @return list of edges """
        raise NotImplementedError("edges")

    def addNode(self, n, **attr):
        """ Add node n with the attributes attr """
        raise NotImplementedError("addNode")

    def addEdge(self, u, v, **attr):
        """ Add an edge with the attributes attr between u and v """
        raise NotImplementedError("addEdge")

    def connected(self, u, v, visited=[]):
        """ @return whether node v can be reached from node u """
        raise NotImplementedError("connected")

    def shortestPath(self, source, target, path=None, color=None):
        """ @return shortest path in the graph """
        raise NotImplementedError("shortestPath")

    def degree(self, n):
        """ @return number of the nodes connected to the node n """
        raise NotImplementedError("degree")

    def distance(self, source, target, weight=None):
        """ @return the length of the shortest path from the source to the target """
        raise NotImplementedError("distance")

    def breadthFirst( self, node, distance, nodes=[]):
        """ @return all nodes within the distance from node in this network """
        raise NotImplementedError("breadthFirst")

class CcEvent(object):
    """
    Abstract class for core concept 'event'.
    Based on Event.hs
    """

    def __init__(self):
        pass

    def within( self ):
        """
        @return a Period
        """
        raise NotImplementedError("within")

    def when( self ):
        """
        @return a Period
        """
        raise NotImplementedError("when")

    def during( self, event ):
        """
        @param event an event
        @return boolean
        """
        raise NotImplementedError("during")

    def before( self, event ):
        """
        @param event an event
        @return Boolean
        """
        raise NotImplementedError("before")

    def after( self, event ):
        """
        @param event an event
        @return Boolean
        """
        raise NotImplementedError("after")

    def overlap( self, event ):
        """
        @param event an event
        @return Boolean
        """
        raise NotImplementedError("overlap")

class CcGranularity:
    def __init__(self):
        pass
        # TODO: cell_size_x, cell_size_y