
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TODO: description of module
"""

__author__ = "Marc Tim Thiemann"
__copyright__ = "Copyright 2014"
__credits__ = ["Marc Tim Thiemann"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = ""
__email__ = ""
__date__ = "December 2014"
__status__ = "Development"

import sys

sys.path = [ '.', '../..' ] + sys.path
from utils import _init_log
from events import *
import dateutil.parser
from datetime import *

log = _init_log("example-1")

p = PyEvent(datetime(2015, 1, 7, 10, 48, 15), datetime(2015, 1, 7, 10, 48, 15))

'''
DEFAULT = datetime(date.today().year, 1, 1, 0, 0, 0, 0)
        try:
            self.startTime = dateutil.parser.parse(startTime, default=DEFAULT)
        except ValueError:
            print "Invalid start time, could not create Event."

        if endTime != None:
            try:
                self.endTime = dateutil.parser.parse(endTime, default=DEFAULT)
            except ValueError:
                print "Invalid end time, could not create Event."
            assert self.endTime >= self.startTime
        else:
            self.endTime = None
'''
