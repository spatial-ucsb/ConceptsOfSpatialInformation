#!/usr/bin/env python

"""
 Module abstract goes here.
"""

__author__ = "Werner Kuhn and Andrea Ballatore"
__copyright__ = "Copyright 2014"
__credits__ = ["Werner Kuhn", "Andrea Ballatore"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = ""
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
     
class ExLoc(ALocate):
    """ 
    IGNORE THIS CLASS FOR THE MOMENT.
    A toy implementation of ALocate.
    """
    
    @staticmethod
    def isAt( figure, ground ):
        # TODO: implementation with some geometric computation
        return True
    
    @staticmethod
    def isIn( figure, ground ):
        # TODO: implementation with some geometric computation
        return True
    
    @staticmethod
    def isPart( figure, ground ):
        # TODO: implementation with some geometric computation
        return False
    
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
    def local( field, position, fun ):
        """
        Map algebra: zone function
        @return new values for field based on function fun
        """
        raise NotImplementedError("local")
    
    @staticmethod
    def focal( field, position, fun ):
        """
        Map algebra: zone function
        @return new values for field based on function fun
        """
        raise NotImplementedError("focal")
    
    @staticmethod
    def zonal( field, position, fun ):
        """
        Map algebra: zone function
        @return new values for field based on function fun
        """
        raise NotImplementedError("zonal")
    
class ArrFields(AFields):
    """ Implementation of AField with Python arrays """
        
    @staticmethod
    def getValue( field, position ):
        x = position[0]
        y = position[1]
        return field[x,y]
    
    @staticmethod
    def setValue( field, position, value ):
        """ @return the position of new value in field """
        x = position[0]
        y = position[1]
        field[x,y] = value
        return field, position, value
     
    @staticmethod
    def domain( field, position, value ):
        """ @return Domains can be described as intervals, rectangles, corner points, convex hulls or boundaries """
        raise NotImplementedError("domain")

class AObjects(object):
    """ Abstract class for core concept 'object' """
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
        """ @return value of prop """
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
    """ Abstract class for core concept 'event' """
    @staticmethod
    def exampleMethod( obj ):
        raise NotImplementedError("exampleMethod")
