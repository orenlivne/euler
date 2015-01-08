'''
============================================================
http://projecteuler.net/problem=211

For a positive integer n, let s2(n) be the sum of the squares of its divisors. For example,

s2(10) = 1 + 4 + 25 + 100 = 130.
Find the sum of all n, 0 < n < 64,000,000 such that s2(n) is a perfect square.
============================================================
'''
import numpy as np
from euler.problem142 import is_sqr

def sigma(p, N):
    '''Returns the list of sigma_p(n) = sum(d|n) d^p values for n=1,...,N.'''
    s = np.ones((N + 1,), dtype=long)
    for d in xrange(2, N + 1):
        if d % 100000 == 0: print d 
        s[d::d] += d ** p
    return s[1:]

if __name__ == "__main__":
    print sum(n for n, s in enumerate((long(x) for x in sigma(2, 64000000)), 1) if is_sqr(s))
