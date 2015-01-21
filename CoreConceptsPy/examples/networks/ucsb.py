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


################################################################################
#                             FAKE WEIGHTED NETWORK                            #
################################################################################
print "\nPathfinding in a faked network"
N = NetworkX()

# lower row
N.addEdge(1, 2, length=5)
N.addEdge(2, 3, length=5)
# mid row
N.addEdge(4, 5, length=5)
N.addEdge(5, 6, length=5)
N.addEdge(6, 7, length=5)
N.addEdge(7, 8, length=5)
# upper row
N.addEdge(9, 10, length=5)
N.addEdge(10, 11, length=5)
# mid - lower row
N.addEdge(4, 1, length=5)
N.addEdge(5, 1, length=5)
N.addEdge(6, 2, length=5)
N.addEdge(7, 3, length=5)
N.addEdge(8, 3, length=5)
# mid - upper row
N.addEdge(4, 9, length=5)
N.addEdge(5, 9, length=5)
N.addEdge(6, 10, length=5)
N.addEdge(7, 11, length=5)
N.addEdge(8, 11, length=5)

a = 4
b = 8

unweighted = N.shortestPath(a, b)
weighted = N.shortestPath(a, b, weight = 'length')

print 'Unweighted: %s' % (unweighted)
print 'Weighted:   %s' % (weighted)


# QUICK DISPLAY
import matplotlib.pyplot as plt

pos = {
    1: (2, 1),
    2: (3, 1),
    3: (4, 1),
    4: (1, 2),
    5: (2, 2),
    6: (3, 2),
    7: (4, 2),
    8: (5, 2),
    9: (2, 3),
    10: (3, 3),
    11: (4, 3)
}
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

################################################################################
#                                UCSB GRAPH ML                                 #
################################################################################
# N._G = nx.read_shp('../data/networks/ucsb.shp')
# nx.write_graphml(N._G, '../data/networks/ucsb_generated.gml')
# N._G = nx.read_graphml('../data/networks/ucsb_generated.gml')
# print N.edges()
# a = (-119.8460526, 34.4116052) # (-119.8515868, 34.4078621) (-119.8497461, 34.4130853)
# b = (-119.8437565, 34.4166028) # (-119.8425923, 34.4096374) (-119.8422863, 34.4117292)

# unweighted = None
# weighted = None
# found = False
# for i in itertools.combinations(N.nodes(), 2):
#     if N.connected(i[0], i[1]):
#         unweighted = N.shortestPath(i[0], i[1])
#         weighted = N.shortestPath(i[0], i[1], weight = 'length')
#         if unweighted != weighted:
#             found = True
#             break
# if found:
#     print 'Unweighted: %s' % (unweighted)
#     print 'Weighted:   %s' % (weighted)
# else:
#     print 'No pair of nodes was found that results in two different paths for weighted and unweighted shortest path finding'


# # QUICK DISPLAY
# import matplotlib.pyplot as plt

# pos = {}
# for i in N.nodes():
#     pos[i] = i
# nx.draw(N._G, pos)

# node_labels = {}
# for i in N.nodes():
#     if not found or i in unweighted or i in weighted:
#         node_labels[i] = i
# nx.draw_networkx_labels(N._G, pos, node_labels)

# edge_labels = {}
# for i in N.edges(True):
#     x = i[2]
#     if 'length' not in x:
#         x['length'] = 1
#     edge_labels[(i[0], i[1])] = x['length']
# nx.draw_networkx_edge_labels(N._G, pos, edge_labels)

# plt.show()
