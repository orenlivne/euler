'''
============================================================
http://projecteuler.net/problem=141

A positive integer, n, is divided by d and the quotient and remainder are q and r respectively. In addition d, q, and r are consecutive positive integer terms in a geometric sequence, but not necessarily in that order.

For example, 58 divided by 6 has quotient 9 and remainder 4. It can also be seen that 4, 6, 9 are consecutive terms in a geometric sequence (common ratio 3/2).
We will call such numbers, n, progressive.

Some progressive numbers, such as 9 and 10404 = 1022, happen to also be perfect squares.
The sum of all progressive perfect squares below one hundred thousand is 124657.

Find the sum of all progressive perfect squares below one trillion (1012).
============================================================
'''
from numpy import prod
from itertools import product
from problem012 import factorize
from problem086 import is_int
from euler.problem005 import gcd

def prog_sq(N):
    '''Return the set of progressive perfect squares <= N.'''
    result = set([])
    for q in xrange(2, int((N / 2.) ** (2. / 3.)) + 1):
        factors, Q = factorize(q), q * q * q
        P, c_max = map(long, factors.keys()), min(int(Q ** 0.5), q)
        # print 'q', q, 'q^3', Q, factors, 'c_max', c_max
        for K in product(*(xrange(3 * k + 1) for k in factors.itervalues())):
            c = prod([p ** k for p, k in zip(P, K)])
            if c <= c_max:
                # print '\t', c, Q / c
                a2 = c + Q / c
                if a2 <= N and is_int(a2 ** 0.5):
                    # print 'Found', 'q', q, 'q^3', Q, 'c', c, 'd', Q / c, 'n', a2, ' =', int(a2 ** 0.5), '^ 2'
                    d = (a2 - c) / q
                    print 'Found', 'n', a2, ' =', int(a2 ** 0.5), '^ 2 =', 'q', q, 'd', d, 'r', c, 'd**0.5', d ** 0.5, '(d/2)**0.5', (d / 2.) ** 0.5 
                    result.add(a2)
    return result

def prog_sq2(N):
    '''Return the set of progressive perfect squares <= N.'''
    result = set([])
    for a in xrange(2, int((N - 1) ** (1. / 3.)) + 1):
        a3 = a ** 3
        for b in (b for b in xrange(1, min(a, int(0.5 * ((a3 * a3 + 4 * N) ** 0.5 - a3)) + 1)) if gcd(a, b) == 1):
            ab, b2 = a3 * b, b * b
            for k in xrange(1, int((b ** 4 + 4 * N * ab) ** 0.5 - b2) / (2 * ab) + 1):
                n = k * (k * ab + b2)
                if int(n ** 0.5) ** 2 == n:
                    print 'n', '=', int(n ** 0.5), '^ 2'
                    result.add(n)
            
    return result

if __name__ == "__main__":
#     print sum(prog_sq(10 ** 5 - 1))
#     print sum(prog_sq(10 ** 12 - 1))
    print sum(prog_sq2(10 ** 5 - 1))
    print sum(prog_sq2(10 ** 12 - 1))
    
