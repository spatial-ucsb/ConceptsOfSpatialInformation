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

sys.path = [ '.', '../..' ] + sys.path
from utils import _init_log
from networks import *

log = _init_log("ucsb")


N = NetworkX()
# N._G = nx.read_shp('../data/networks/ucsb.shp')
N.addEdge((1, 1), (3, 1), length = 4)
N.addEdge((1, 1), (2, 3), length = 2)
N.addEdge((2, 3), (3, 1))

a = None
b = None
for i in itertools.combinations(N.nodes(), 2):
    if N.connected(i[0], i[1]):
        if N.shortestPath(i[0], i[1]) != N.shortestPath(i[0], i[1], weight = 'length'):
            a = i[0]
            b = i[1]
            break
if a is not None and b is not None:
    print 'Unweighted: %s' % (N.shortestPath(a, b))
    print 'Weighted:   %s' % (N.shortestPath(a, b, weight = 'length'))
else:
    print 'No pair of nodes was found that results in two different paths for weighted and unweighted shortest path finding'



# QUICK DISPLAY
import matplotlib.pyplot as plt

pos = {}
for n in N.nodes():
    pos[n] = n
nx.draw(N._G, pos)

node_labels = {}
for i in N.nodes():
    node_labels[i] = i
nx.draw_networkx_labels(N._G, pos, node_labels)

edge_labels = {}
for i in N.edges(True):
    x = i[2]
    if 'length' not in x:
        x['length'] = 1
    edge_labels[(i[0], i[1])] = x['length']
nx.draw_networkx_edge_labels(N._G, pos, edge_labels)

plt.show()
