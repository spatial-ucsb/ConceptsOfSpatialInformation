#!/usr/bin/env python
 
# UNIT TESTS
# https://docs.python.org/2/library/unittest.html 
#

import unittest
from utils import _init_log
import numpy as np

from coreconcepts import ALocate, ExLoc, AFields, ArrFields 

log = _init_log("tests")

class CoreConceptsTest(unittest.TestCase):
    """ Unit tests for module CoreConceptsPy """
    
    def testExample(self):
        self.assertEqual(1+3,4)
        
    def testLocate(self):
        pass
        """
        figureA = Entity()
        figureB = Entity()
        groundA = Entity()
        groundB = Entity()
        
        self.assertTrue( ExLoc.isAt( figureA, groundA ) )
        self.assertFalse( ExLoc.isPart( figureA, groundA ) )
        """
        
    def testFields(self):
        
        # basic python list of tuples
        basicField = [((0,0),"ul"),((0,1),"ur"),((1,0),"ll"),((1,1),"lr")]
        print basicField
        
        # arrays based on Numpy
        numpyFieldChar = np.array([ ['ul', 'ur'], ['ll', 'lr'] ])
        print "numpyFieldChar\n",numpyFieldChar
        
        # array of floating points
        numpyFieldFloat = np.array([ [.5, .1], [.45, .2] ])
        print "numpyFieldFloat\n",numpyFieldFloat
        
        print "value for 0,0 =", ArrFields.getValue( numpyFieldFloat, [0, 0] )
        print "value for 1,1 =", ArrFields.getValue( numpyFieldFloat, [1, 1] )
        
        #print ArrField.setValue( numpyArr, [0, 1], "new value" )
        ArrFields.setValue( numpyFieldFloat, [0, 1], .2 )
        print "numpyFieldFloat after change\n",numpyFieldFloat
        #print ArrField.getValue( basicArr, [1, 1] )
    
    def testFieldsMapAlgebra(self):
        print "TODO: test map algebra on fields"
        
    def testObjects(self):
        print "TODO: test objects"
    
    def testFunctionCall(self):
        """ For @Eric: Pass a function as a parameter """
        
        def myFunction(x):
            return x * 2 + 4
        
        def myFunction2(x):
            return x - 5
        
        def funcCaller( a, func ):
            # call func on parameter a
            # "func" is a function can that can be called normally
            return func(a)
        
        # call funcCaller passing myFunction and myFunction2 as parameters, checking outputs
        self.assertEquals( funcCaller( 3, myFunction ), 10 )
        self.assertEquals( funcCaller( 3, myFunction2 ), -2 )
        self.assertEquals( funcCaller( 5, myFunction ), 14 )
        self.assertEquals( funcCaller( 5, myFunction2 ), 0 )
        
if __name__ == '__main__':
    unittest.main()