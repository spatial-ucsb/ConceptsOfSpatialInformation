#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 Abstract: These classes are unit tests of the implementations of the core concept 'network', as defined in networks_impl.py
"""

__author__ = "Michel Zimmer"
__copyright__ = "Copyright 2014"
__credits__ = ["Michel Zimmer"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = ""
__email__ = ""
__date__ = "December 2014"
__status__ = "Development"

import unittest
import networkx as nx
from networks_impl import *

class TestNetworkXEmptyNetwork(unittest.TestCase):

    def setUp( self ):
        self.N = NetworkX()

    def test_nodes( self ):
        self.assertEqual(self.N.nodes(), self.N.G.nodes())

    def test_edges( self ):
        self.assertEqual(self.N.edges(), self.N.G.edges())

    def test_addNode( self ):
        """
           1   2
        """
        self.N.addNode(1)
        self.N.addNode(2)

        self.assertEqual(self.N.G.nodes(), [1, 2])

    def test_addEdge( self ):
        """
           1 - 2
        """
        self.N.addEdge(1, 2)

        self.assertEqual(self.N.G.nodes(), [1, 2])
        self.assertEqual(self.N.G.edges(), [(1, 2)])

    def test_connected( self ):
        """
           1 - 2   3
        """
        self.N.G.add_edge(1, 2)
        self.N.G.add_node(3)

        self.assertTrue(self.N.connected(1, 2))
        self.assertFalse(self.N.connected(1, 3))

    def test_shortestPath( self ):
        """
           1 - 2 - 3
           |       |
           + - 5 - 4
        """
        self.N.G.add_edge(1, 2)
        self.N.G.add_edge(2, 3)
        self.N.G.add_edge(3, 4)
        self.N.G.add_edge(4, 5)
        self.N.G.add_edge(5, 1)

        self.assertEquals(self.N.shortestPath(1, 4), [1, 5, 4])

    def test_degree( self ):
        """
           1 - 2   3
        """
        self.N.G.add_edge(1, 2)
        self.N.G.add_node(3)

        self.assertEquals(self.N.degree(1), 1)
        self.assertEquals(self.N.degree(3), 0)

    def test_distance( self ):
        """
           1 - 2 - 3
           |       |
           + - 5 - 4
        """
        self.N.G.add_edge(1, 2)
        self.N.G.add_edge(2, 3)
        self.N.G.add_edge(3, 4)
        self.N.G.add_edge(4, 5)
        self.N.G.add_edge(5, 1)

        self.assertEquals(self.N.distance(1, 4), 2)

    def test_breadthFirst( self ):
        """
           4 - 3 - 1 - 5 - 6 - 7
                   |
                   2
        """
        self.N.G.add_edge(1, 2)
        self.N.G.add_edge(1, 3)
        self.N.G.add_edge(3, 4)
        self.N.G.add_edge(1, 5)
        self.N.G.add_edge(5, 6)
        self.N.G.add_edge(6, 7)

        self.assertEquals(self.N.breadthFirst(1, 2), [1, 2, 3, 4, 5, 6])

class TestNetworkXKarateNetwork(unittest.TestCase):

    def setUp( self ):
        self.N = NetworkX()
        self.N.G = nx.read_gml('data/networks/karate.gml')

    def test_nodes( self ):
        self.assertEqual(self.N.nodes(), self.N.G.nodes())

    def test_edges( self ):
        self.assertEqual(self.N.edges(), self.N.G.edges())

    def test_addNode( self ):
        self.N.addNode(101)
        self.N.addNode(102)

        self.assertEqual(self.N.nodes(), self.N.G.nodes())
        self.assertEqual(self.N.edges(), self.N.G.edges())

    def test_addEdge( self ):
        self.N.addEdge(101, 102)

        self.assertEqual(self.N.nodes(), self.N.G.nodes())
        self.assertEqual(self.N.edges(), self.N.G.edges())

    def test_connected( self ):
        self.N.G.add_node(101)

        self.assertTrue(self.N.connected(1, 20))
        self.assertFalse(self.N.connected(1, 101))

    def test_shortestPath( self ):
        self.assertEquals(self.N.shortestPath(1, 24), [1, 32, 33, 24])

    def test_degree( self ):
        self.assertEquals(self.N.degree(1), 16)

    def test_distance( self ):
        self.assertEquals(self.N.distance(1, 24), 3)

    def test_breadthFirst( self ):
        self.assertEquals(self.N.breadthFirst(17, 3), [32, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 17, 18, 20, 22])

if __name__ == '__main__':
    unittest.main()
