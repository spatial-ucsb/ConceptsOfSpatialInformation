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
import networkx as nx

sys.path = [ '.', '../..' ] + sys.path
from utils import _init_log
from networks import *

log = _init_log("ucsb")


N = NetworkX()
N._G = nx.read_shp('examples/networks/data/ucsb.shp')
# print nx.get_node_attributes(N._G, 0)
# print nx.get_node_attributes(N._G, N.nodes()[0])
# print nx.get_node_attributes(N._G, 3)
# print nx.get_node_attributes(N._G, N.nodes()[3])


# QUICK DISPLAY
# import matplotlib.pyplot as plt
# pos=nx.spring_layout(N._G)
# nx.draw(N._G)
# plt.show()
