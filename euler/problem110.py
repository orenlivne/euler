'''
============================================================
http://projecteuler.net/problem=110

In the following equation x, y, and n are positive integers.

1/x + 1/y= 1/n

It can be verified that when n = 1260 there are 113 distinct solutions and this is the least value of n for which the total number of distinct solutions exceeds one hundred.

What is the least value of n for which the number of distinct solutions exceeds four million?

NOTE: This problem is a much more difficult version of problem 108 and as it is well beyond the limitations of a brute force approach it requires a clever implementation.
(Same as http://projecteuler.net/problem=108 with S = four
million.)
============================================================
'''
from problem007 import primes
from problem012 import factorize
from math import log, ceil
from numpy import prod

def min_n_above(S):
    s = 2 * S + 1
    m = int(ceil(log(s) / log(3)))
    p = primes('first', m)
    fac, n, f = dict((x, factorize(x)) for x in xrange(1, p[-1])), prod([long(x) for x in p]), dict((x, 1) for x in p)
    while p.size:
        found, f0 = False, f.copy()
        del f0[p[-1]]
        for t in xrange(1, p[-1]):
            ft = f0.copy()
            for k, v in fac[t].iteritems(): ft[k] += v
            if prod([2 * k + 1 for k in ft.itervalues()]) > s:
                found, n, f, p = True, (n / p[-1]) * t, ft, p[:-1]
                break
        if not found: break
    return n

if __name__ == "__main__":
    print min_n_above(1000)
    print min_n_above(4 * 10 ** 6)
