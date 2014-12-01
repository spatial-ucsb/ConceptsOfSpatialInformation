__author__ = "Michel Zimmer"
__copyright__ = "Copyright 2014"
__credits__ = ["Michel Zimmer", "Andrea Ballatore"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = ""
__email__ = ""
__date__ = "December 2014"
__status__ = "Development"

from coreconcepts import CcNetwork
import networkx as nx
from utils import _init_log

log = _init_log("networks_impl")

class NetworksX(CcNetwork):
    """
    NetworksX wrapper implementation for core concept 'network'
    """

    def __init__( self ):
        pass

    def nodes( self ):
        """ @return a copy of the graph nodes in a list """
        return self.nodes()

    def edges( self ):
        """ @return list of edges """
        return self.edges()

    def addNode( self, n ):
        """ Add a single node n """
        self.add_node(n)

    def addEdge( self, u, v ):
        """ Add an edge between u and v """
        self.add_edge(u, v)

    def connected( self, u, v ):
        """ @return whether node v can be reached from node u """
        return len(self.shortestPath(u, v)) > 0

    def shortestPath( self, source, target ):
        """ @return shortest path in the graph """
        return nx.shortest_path(self, source, target)

    def degree( self, n ):
        """ @return number of the nodes connected to the node n """
        return len(self.neighbors(n))

    def distance( self, source, target ):
        """ @return the length of the shortest path from the source to the target """
        return nx.shortest_path_length(self, source, target)

    def breadthFirst( self, node, cutoff ):
        """ @return all nodes within the distance cutoff from node in this network """
        return nx.single_source_shortest_path(self, node, cutoff)
