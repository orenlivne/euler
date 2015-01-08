'''
============================================================
http://projecteuler.net/problem=5

2520 is the smallest number that can be divided by each of the numbers from 1 to 10 without any remainder.

What is the smallest positive number that is evenly divisible by all of the numbers from 1 to 20?

Created on Feb 21, 2013
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
import numpy as np

def smallest_mult(n):
    '''Return the  smallest positive number that is evenly divisible by all of the numbers
    from 1 to n.

    >>> smallest_mult(10)
    2520

    >>> smallest_mult(20)
    232792560

    >>> [smallest_mult(x) for x in xrange(2,20)]
    [2, 6, 12, 60, 60, 420, 840, 2520, 2520, 27720, 27720, 360360, 360360, 360360, 720720, 12252240, 12252240, 232792560]'''
    a = np.arange(2, n + 1)
    for i in xrange(n - 1):
        p = a[i]
        if p > 1:
            a[i + 1:] /= np.array([gcd(p, x) for x in a[i + 1:]])
    return np.prod(a)

def gcd(m, n):
    '''Greatest common divisor. Eulid''s algorithm.'''
    while n: m, n = n, m % n
    return m

if __name__ == "__main__":
    import doctest
    doctest.testmod()
