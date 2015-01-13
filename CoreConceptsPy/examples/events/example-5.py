#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Example 5:

Use Cases:

Provided data:

"""

__author__ = "Marc Tim Thiemann"
__copyright__ = "Copyright 2014"
__credits__ = ["Marc Tim Thiemann"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = ""
__email__ = ""
__date__ = "January 2015"
__status__ = "Development"

import sys

sys.path = [ '.', '../..' ] + sys.path
from utils import _init_log
from events import *
import dateutil.parser
from datetime import *

log = _init_log("example-5")
