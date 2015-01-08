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
import numpy as np
from collections import Counter
from itertools import product, izip

def to_alexandrian_set(triples):
    '''Convert (p,a=p+q,b=p+r) to a sorted list of Alexandrian integers.'''
    A = set()
    for p, a, b in triples:
        qr = (a - p) * (b - p)
        if qr > 0: A.add(p * qr)
        A.add(p * (a + p) * (b + p))
    return sorted(A)

def alexandrian_iter(n, triples_gen, p_init=10, p_fac=2.0):
    '''Return first n Alexandrian integers.'''
    p_max = p_init
    while True:
        A = to_alexandrian_set(triples_gen(p_max))
        if len(A) >= n: return A[:n]
        p_max = int(p_max * p_fac)

def shanks_sieve(L):
    '''Shanks sieve. Return the factors of n**2+1 for n=0,1,2,...,L as a list of prime power Counters.'''
    # Initialize arrays
    a, f = np.array([n * n + 1L for n in xrange(L + 1)], dtype=np.long), [Counter() for _ in xrange(L + 1)]
    # Boundary case of p=2
    a[1::2] /= 2L
    for n in xrange(1L, L + 1, 2L): f[n][2] += 1
    # A1 sieving passes
    for n in xrange(1L, L + 1):
        p = long(a[n])
        if p > 1:
            # Initialize with p-adic roots fpr p^k=p
            k, pk, A, B, h = 1, p, n, p - n, (((p + 1) / 2) * n) % p
            while A <= L or B <= L:
                for x in (A, B):
                    if x <= L:
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
        ab = p * p + 1L
        for a in (a for a in divisors(f) if a <= p): yield p, a, ab / a

def divisors(f):
    '''A generator of all divisors of n whose factorization is given by the prime power Counter f.'''
    if not f: return ()
    else:
        P, M = zip(*f.iteritems())
        return (long(np.prod([p ** k for p, k in izip(P, c)])) for c in product(*(xrange(m + 1) for m in M)))

alexandrian2 = lambda n: alexandrian_iter(n, triples_shanks, p_init=5 * n)

if __name__ == "__main__":
    print alexandrian2(6)[-1] # 630
    print alexandrian2(150000)[-1] # 1884161251122450
