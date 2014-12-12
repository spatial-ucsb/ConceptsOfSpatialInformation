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
        self.assertEqual(self.N.nodes(), [])

    def test_edges( self ):
        self.assertEqual(self.N.edges(), [])

    def test_addNode( self ):
        """
           1   2
        """
        self.N.addNode(1)
        self.N.addNode(2)

        self.assertEqual(self.N.nodes(), [1, 2])

    def test_addEdge( self ):
        """
           1 - 2
        """
        self.N.addEdge(1, 2)

        self.assertEqual(self.N.nodes(), [1, 2])
        self.assertEqual(self.N.edges(), [(1, 2)])

    def test_connected( self ):
        """
           1 - 2   3
        """
        self.N.addEdge(1, 2)
        self.N.addNode(3)

        self.assertTrue(self.N.connected(1, 2))
        self.assertFalse(self.N.connected(1, 3))

    def test_shortestPath( self ):
        """
           1 - 2 - 3
           |       |
           + - 5 - 4
        """
        self.N.addEdge(1, 2)
        self.N.addEdge(2, 3)
        self.N.addEdge(3, 4)
        self.N.addEdge(4, 5)
        self.N.addEdge(5, 1)

        self.assertEquals(self.N.shortestPath(1, 4), [1, 5, 4])

    def test_degree( self ):
        """
           1 - 2   3
        """
        self.N.addEdge(1, 2)
        self.N.addNode(3)

        self.assertEquals(self.N.degree(1), 1)
        self.assertEquals(self.N.degree(3), 0)

    def test_distance( self ):
        """
           1 - 2 - 3
           |       |
           + - 5 - 4
        """
        self.N.addEdge(1, 2)
        self.N.addEdge(2, 3)
        self.N.addEdge(3, 4)
        self.N.addEdge(4, 5)
        self.N.addEdge(5, 1)

        self.assertEquals(self.N.distance(1, 4), 2)

    def test_breadthFirst( self ):
        """
           4 - 3 - 1 - 5 - 6 - 7
                   |
                   2
        """
        self.N.addEdge(1, 2)
        self.N.addEdge(1, 3)
        self.N.addEdge(3, 4)
        self.N.addEdge(1, 5)
        self.N.addEdge(5, 6)
        self.N.addEdge(6, 7)

        self.assertEquals(self.N.breadthFirst(1, 2), [1, 2, 3, 4, 5, 6])

class TestNetworkXKarateNetwork(unittest.TestCase):

    def setUp( self ):
        self.N = NetworkX()
        self.N._G = nx.read_gml('data/networks/karate.gml')

    def test_nodes( self ):
        self.assertEqual(self.N.nodes(), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34])

    def test_edges( self ):
        self.assertEqual(self.N.edges(), [(1, 32), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 11), (1, 12), (1, 13), (1, 14), (1, 18), (1, 20), (1, 22), (2, 3), (2, 4), (2, 8), (2, 14), (2, 18), (2, 20), (2, 22), (2, 31), (3, 4), (3, 33), (3, 8), (3, 9), (3, 10), (3, 14), (3, 28), (3, 29), (4, 8), (4, 13), (4, 14), (5, 11), (5, 7), (6, 7), (6, 11), (6, 17), (7, 17), (9, 31), (9, 34), (9, 33), (10, 34), (14, 34), (15, 33), (15, 34), (16, 33), (16, 34), (19, 33), (19, 34), (20, 34), (21, 33), (21, 34), (23, 33), (23, 34), (24, 33), (24, 26), (24, 28), (24, 34), (24, 30), (25, 32), (25, 26), (25, 28), (26, 32), (27, 34), (27, 30), (28, 34), (29, 32), (29, 34), (30, 33), (30, 34), (31, 34), (31, 33), (32, 33), (32, 34), (33, 34)])

    def test_addNode( self ):
        self.N.addNode(101)
        self.N.addNode(102)

        self.assertEqual(self.N.nodes(), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 101, 102])
        self.assertEqual(self.N.edges(), [(1, 32), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 11), (1, 12), (1, 13), (1, 14), (1, 18), (1, 20), (1, 22), (2, 3), (2, 4), (2, 8), (2, 14), (2, 18), (2, 20), (2, 22), (2, 31), (3, 4), (3, 33), (3, 8), (3, 9), (3, 10), (3, 14), (3, 28), (3, 29), (4, 8), (4, 13), (4, 14), (5, 11), (5, 7), (6, 7), (6, 11), (6, 17), (7, 17), (9, 31), (9, 34), (9, 33), (10, 34), (14, 34), (15, 33), (15, 34), (16, 33), (16, 34), (19, 33), (19, 34), (20, 34), (21, 33), (21, 34), (23, 33), (23, 34), (24, 33), (24, 26), (24, 28), (24, 34), (24, 30), (25, 32), (25, 26), (25, 28), (26, 32), (27, 34), (27, 30), (28, 34), (29, 32), (29, 34), (30, 33), (30, 34), (31, 34), (31, 33), (32, 33), (32, 34), (33, 34)])

    def test_addEdge( self ):
        self.N.addEdge(101, 102)

        self.assertEqual(self.N.nodes(), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 101, 102])
        self.assertEqual(self.N.edges(), [(1, 32), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 11), (1, 12), (1, 13), (1, 14), (1, 18), (1, 20), (1, 22), (2, 3), (2, 4), (2, 8), (2, 14), (2, 18), (2, 20), (2, 22), (2, 31), (3, 4), (3, 33), (3, 8), (3, 9), (3, 10), (3, 14), (3, 28), (3, 29), (4, 8), (4, 13), (4, 14), (5, 11), (5, 7), (6, 7), (6, 11), (6, 17), (7, 17), (9, 31), (9, 34), (9, 33), (10, 34), (14, 34), (15, 33), (15, 34), (16, 33), (16, 34), (19, 33), (19, 34), (20, 34), (21, 33), (21, 34), (23, 33), (23, 34), (24, 33), (24, 26), (24, 28), (24, 34), (24, 30), (25, 32), (25, 26), (25, 28), (26, 32), (27, 34), (27, 30), (28, 34), (29, 32), (29, 34), (30, 33), (30, 34), (31, 34), (31, 33), (32, 33), (32, 34), (33, 34), (101, 102)])

    def test_connected( self ):
        self.N.addNode(101)

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
