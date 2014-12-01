#!/usr/bin/env python

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

log = _init_log("coreconcepts_oo")

class ALocate(object):
    """
    IGNORE THIS CLASS FOR THE MOMENT. 
    Class defining abstract location relations
    """
    
    @staticmethod
    def isAt( figure, ground ):
        """
        @return Bool
        """
        raise NotImplementedError("isAt")
    
    @staticmethod
    def isIn( figure, ground ):
        """
        @return Bool
        """
        raise NotImplementedError("isIn")
    
    @staticmethod
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
        pass
    
    def getValue( self, position ):
        """ @return the value of field at position """
        raise NotImplementedError("getValue")
    
    def setValue( self, position, value ):
        """ @return the position of new value in field """
        raise NotImplementedError("setValue")
        
    def domain( self, position, value ):
        """ @return Domains can be described as intervals, rectangles, corner points, convex hulls or boundaries """
        raise NotImplementedError("domain")
    
    def neigh( self, position ):
        """
        Map algebra: neighborhood function
        @return Geometry 
        """
        raise NotImplementedError("neigh")
    
    def zone( self, position ):
        """
        Map algebra: zone function
        @return Geometry
        """
        raise NotImplementedError("zone")
    
    def local( self, fun ):
        """
        Map algebra's local operations, with a function to compute the new values
        @return new field
        """
        raise NotImplementedError("local")
    
    def focal( self, fun ):
        """
        Map algebra's focal operations, with a kernel function to compute the new values based on the neighborhood of the position
        @return new field
        """
        raise NotImplementedError("focal")
    
    def zonal( self, fun ):
        """
        Map algebra's zonal operations, with a function to compute the new values based on zones containing the positions.
        @return new field
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

    def nodes( self ):
        """ @return all nodes part of this network """
        raise NotImplementedError("nodes")
    
    def edges( self ):
        """ @return all edges part of this network """
        raise NotImplementedError("edges")
    
    def addNode( self, node ):
        """ adds given node to this network """
        raise NotImplementedError("addNode")
    
    def addEdge( self, edge ):
        """ adds given edge to this network """
        raise NotImplementedError("addEdge")
    
    def connected( self, nodeA, nodeB ):
        """ @return whether B can be reached from A in this network """
        raise NotImplementedError("connected")

    def shortestPath( self, nodeA, nodeB ):
        """ @return list of edges """
        raise NotImplementedError("shortestPath")
    
    def degree( self, node ):
        """ @return the number of edges to other nodes in this network """
        raise NotImplementedError("degree")
    
    def linking( netw, edge ):
        """ @return the nodes encapsulating given edge in this network """
        raise NotImplementedError("linking")

    def distance( self, nodeA, nodeB ):
        """ @return the length of shortest path from A to B in this network """
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
    
    @staticmethod
    def before( self, event ):
        """
        @param event an event
        @return Boolean
        """
        raise NotImplementedError("before")
    
    @staticmethod
    def after( self, event ):
        """
        @param event an event
        @return Boolean
        """
        raise NotImplementedError("after")
    
    @staticmethod
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
