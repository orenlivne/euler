'''
============================================================
http://projecteuler.net/problem=127

The radical of n, rad(n), is the product of distinct prime factors of n. For example, 504 = 23  32  7, so rad(504) = 2  3  7 = 42.

We shall define the triplet of positive integers (a, b, c) to be an abc-hit if:

GCD(a, b) = GCD(a, c) = GCD(b, c) = 1
a  b
a + b = c
rad(abc)  c
For example, (5, 27, 32) is an abc-hit, because:

GCD(5, 27) = GCD(5, 32) = GCD(27, 32) = 1
5  27
5 + 27 = 32
rad(4320) = 30  32
It turns out that abc-hits are quite rare and there are only thirty-one abc-hits for c < 1000, with c = 12523.

Find c for c < 120000.
============================================================
'''
import numpy as np
from euler.problem007 import primes
from euler.problem005 import gcd

def rad(N):
    '''Return an array of rad(n), 0 <= n < N.'''
    r = np.ones((N,), dtype=np.uint64)
    for p in primes('lt', N): r[p::p] *= p
    return r.tolist()

def abc_hit(N):
    '''Yield all abc-hits with c < N.'''
    r = rad(N)
    for a in xrange(1, (N - 1) / 2 + 1):
        if a % 100 == 0: print 'a', a
        for b in xrange(a + 1, N - a):
            c = a + b
            rab = r[a] * r[b]
            if rab < c and rab * r[c] < c and gcd(a, b) == 1: yield a, b, c
            
if __name__ == "__main__":
    print sum(c for (_, _, c) in abc_hit(120000))
