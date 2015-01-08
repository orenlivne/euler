'''
============================================================
http://projecteuler.net/problem=216

Consider numbers t(n) of the form t(n) = 2n2-1 with n > 1.
The first such numbers are 7, 17, 31, 49, 71, 97, 127 and 161.
It turns out that only 49 = 7*7 and 161 = 7*23 are not prime.
For n <= 10000 there are 2202 numbers t(n) that are prime.

How many numbers t(n) are prime for n <= 50,000,000 ?
============================================================
'''
import numpy as np
from problem007 import primes
from itertools import dropwhile
from problem058 import is_prime

def sqrt_mod(a, p):
    '''Return the square-root of a modulo p for a prime p.'''
    s, p1, h, m = 0, p - 1, (p - 1) / 2, p - 1
    while m % 2 == 0: s, m = s + 1, m / 2  # Write p = 2^s * m + 1 where m is odd
#    print 'm', m, 's', s
    z = long(dropwhile(lambda z: pow(z, h, p) != p1, xrange(p)).next())  # Find a nonresidue z. Smaller is better to reduce the subsequent pow() calls' complexity
#    print 'z', z
    c, u, v = pow(z, m, p), pow(a, m, p), pow(a, (m + 1) / 2, p)
#    print u, v, c
    # print 2 ** np.arange(s - 2, -1, -1, dtype=np.long)
    for i in [long(2 ** x) for x in xrange(s - 2, -1, -1)]:
        if pow(u, i, p) == p1: u, v = (u * c * c) % p, (v * c) % p
        c = (c * c) % p
#        print u, v, c
    return v

def sq_primes(N):
    '''Return the list of primes of the form 2*n**2-1 for 1<n<=N.'''
    P = map(long, primes('lt', int(2 ** 0.5 * N) + 1)[1:])  # t(n) is always odd so omit divisibility-by-2 check
    s = np.zeros((N + 1,), dtype=bool)
    s[:] = True; s[:2] = False
    for p in P:
        print 'p', p
        h = (p + 1) / 2
        if pow(h, (p - 1) / 2, p) == 1:
            a = sqrt_mod(h, p)
#            print '\t', 'h', h, 'a', a
            for q in (a, p - a):
#                print '\t', 'q', q, 'Sieving', range((p + q) if (2 * q * q - 1 == p) else q, len(s), p)
                s[(p + q) if (q * q == h) else q::p] = False
#     print 's', s
#     print 'n', np.where(s)[0]
    return map(lambda n: 2 * n * n - 1, np.where(s)[0])

if __name__ == "__main__":
    # print sqrt_mod(83L, 673L)
    # print sqrt_mod(9, 17)
    # N = 10000
    N = 50000000
    # t_bf = [2 * x * x - 1 for x in xrange(1, N + 1) if is_prime(2 * x * x - 1)]
    # print len(t_bf), t_bf
    t = sq_primes(N)
    print len(t)  # , t
