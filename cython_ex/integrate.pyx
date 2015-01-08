# encoding: utf-8
# filename: integrate.py
'''
============================================================
http://docs.cython.org/src/quickstart/cythonize.html

Created on Apr 8, 2013
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
from __future__ import division

#-------------------------------------------------
# Native Python implementation
#-------------------------------------------------
def f(x):
    return x ** 2 - x

def integrate_f(a, b, N):
    s, dx = 0, (b - a) / N
    for i in xrange(N):
        s += f(a + i * dx)
    return s * dx

#-------------------------------------------------
# With static typing
#-------------------------------------------------
cdef inline double f_static(double x) except? - 2:
    return x ** 2 - x

def integrate_f_static(double a, double b, int N):
    cdef int i
    cdef double s = 0, dx
    dx = (b - a) / N
    for i in xrange(N):
        s += f_static(a + i * dx)
    return s * dx
