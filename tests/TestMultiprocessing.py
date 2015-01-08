'''
============================================================
Test multiprocessing library usage. 

Created on May 30, 2012
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
import unittest
from numpy.ma.testutils import assert_equal
from multiprocessing import Pool

f = lambda x: x * x

class TestMultiprocessing(unittest.TestCase):
    #---------------------------------------------
    # Constants
    #---------------------------------------------
    
    #---------------------------------------------
    # Test Methods
    #---------------------------------------------   
    def __test_map(self):
        # This function doesn't seem to work in unittest, only in main runs due to
        # PicklingError: Can't pickle <type 'function'>: attribute lookup __builtin__.function failed
        '''Test computing thingsCompare performance of different set intersection implementations.
        frozenset intersection is the fastest.'''
        pool = Pool(processes=4)  # start 4 worker processes
        result = pool.apply_async(f, (10,))  # evaluate "f(10)" asynchronously
        print result.get(timeout=1)  # prints "100" unless your computer is *very* slow
        assert_equal(pool.map(f, xrange(10)), [f(x) for x in xrange(10)])  # prints "[0, 1, 4,..., 81]"
    
#---------------------------------------------
# Private Methods
#---------------------------------------------
