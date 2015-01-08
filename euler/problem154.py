'''
============================================================
http://projecteuler.net/problem=154

A triangular pyramid is constructed using spherical balls so that each ball rests on exactly three balls of the next lower level.


Then, we calculate the number of paths leading from the apex to each position:

A path starts at the apex and progresses downwards to any of the three spheres directly below the current position.

Consequently, the number of paths to reach a certain position is the sum of the numbers immediately above it (depending on the position, there are up to three numbers above it).

The result is Pascal's pyramid and the numbers at each level n are the coefficients of the trinomial expansion (x + y + z)n.

How many coefficients in the expansion of (x + y + z)**200000 are multiples of 10**12?
============================================================
'''
import itertools as it, time, numpy as np
from problem148 import binom

#--------------- Brute force ---------------
def trinom(N):
    b = list(it.islice(binom(), 0, N + 1)) 
    return (b[N][k] * b[N - k][l] for k in xrange(N + 1) for l in xrange(N - k + 1))

def num_divisible_bf(N, M):
    '''Brute-force calculation.'''
    r = 10 ** M
    return sum(1 for y in trinom(N) if y % r == 0)

#--------------- Pruned Brute force ---------------
def num_divisors(n, p):
    '''Number of times the prime p appears in the prime factorization of n!. Non-recursive implementation.'''
    s = 0
    while n:
        n /= p
        s += n
    return s

num_factors = lambda n, p: [num_divisors(k, p) for k in xrange(n + 1)]

def num_divisible_bf1(n, m):
    a, b = num_factors(n, 2), num_factors(n, 5)
    an, bn = a[n], b[n]
    return sum(1 for k in xrange(n + 1) for l in xrange(n - k + 1) 
               if an - a[k] - a[l] - a[n - k - l] >= m 
               and bn - b[k] - b[l] - b[n - k - l] >= m)

def num_divisible_bf2(n, m):
    a, b = num_factors(n, 2), num_factors(n, 5)
    an, bn, s = a[n] - m, b[n] - m, 0
    for k in xrange(n + 1):
        c, d = an - a[k], bn - b[k]
        if c >= 0 and d >= 0:
            s += sum(1 for l in xrange(n - k + 1) if a[l] + a[n - k - l] <= c and b[l] + b[n - k - l] <= d)
        if k % 100 == 0: print k, s
    return s

def num_divisible_bf3(n, m):
    a, b = num_factors(n, 2), num_factors(n, 5)
    an, bn, s = a[n] - m, b[n] - m, 0
    for k in xrange(n + 1):
        nk = n - k
        c, d = an - a[k], bn - b[k]
        if c >= 0 and d >= 0:
            lim = nk / 2 + 1 if nk % 2 else nk / 2
            s += 2 * sum(1 for l in xrange(lim) if a[l] + a[nk - l] <= c and b[l] + b[nk - l] <= d)
            if nk % 2 == 0:
                l = nk / 2
                if a[l] + a[nk - l] <= c and b[l] + b[nk - l] <= d: s += 1
        if k % 100 == 0: print k, s
    return s

def num_divisible_bf4(n, m):
    a, b = num_factors(n, 2), num_factors(n, 5)
    g = group_by(a, b)
    ga, gb = g.shape
    an, bn, s = a[n] - m, b[n] - m, 0
    for k in xrange(n + 1):
        c, d = an - a[k], bn - b[k]
        if c >= 0 and d >= 0:
            for A, B in it.product(xrange(min(ga, c + 1)), xrange(min(gb, d + 1))):
                C, D = c - A, d - B
                if C >= 0 and D >= 0:
                    for l in g[A, B]:
                        if l > n - k: break
                        if a[n - k - l] <= C and b[n - k - l] <= D: s += 1
    return s

def group_by(a, b):
    '''Return a hash table of 0..len(a)-1 by (a,b) value.'''
    a_max, b_max = max(a), max(b)
    g = np.zeros((a_max + 1, b_max + 1), dtype=np.object)
    for i, j in it.product(xrange(a_max + 1), xrange(b_max + 1)): g[i, j] = list()
    for k in xrange(n): g[a[k], b[k]].append(k)
    return g
    
if __name__ == "__main__":
    n = 200000
    m = 12

    # print list(trinom(n))
#    start = time.time()
#    print num_divisible_bf(n, m)
#    print time.time() - start, 'sec'
#
#    start = time.time()
#    print num_divisible_bf1(n, m)
#    print time.time() - start, 'sec'
#
#    start = time.time()
#    print num_divisible_bf2(n, m)
#    print time.time() - start, 'sec'

    start = time.time()
    print num_divisible_bf3(n, m)
    print time.time() - start, 'sec'

#    print num_divisible(2, 1)
    # print num_divisible(200000, 12)
#     for n in xrange(1, 21):
#         t = trinom(n)
#         #print t
#         print n, len(t), len(set(t))        



# def num_factors(N, p):
#    c = np.array([num_divisors(k, p) for k in xrange(N + 1)])
#    return c[N] - c - c[-1::-1]
#
# def num_divisible(N, M):
#    s, t, M1 = num_factors(N, 2), num_factors(N, 5), M - 1
#    print 'N', N, 'M', M
#    print 's', s
#    print 't', t
#    print 'Total trinomials', (N + 1) * (N + 2) / 2
#    tot = (N + 1) * (N + 2) / 2
#    for k in np.where((s < M) & (t < M))[0]:
#        print 'k', k
#        u = num_terms_le(N - k, M1 - s[k], M1 - t[k])
#        print 'u', u
#        tot -= u
#    return tot
#    # return (N + 1) * (N + 2) / 2 - sum(num_terms_le(N - k, M1 - s[k], M1 - t[k]) for k in np.where((s < M) & (t < M))[0])
#
# def num_terms_le(n, S, T):
#    print '\t', 'num_terms_le(n=%d, S=%d, T=%d)' % (n, S, T)
#    d = {}
#    s, t = num_factors(n, 2), num_factors(n, 5)
#    print '\t', 's', s
#    print '\t', 't', t
#    for k in xrange(n / 2 if n % 2 == 0 else n / 2 + 1):  # Utilize binomial symmetry across the k=n/2 point
#        key = (s[k], t[k])
#        d[key] = d.setdefault(key, 0) + 2
#    if n % 2 == 0:  # Central element
#        k = n / 2
#        key = (s[k], t[k])
#        d[key] = d.setdefault(key, 0) + 1
#    print '\t', d
#    return sum(v for ((s, t), v) in d.iteritems() if s <= S and t <= T)
