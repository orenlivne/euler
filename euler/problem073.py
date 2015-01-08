'''
============================================================
http://projecteuler.net/problem=73

Consider the fraction, n/d, where n and d are positive integers. If nd and HCF(n,d)=1, it is called a reduced proper fraction.

If we list the set of reduced proper fractions for d  8 in ascending order of size, we get:

1/8, 1/7, 1/6, 1/5, 1/4, 2/7, 1/3, 3/8, 2/5, 3/7, 1/2, 4/7, 3/5, 5/8, 2/3, 5/7, 3/4, 4/5, 5/6, 6/7, 7/8

It can be seen that there are 3 fractions between 1/3 and 1/2.

How many fractions lie between 1/3 and 1/2 in the sorted set of reduced proper fractions for d <= 12,000?
============================================================
'''
from math import ceil
from problem005 import gcd
import itertools as it

def num_frac(A, B, D):
    a, b = A + 1e-15, B - 1e-15
#     for d in xrange(2, D + 1):
#         high = it.dropwhile(lambda n: gcd(d, n) != 1 and n > 0, xrange(int(b * d), -1, -1)).next()
#         low = it.dropwhile(lambda n: gcd(d, n) != 1 and n < d, xrange(int(ceil(a * d)), d + 1)).next()
#         print 'd', d, '%.2f < %d/%d=%.2f to %d/%d=%.2f < %.2f, %d' % \
#         (a, low, d, float(low) / d, high, d, float(high) / d, b, max(high - low + 1, 0))
#         
    return sum(len(filter(lambda n: gcd(d, n) == 1, xrange(int(ceil(a * d)), int(b * d) + 1)))
               for d in xrange(2, D + 1))
#     return sum(max(it.dropwhile(lambda n: gcd(d, n) != 1 and n > 0,
#                                 xrange(int(b * d), -1, -1)).next() - 
#                    it.dropwhile(lambda n:gcd(d, n) != 1 and n < d,
#                                 xrange(int(ceil(a * d), d + 1))).next() + 1, 0) 
#                for d in xrange(2, D + 1))
    
if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
    print num_frac(1. / 3, 1. / 2, 12000)
