'''
============================================================
http://projecteuler.net/problem=231

The binomial coefficient 10C3 = 120.
120 = 23 x 3 x 5 = 2 x 2 x 2 x 3 x 5, and 2 + 2 + 2 + 3 + 5 = 14.
So the sum of the terms in the prime factorisation of 10C3 is 14. 

Find the sum of the terms in the prime factorisation of 20000000C15000000.
============================================================
'''
from itertools import takewhile
from problem007 import primes
from problem160 import C

S_fac = lambda n, p: sum(x * C(n, x) for x in takewhile(lambda x: x <= n, p))

def S_binom(n, k):
    p = map(long, primes('lt', n + 1))
    return S_fac(n, p) - S_fac(n - k, p) - S_fac(k, p)

if __name__ == "__main__":
    print S_binom(2 * 10 ** 7L, 15 * 10 ** 6L)
