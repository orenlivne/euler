'''
============================================================
Test and time various Cython implementations of integrating
a function. 

Created on June 13, 2012
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
from __future__ import division
import pyximport  # @UnresolvedImport
pyximport.install()

import time, unittest
from numpy.ma.testutils import assert_almost_equal, assert_equal
from cython_ex import integrate, hello

class TestCythonExamples(unittest.TestCase):
    #---------------------------------------------
    # Constants
    #---------------------------------------------
    
    #---------------------------------------------
    # Test Methods
    #---------------------------------------------
    def test_python_impl(self):
        '''Native python implementation.'''
        start = time.time()
        r = integrate.integrate_f(0, 1, 1000000)
        print time.time() - start, 'sec'
        assert_almost_equal(r, -1 / 6, decimal=5, err_msg='Wrong integration result')

    def test_static_typing(self):
        '''With Static typing.'''
        start = time.time()
        r = integrate.integrate_f_static(0, 1, 1000000)
        print time.time() - start, 'sec'
        assert_almost_equal(r, -1 / 6, decimal=5, err_msg='Wrong integration result')
    
    def test_primes(self):
        '''With Static typing.'''
        start = time.time()
        p = hello.primes(10000)
        print time.time() - start, 'sec'
        assert_equal(p[:10], [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] , err_msg='Wrong prime list')
        
#---------------------------------------------
# Private Methods
#---------------------------------------------
