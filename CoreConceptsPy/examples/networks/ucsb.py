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
# N._G = nx.read_shp('examples/networks/data/ucsb.shp')
N.addEdge(1, 2, length = 5)
N.addEdge(1, 3)
N.addEdge(3, 2)

print N.edges(True)[0][2]['length']

a = None
b = None
for i in itertools.combinations(N.nodes(), 2):
    if N.connected(i[0], i[1]):
        if N.shortestPath(i[0], i[1]) != N.shortestPath(i[0], i[1], weight = 'length'):
            a = i[0]
            b = i[1]
            break
print a
print b

# QUICK DISPLAY
# import matplotlib.pyplot as plt
# pos=nx.spring_layout(N._G)
# nx.draw(N._G)
# plt.show()
