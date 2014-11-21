#!/usr/bin/env python

"""
 Abtract: These classes are the specifications of the core concepts, adapted from Haskell.
          The classes are written in a functional style.
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
    
class AFields(object):
    """ Class defining abstract fields """
    
    @staticmethod
    def getValue( field, position ):
        """ @return the value of field at position """
        raise NotImplementedError("getValue")
    
    @staticmethod
    def setValue( field, position, value ):
        """ @return the position of new value in field """
        raise NotImplementedError("setValue")
        
    @staticmethod
    def domain( field, position, value ):
        """ @return Domains can be described as intervals, rectangles, corner points, convex hulls or boundaries """
        raise NotImplementedError("domain")
    
    @staticmethod
    def neigh( field, position ):
        """
        Map algebra: neighborhood function
        @return Geometry 
        """
        raise NotImplementedError("neigh")
    
    @staticmethod
    def zone( field, position ):
        """
        Map algebra: zone function
        @return Geometry
        """
        raise NotImplementedError("neigh")
    
    @staticmethod
    def local( field, fun ):
        """
        Map algebra's local operations, with a function to compute the new values
        @return new field
        """
        raise NotImplementedError("local")
    
    @staticmethod
    def focal( field, fun ):
        """
        Map algebra's focal operations, with a kernel function to compute the new values based on the neighborhood of the position
        @return new field
        """
        raise NotImplementedError("focal")
    
    @staticmethod
    def zonal( field, fun ):
        """
        Map algebra's zonal operations, with a function to compute the new values based on zones containing the positions.
        @return new field
        """
        raise NotImplementedError("zonal")

class AObjects(object):
    """ Abstract class for core concept 'object' """
    #TODO: update with new specs 
    @staticmethod
    def getBounds( obj ):
        raise NotImplementedError("getBounds")
    
    @staticmethod
    def hasRelation( objA, objB, relType ):
        """ @return Boolean True if objA and objB are in a relationship of type relType
                    False otherwise
        """
        raise NotImplementedError("hasRelation")
    
    @staticmethod
    def getProperty( obj, prop ):
        """
        @param obj the object
        @param prop the property name 
        @return value of property in obj
        """
        raise NotImplementedError("getProperty")
    
class ANetworks(object):
    """ Abstract class for core concept 'network' """
    @staticmethod
    def nodes( netw ):
        """ @return all nodes part of this network """
        raise NotImplementedError("nodes")
    
    @staticmethod
    def edges( netw ):
        """ @return all edges part of this network """
        raise NotImplementedError("edges")
    
    @staticmethod
    def addNode( netw, node ):
        """ adds given node to this network """
        raise NotImplementedError("addNode")
    
    @staticmethod
    def addEdge( netw, edge ):
        """ adds given edge to this network """
        raise NotImplementedError("addEdge")
    
    @staticmethod
    def linking( netw, edge ):
        """ @return the nodes encapsulating given edge in this network """
        raise NotImplementedError("linking")
    
    @staticmethod
    def degree( netw, node ):
        """ @return the number of edges to other nodes in this network """
        raise NotImplementedError("degree")
    
    @staticmethod
    def connected( netw, nodeA, nodeB ):
        """ @return whether B can be reached from A in this network """
        raise NotImplementedError("connected")
    
    @staticmethod
    def shortestPath( netw, nodeA, nodeB ):
        """ @return the shortest path from A to B in this network """
        raise NotImplementedError("shortestPath")
    
    @staticmethod
    def distance( netw, nodeA, nodeB ):
        """ @return the length of shortest path from A to B in this network """
        raise NotImplementedError("distance")
    
    @staticmethod
    def breadthFirst( netw, node, distance ):
        """ @return all nodes within the distance from node in this network """
        raise NotImplementedError("breadthFirst")
    
class AEvents(object):
    """ Abstract class for core concept 'event'. Based on Event.hs """
    
    @staticmethod
    def within( ev ):
        """
        @ev an event
        @return a Period 
        """
        raise NotImplementedError("within")
    
    @staticmethod
    def when( ev ):
        """
        @ev an event
        @return a Period 
        """
        raise NotImplementedError("when")
    
    @staticmethod
    def during( ev, otherEv ):
        """
        @ev an event
        @ev otherEvent another event
        @return boolean
        """
        raise NotImplementedError("during")
    
    @staticmethod
    def before( ev, otherEv ):
        """
        @ev an event
        @ev otherEvent another event
        @return boolean
        """
        raise NotImplementedError("before")
    
    @staticmethod
    def after( ev, otherEv ):
        """
        @ev an event
        @ev otherEvent another event
        @return boolean
        """
        raise NotImplementedError("after")
    
    @staticmethod
    def overlap( ev, otherEv ):
        """
        @ev an event
        @ev otherEvent another event
        @return boolean
        """
        raise NotImplementedError("overlap")
    
class Event(object):
    """ Simple event class. TODO: implement"""
    pass

class Period(object):
    """ Simple period class. TODO: implement"""
    pass
