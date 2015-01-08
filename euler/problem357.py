'''
============================================================
http://projecteuler.net/problem=357

Consider the divisors of 30: 1,2,3,5,6,10,15,30.
It can be seen that for every divisor d of 30, d+30/d is prime.

Find the sum of all positive integers n not exceeding 100 000 000
such that for every divisor d of n, d+n/d is prime.
============================================================
'''
from problem007 import primes
import numpy as np

def div_sums_bf(N):
    P = primes('lt', N + 2)
    return np.array([n for n in xrange(1, N + 1) if 
                     all(n / d + d in P for d in (d for d in xrange(1, n + 1) if n % d == 0))])
    
def div_sums(N):
    '''Returns an array of all n''s <= N such that n/d + d is prime if d|n.'''
    s, P = np.zeros((N + 2,), dtype=bool), primes('lt', N + 2)
    s.fill(False); s[1] = True; s[P] = True; n = P - 1
    print '|primes|', len(P) + 1
    for d in xrange(2, int(N ** 0.5) + 1):
        # print 'd', d, 'n', n, n / d + d, s[n / d + d]
        d2 = d * d
        if n[-1] < d2: break
        n = n[(n % d != 0) | s[n / d + d]]
        if d % 1000 == 0: print 'd', d, '|n|', len(n)
        
    return n

if __name__ == "__main__":
    print np.all(div_sums_bf(100) == div_sums(100))
    print sum(div_sums(10 ** 8))
