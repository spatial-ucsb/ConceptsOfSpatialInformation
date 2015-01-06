#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 Abstract: Operations on a social graph as examples for how to use the core concept 'network'
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

sys.path = [ '.', '../..' ] + sys.path

from utils import _init_log
from networks import *

log = _init_log("karate")

N = NetworkX()
N._G = nx.read_gml('examples/networks/data/karate.gml')

# TODO
