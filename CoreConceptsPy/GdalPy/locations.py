# -*- coding: utf-8 -*-

"""
 Module abstract goes here.
"""

__author__ = "Werner Kuhn and Andrea Ballatore"
__copyright__ = "Copyright 2014"
__credits__ = ["Werner Kuhn", "Andrea Ballatore"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = ""
__email__ = ""
__date__ = "August 2014"
__status__ = "Development"

from utils import _init_log
from coreconcepts import CcLocation

log = _init_log("location")

class ExLoc(CcLocation):
    """
    IGNORE THIS CLASS FOR THE MOMENT.
    A toy implementation of ALocate.
    """

    def isAt( figure, ground ):
        # TODO: implementation with some geometric computation
        return True

    def isIn( figure, ground ):
        # TODO: implementation with some geometric computation
        return True

    def isPart( figure, ground ):
        # TODO: implementation with some geometric computation
        return False
