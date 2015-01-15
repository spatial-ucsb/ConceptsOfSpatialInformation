#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 Abstract: Unit tests for the implementations of the core concept 'network'
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

import sys
import unittest
import networkx as nx

sys.path = [ '.', '..' ] + sys.path
from utils import _init_log
from networks import *

log = _init_log("networks_test")

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

    def test_shortestWeightedEdgesPath( self ):
        """
           1 = 3
           |   |
           2 - +
        """
        self.N.addEdge(1, 2, weight = 1)
        self.N.addEdge(2, 3)
        self.N.addEdge(1, 3, weight = 4)

        self.assertEquals(self.N.shortestPath(1, 3), [1, 3])
        self.assertEquals(self.N.shortestPath(1, 3, 'weight'), [1, 2, 3])

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

if __name__ == '__main__':
    unittest.main()
