#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 Abstract: Operations on a street netwrk as examples for how to use the core concept 'network'
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
import itertools
import networkx as nx
import matplotlib.pyplot as plt

sys.path = [ '.', '../..' ] + sys.path
from utils import _init_log
from networks import *

log = _init_log("ucsb")

print "\nShortest paths in the ucsb street network"
N = NetworkX()

coordinates_ids = {}
for edge in nx.read_shp('../data/networks/ucsb.shp').edges(data = True):
    sourceId = 0
    sourceCoordinates = edge[0]
    if sourceCoordinates in coordinates_ids:
        sourceId = coordinates_ids[sourceCoordinates]
    else:
        sourceId = len(N.nodes()) + 1
        N.addNode(sourceId, coordinates = sourceCoordinates)
        coordinates_ids[sourceCoordinates] = sourceId
    targetId = 0
    targetCoordinates = edge[1]
    if targetCoordinates in coordinates_ids:
        targetId = coordinates_ids[targetCoordinates]
    else:
        targetId = len(N.nodes()) + 1
        N.addNode(targetId, coordinates = targetCoordinates)
        coordinates_ids[targetCoordinates] = targetId
    N.addEdge(sourceId, targetId, length = edge[2]['length'])

a = 22
b = 86

unweighted = N.shortestPath(a, b)
weighted = N.shortestPath(a, b, weight = 'length')

print 'Unweighted: %s' % (unweighted)
print 'Weighted:   %s' % (weighted)

node_positions = {}
for node in N.nodes(data = True):
    node_positions[node[0]] = node[1]['coordinates']

node_labels = {}
for i in N.nodes():
    if i in unweighted or i in weighted:
        node_labels[i] = i

edge_color = ['black'] * len(N.edges())
for i in range(len(N.edges())):
    for j in range(len(unweighted)-1):
        if unweighted[j] == N.edges()[i][0] and unweighted[j+1] == N.edges()[i][1] or unweighted[j] == N.edges()[i][1] and unweighted[j+1] == N.edges()[i][0]:
            edge_color[i] = 'red'
    for j in range(len(weighted)-1):
        if weighted[j] == N.edges()[i][0] and weighted[j+1] == N.edges()[i][1] or weighted[j] == N.edges()[i][1] and weighted[j+1] == N.edges()[i][0]:
            edge_color[i] = 'blue'

plt.figure().canvas.set_window_title('UCSB STREET NETWORK')
nx.draw(N._G, node_positions, edge_color = edge_color)
nx.draw_networkx_labels(N._G, node_positions, node_labels)
plt.show()
