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
from math import log, exp

def p(k, n):
    '''Calculate the probability p(k,n) using the complement of the event and summing over all possibilities
    for dealing defects to chips with exactly l chips with a pair of defects and k-l for single defect.
    Take log of appropriately grouped terms to avoid round-off cancellation errors.''' 
    a = cumsum([log((k - s) / (s + 1)) for s in xrange(k)])
    b = cumsum([log((k - s) / (2 * n)) for s in xrange(k)])
    c = cumsum([log(1 - s / n) for s in xrange(k)])
    return 1 - sum(exp(((a[l - 1] + b[2 * l - 1] - b[l - 1]) if l > 0 else 0) + c[k - l - 1]) for l in xrange(k // 2 + 1))

if __name__ == "__main__":
    print '%.10f' % (p(3, 7),)
    print '%.10f' % (p(2 * 10 ** 4, 10 ** 6),)
