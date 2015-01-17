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

class CCLocation(object):
    """
    IGNORE THIS CLASS FOR THE MOMENT.
    Class defining abstract location relations
    """

    def isAt( figure, ground ):
        """
        @return Bool
        """
        raise NotImplementedError("isAt")

    def isIn( figure, ground ):
        """
        @return Bool
        """
        raise NotImplementedError("isIn")

    def isPart( figure, ground ):
        """
        @return Bool
        """
        raise NotImplementedError("isPart")

class CcField(object):
    """
    Class defining abstract field.
    Based on Field.hs
    """

    def __init__(self):
        """ Define appropriate parameters for construction of the concrete object """
        pass

    def getValue( self, position ):
        """ @return the value of field at position """
        raise NotImplementedError("getValue")

    def domain( self, position, value ):
        """ @return Domains can be described as intervals, rectangles, corner points, convex hulls or boundaries """
        raise NotImplementedError("domain")

    def rectNeigh( self, position, width, height ):
        """
        Map algebra: rectangular neighborhood function
        @return Geometry (a field mask)
        """
        raise NotImplementedError("rectNeigh")

    def zone( self, position ):
        """
        Map algebra: zone function
        @return Geometry (a field mask)
        """
        raise NotImplementedError("zone")

    def local( self, fun ):
        """
        Map algebra's local operations, with a function to compute the new values
        @return new CcField field
        """
        raise NotImplementedError("local")

    def focal( self, fun ):
        """
        Map algebra's focal operations, with a kernel function to compute the new values based on the neighborhood of the position
        @return new CcField field
        """
        raise NotImplementedError("focal")

    def zonal( self, fun ):
        """
        Map algebra's zonal operations, with a function to compute the new values based on zones containing the positions.
        @return new CcField field
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

class CcNetwork(object):
    """
    Abstract class for core concept 'network'
    Based on Network.hs
    """

    def __init__(self):
        pass

    def nodes( self, data = False ):
        """ @return a copy of the graph nodes in a list """
        raise NotImplementedError("nodes")

    def edges( self, data = False ):
        """ @return list of edges """
        raise NotImplementedError("edges")

    def addNode( self, n ):
        """ Add a single node n """
        raise NotImplementedError("addNode")

    def addEdge( self, u, v, **attr ):
        """ Add an edge with the attributes attr between u and v """
        raise NotImplementedError("addEdge")

    def connected( self, u, v ):
        """ @return whether node v can be reached from node u """
        raise NotImplementedError("connected")

    def shortestPath( self, source, target, weight = None ):
        """ @return shortest path in the graph """
        raise NotImplementedError("shortestPath")

    def degree( self, n ):
        """ @return number of the nodes connected to the node n """
        raise NotImplementedError("degree")

    def distance( self, source, target ):
        """ @return the length of the shortest path from the source to the target """
        raise NotImplementedError("distance")

    def breadthFirst( self, node, distance ):
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

class Period(object):
    """ Simple period class. TODO: implement"""
    def __init__(self):
        pass
