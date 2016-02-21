# -*- coding: utf-8 -*-

"""
 Abstract: These classes are implementations of the core concept 'network', as defined in coreconcepts.py
           The class is written in an object-oriented style.
"""

__author__ = "Michel Zimmer"
__copyright__ = "Copyright 2014"
__credits__ = ["Michel Zimmer", "Andrea Ballatore"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = ""
__email__ = ""
__date__ = "December 2014"
__status__ = "Development"

import networkx as nx

from utils import _init_log
from coreconcepts import CcNetwork

log = _init_log("networks")

class NetworkX(CcNetwork):
    """
    NetworkX wrapper implementation for core concept 'network'
    """

    def __init__( self ):
        self._G = nx.Graph()

    def nodes( self, data = False ):
        """ @return a copy of the graph nodes in a list """
        return self._G.nodes(data = data)

    def edges( self, data = False ):
        """ @return list of edges """
        return self._G.edges(data = data)

    def addNode( self, n, **attr ):
        """ Add node n with the attributes attr """
        self._G.add_node(n, attr)

    def addEdge( self, u, v, **attr ):
        """ Add an edge with the attributes attr between u and v """
        self._G.add_edge(u, v, attr)

    def connected( self, u, v ):
        """ @return whether node v can be reached from node u """
        try:
            self.shortestPath(u, v)
            return True
        except nx.NetworkXNoPath:
            return False

    def shortestPath( self, source, target, weight = None ):
        """ @return shortest path in the graph """
        if weight == None:
            return nx.shortest_path(self._G, source, target)
        else:
            return nx.shortest_path(self._G, source, target, weight = weight)

    def degree( self, n ):
        """ @return number of the nodes connected to the node n """
        return len(self._G.neighbors(n))

    def distance( self, source, target ):
        """ @return the length of the shortest path from the source to the target """
        return nx.shortest_path_length(self._G, source, target)

    def breadthFirst( self, node, cutoff ):
        """ @return all nodes within the distance cutoff from node in this network """
        return nx.single_source_shortest_path(self._G, node, cutoff).keys()
