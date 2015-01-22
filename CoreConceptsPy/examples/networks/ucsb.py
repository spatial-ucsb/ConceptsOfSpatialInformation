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
N._G = nx.read_shp('../data/networks/ucsb.shp')

unweighted = None
weighted = None
found = False
for i in itertools.combinations(N.nodes(), 2):
    if N.connected(i[0], i[1]):
        unweighted = N.shortestPath(i[0], i[1])
        weighted = N.shortestPath(i[0], i[1], weight = 'length')
        if unweighted != weighted:
            found = True
            break
if found:
    print 'Unweighted: %s' % (unweighted)
    print 'Weighted:   %s' % (weighted)
else:
    print 'No pair of nodes was found that results in two different paths for weighted and unweighted shortest path finding'

pos = {}
for i in N.nodes():
    pos[i] = i

plt.figure().canvas.set_window_title('UCSB STREET NETWORK')
nx.draw(N._G, pos)
plt.show()
