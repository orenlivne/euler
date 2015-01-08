'''
============================================================
http://projecteuler.net/problem=221

We shall call a positive integer A an "Alexandrian integer", if there exist integers p, q, r such that
A = pqr and 1/A=1/p+1/q+1/r.
For example, 630 is an Alexandrian integer (p = 5, q = -7, r = -18). In fact, 630 is the 6th Alexandrian integer,
the first 6 Alexandrian integers being: 6, 42, 120, 156, 420 and 630.

Find the 150000th Alexandrian integer.

============================================================
'''
from numpy import round

#-------------------------------
# My sieve
#-------------------------------
def triples_oren_sieve(p_max):
    '''Return the sequence of Alexandrian integers up to p=p_max in our parameterization.'''
    P = p_max * p_max + 1L
#    print 'P', P
    for a in xrange(1L, p_max):
#        print 'a', a
        for b in xrange(1L, P / a + 1):  # wasteful, go over relevant b's only near (1+p^2)'s
            ab = a * b
#             p = int(round((ab - 1L) ** 0.5))
#             c = p * p + 1L
#             print '\t', 'b', b, 'ab', ab, 'p', p, 'c', c, c == ab 
            if ab > 1:
                p = int(round((ab - 1L) ** 0.5))
                c = p * p + 1L
                if c == ab:
                    yield p, a, b

def to_alexandrian_set(triples):
    A = set()
    for p, a, b in triples:
        qr = (a - p) * (b - p)
        if qr > 0: A.add(p * qr)
        A.add(p * (a + p) * (b + p))
    print 'Unsorted length', len(A)
    return sorted(A)

def to_alexandrian_records(triples):
    A = set()
    for p, a, b in triples:
        qr = (a - p) * (b - p)
        if qr > 0: A.add((p * qr, tuple(sorted((p, a - p, b - p)))))
        A.add((p * (a + p) * (b + p), tuple(sorted((p, -a - p, -b - p)))))
    return sorted(A)

def alexandrian_iter(n, triples_gen, p_init=10, p_fac=2.0, output='A'):
    '''Return the nth Alexandrian integer. n is 1-based.'''
    alexandrian_output = to_alexandrian_set if output == 'A' else to_alexandrian_records
    p_max = p_init
    while True:
        A = alexandrian_output(triples_gen(p_max))
        # A = to_alexandrian_set(triples_gen(p_max))
        print p_max, len(A)
        if len(A) >= n: return A[:n]  # return A[n - 1]
        p_max = int(p_max * p_fac)

alexandrian1 = lambda n, p_init = 10, p_fac = 2.0, output = 'A': alexandrian_iter(n, triples_oren_sieve, p_init=p_init, p_fac=p_fac, output=output)

#-------------------------------
# Shanks sieve
#-------------------------------
import numpy as np
from collections import Counter
from itertools import product, izip

def shanks_sieve(L):
    '''Shanks sieve. Return the factors of n**2+1 for n=0,1,2,...,L as a list of prime power Counters.'''
    print 'L', L
    # Initialize arrays
    a, f = np.array([n * n + 1L for n in xrange(L + 1)], dtype=np.long), [Counter() for _ in xrange(L + 1)]
    # Boundary case of p=2
    a[1::2] /= 2L
    for n in xrange(1L, L + 1, 2L): f[n][2] += 1
    # A1 sieving passes
    for n in xrange(1L, L + 1):
        p = long(a[n])
        if n % (L / 10) == 0: 
            print 'n', n, 'a[n]', a[n], n * n + 1L
        if p > 1:
            # Initialize with p-adic roots fpr p^k=p
            k, pk, A, B, h = 1, p, n, p - n, (((p + 1) / 2) * n) % p
            while A <= L or B <= L:
                # print '\t', 'k', k, 'p^k', pk, 'Ak', A, 'Bk', B
                for x in (A, B):
                    if x <= L:
                        # print '\t\t', 'x', x
                        # Prevent xrange third argument overflow if sieve contains only one term (x)
                        if x <= L - pk: 
                            a[x::pk] /= p
                            for l in xrange(x, L + 1, pk): f[l][p] += 1
                        else:
                            a[x] /= p
                            f[x][p] += 1
                # Advance p-adic roots to next power of p (there are always exactly 2 roots)
                C = (h * (A * A + 1) / pk) % p
                A += C * pk
                pk *= p
                k += 1
                B = pk - A
    return f

def triples_shanks(L):
    for p, f in enumerate(shanks_sieve(L)):
        if p % 10000 == 0: print 'p', p
        ab = p * p + 1L
        for a in (a for a in divisors(f) if a <= p): yield p, a, ab / a

def divisors(f):
    '''A generator of all divisors of n whose factorization is given by the prime power Counter f.'''
    if not f: return ()
    else:
        P, M = zip(*f.iteritems())
        return (long(np.prod([p ** k for p, k in izip(P, c)])) for c in product(*(xrange(m + 1) for m in M)))

alexandrian2 = lambda n, output = 'A': alexandrian_iter(n, triples_shanks, p_init=5 * n, output=output)

#-------------------------------
# Testing
#-------------------------------
from fractions import Fraction
ZERO = Fraction(0L, 1L)
def is_alexandrian(A, (p, q, r)):
    return A == p * q * r and (Fraction(1L, p) + Fraction(1L, q) + Fraction(1L, r) - Fraction(1L, A) == ZERO)

is_all_alexandrian = lambda a: all(is_alexandrian(A, (p, q, r)) for (A, (p, q, r)) in a)

def test_alexandrian_fast_vs_oren_sieve():
    N = 200
    a = alexandrian1(N, p_init=80, output='record')
    b = alexandrian2(N, output='record')
    print a
    print b
    print a == b
    print is_all_alexandrian(a)
    print is_all_alexandrian(b)

if __name__ == "__main__":
    # test_alexandrian_fast_vs_oren_sieve()
    print alexandrian2(6)[-1]
    print alexandrian2(1000)[-1]
    print alexandrian2(10000)[-1]
    print alexandrian2(150000)[-1]
