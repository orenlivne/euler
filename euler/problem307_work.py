'''
============================================================
http://projecteuler.net/problem=307

k defects are randomly distributed amongst n integrated-circuit chips produced by a factory (any number of defects may be found on a chip and each defect is independent of the other defects).

Let p(k,n) represent the probability that there is a chip with at least 3 defects.
For instance p(3,7) ~ 0.0204081633.

Find p(20 000, 1 000 000) and give your answer rounded to 10 decimal places in the form 0.abcdefghij
============================================================
'''
from __future__ import division
from numpy import cumsum
from math import log, exp, factorial
import itertools as it
from problem171 import occur_dict

def log_factorial(N):
    '''Return an array of log(n) values for n = 0..N.'''
    L = [0] * (N + 1)
    for n in xrange(2, N + 1): L[n] = L[n - 1] + log(n)
    return L

def p2(k, n):
    c = cumsum([log(1 - s / n) for s in xrange(k)])
    b = cumsum([log((k - s) / (2 * n)) for s in xrange(k)])
    a = cumsum([log((k - s) / (s + 1)) for s in xrange(k)])
    
    # print L
#    for l in xrange(k // 2 + 1):
#        print 'l', l, exp(L[n] + L[k] - k * log(n) - l * log2 - L[k - 2 * l] - L[n - k + l] - L[l])
    return 1 - sum(exp(((a[l - 1] + b[2 * l - 1] - b[l - 1]) if l > 0 else 0) + c[k - l - 1]) for l in xrange(k // 2 + 1))

def p(k, n):
    L, log2 = log_factorial(n), log(2)
    # print L
    for l in xrange(k // 2 + 1):
        print 'l', l, exp(L[n] + L[k] - k * log(n) - l * log2 - L[k - 2 * l] - L[n - k + l] - L[l])
    return 1 - sum(exp(L[n] + L[k] - k * log(n) - l * log2 - L[k - 2 * l] - L[n - k + l] - L[l]) for l in xrange(k // 2 + 1))

def d(k, n):
    L, log2 = log_factorial(n), log(2)
    return [exp(L[n] + L[k] - k * log(n) - l * log2 - L[k - 2 * l] - L[n - k + l] - L[l]) for l in xrange(k // 2 + 1)]

def p_direct(k, n):
    s = 0
    for l in xrange(k // 2 + 1):
        c = factorial(k) / (2 ** l * factorial(k - 2 * l) * factorial(l))
        d = factorial(n) / factorial(n - k + l)
        # print 'l', l, c, d
        s += c * d
    pp = 1 - s / n ** k
    # print 's', s, 'denominator', n ** k, 'p', pp
    return pp

def combos_bf(k, n, m=3):
    for x in it.product(*(xrange(1, n + 1) for _ in xrange(k))):
        d = occur_dict(x)
        if max(d.itervalues()) < m:
            yield x
#             d = occur_dict(x)
#             pairs, singles = [k for k, v in d.iteritems() if v == 2], [k for k, v in d.iteritems() if v == 1]
#             yield x, len(pairs), pairs, singles

p_bf = lambda k, n, m = 3: 1 - sum(1 for _ in combos_bf(k, n, m)) / n ** k

if __name__ == "__main__":
    for n in xrange(8):
        for k in xrange(1, n):
            a, b, c, d = p_bf(k, n), p_direct(k, n), p(k, n), p2(k, n)
            print 'n=%d k=%d %.15f %.15f %.15f %.15f' % (n, k, a, b, c, d)
    print '%.10f' % (p(3, 7),)
    print '%.10f' % (p(2 * 10 ** 4, 10 ** 6),)
    print '%.10f' % (p2(2 * 10 ** 4, 10 ** 6),)
