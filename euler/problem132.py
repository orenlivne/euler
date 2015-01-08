'''
============================================================
http://projecteuler.net/problem=132

A number consisting entirely of ones is called a repunit. We shall define R(k) to be a repunit of length k.

For example, R(10) = 1111111111 = 11412719091, and the sum of these prime factors is 9414.

Find the sum of the first forty prime factors of R(109).
============================================================
'''
#------------- My working byt slow solution ------------- 
# import itertools as it, numpy as np, operator
# from problem035 import is_prime
# from problem129 import A
# #from euler.problem012 import factorize
# #
# #def A(p):
# #    print 'p', p
# #    qs = [1, ]
# #    for f in factorize(p - 1).iteritems():
# #        qs = [q * f[0] ** j for j in xrange(1 + f[1]) for q in qs]
# #    for q in sorted(qs):
# #        if pow(10, q, p) == 1: break
# #    return q
#
# def first_factors(d, n):
#    fac, a_values = set([]), sorted(2 ** k * 5 ** l for k in xrange(d + 1) for l in xrange(d + 1) if k + l > 0)
#    print 'd', d, 'n', n, 'a_values', a_values
# #    P = [it.imap(operator.itemgetter(0), it.ifilter(lambda (p, ap): ap == p - 1,
# #                                                    ((p, A(p)) for p in it.ifilter(is_prime, (c * a + 1 for c in it.count(3 if a == 2 else (2 if a == 4 else 1)))))
# #                                                    )) for a in a_values]
#    p = lambda a: ((a, c * a + 1) for c in it.count(3 if a == 2 else (2 if a == 4 else 1)))
#    P = np.array([p(a) for a in a_values])
#    while P.size:
#        print 'len(P)', len(P), 'fac', fac
#        Q = [lst.next() for lst in P]
#        #print '\t', 'Q', Q
#        if len(fac) == n:
#            f_max = -iter(sorted(fac)).next()
#            #print '\t', 'f_max', f_max
#            admissible = map(operator.itemgetter(0), it.ifilter(lambda (_, (a, x)): x < f_max, enumerate(Q)))
#            Q = [Q[x] for x in admissible]
#            P = P[admissible]
#            #print '\t', 'admissible', admissible
#            #print '\t', 'After filtering too large', len(P), 'Q', Q
#        #print '\t', [(a, p, A(p)) for a, p in it.ifilter(lambda (a, p): is_prime(p), Q)]
#        Q = np.array(map(operator.itemgetter(1),
#                         it.ifilter(lambda (a, p, ap): ap == a,
#                                    ((a, p, A(p)) for a, p in it.ifilter(lambda (a, p): is_prime(p), Q)))))
#        #print '\t', 'Filtered Q', Q
#        for p in sorted(Q):
#            fac.add(-p)
#            if len(fac) == n:
#                break
#    return (-x for x in fac)
#
# if __name__ == "__main__":
#    print sum(first_factors(1, 4))
#    print sum(first_factors(9, 40))

# Solution based on the idea in http://www.mathblog.dk/project-euler-132-large-repunit-factors/
from itertools import islice
from problem012 import Primes

pfactors = lambda a, k: (p for p in Primes() if pow(a, k, int(9 * p)) == 1)

if __name__ == "__main__":
    print sum(islice(pfactors(10, 10), 4))
    print sum(islice(pfactors(10, 10 ** 9), 40))
    
