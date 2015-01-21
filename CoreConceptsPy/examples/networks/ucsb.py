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
print "\nShortest paths found in the fake network:"
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


# QUICK DISPLAY
import matplotlib.pyplot as plt
plt.figure().canvas.set_window_title('FAKE NETWORK')

pos = {
    1: (2, 1),
    2: (4, 1),
    3: (1, 2),
    4: (3, 2),
    5: (5, 2),
    6: (2, 3),
    7: (4, 3)
}
edge_color = ['black'] * len(N.edges())
for i in range(len(N.edges())):
    for j in range(len(unweighted)-1):
        if unweighted[j] == N.edges()[i][0] and unweighted[j+1] == N.edges()[i][1] or unweighted[j] == N.edges()[i][1] and unweighted[j+1] == N.edges()[i][0]:
            edge_color[i] = 'red'
    for j in range(len(weighted)-1):
        if weighted[j] == N.edges()[i][0] and weighted[j+1] == N.edges()[i][1] or weighted[j] == N.edges()[i][1] and weighted[j+1] == N.edges()[i][0]:
            edge_color[i] = 'blue'
nx.draw(N._G, pos, edge_color=edge_color)

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
