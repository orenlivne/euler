'''
============================================================
Test and time various Cython implementations of integrating
a function. 

Created on June 13, 2012
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
import rosalind.rosutil as ro, unittest
from numpy.ma.testutils import assert_equal

class TestRosUtil(unittest.TestCase):
    def test_skip(self):
        assert_equal(list(ro.skip((x**2 for x in xrange(5)), 2)), [4, 9, 16]) 
