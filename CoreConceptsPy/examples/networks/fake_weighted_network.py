#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 Abstract: Operations on a street network as examples for how to use the core concept 'network'
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
import networkx as nx
import matplotlib.pyplot as plt

sys.path = [ '.', '../..' ] + sys.path
from utils import _init_log
from networks import *

log = _init_log("fake_weighted_network")

print "\nShortest paths in the fake weighted network"
N = NetworkX()

# horizontal
N.addEdge(1, 2, length = 5)
N.addEdge(3, 4, length = 5)
N.addEdge(4, 5, length = 4)
N.addEdge(6, 7, length = 9)
# vertical
N.addEdge(1, 3, length = 1)
N.addEdge(1, 4, length = 3)
N.addEdge(2, 4, length = 5)
N.addEdge(2, 5, length = 2)
N.addEdge(6, 3, length = 8)
N.addEdge(6, 4)
N.addEdge(7, 4)
N.addEdge(7, 5, length = 2)

a = 3
b = 5

unweighted = N.shortestPath(a, b)
weighted = N.shortestPath(a, b, weight = 'length')

print 'Unweighted: %s' % (unweighted)
print 'Weighted:   %s' % (weighted)

node_position = {
    1: (2, 1),
    2: (4, 1),
    3: (1, 2),
    4: (3, 2),
    5: (5, 2),
    6: (2, 3),
    7: (4, 3)
}

node_labels = {}
for i in N.nodes():
    node_labels[i] = i

edge_labels = {}
for i in N.edges(True):
    x = i[2]
    if 'length' not in x:
        x['length'] = 1
    edge_labels[(i[0], i[1])] = x['length']

edge_color = ['black'] * len(N.edges())
for i in range(len(N.edges())):
    for j in range(len(unweighted)-1):
        if unweighted[j] == N.edges()[i][0] and unweighted[j+1] == N.edges()[i][1] or unweighted[j] == N.edges()[i][1] and unweighted[j+1] == N.edges()[i][0]:
            edge_color[i] = 'red'
    for j in range(len(weighted)-1):
        if weighted[j] == N.edges()[i][0] and weighted[j+1] == N.edges()[i][1] or weighted[j] == N.edges()[i][1] and weighted[j+1] == N.edges()[i][0]:
            edge_color[i] = 'blue'

plt.figure().canvas.set_window_title('FAKE WEIGHTED NETWORK')
nx.draw(N._G, node_position, edge_color=edge_color)
nx.draw_networkx_labels(N._G, node_position, node_labels)
nx.draw_networkx_edge_labels(N._G, node_position, edge_labels)
plt.show()
