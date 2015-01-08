'''
============================================================
http://projecteuler.net/problem=157

Consider the diophantine equation 1/a+1/b= p/10n with a, b, p, n positive integers and a <= b.
For n=1 this equation has 20 solutions that are listed below:

1/1+1/1=20/10    1/1+1/2=15/10    1/1+1/5=12/10    1/1+1/10=11/10    1/2+1/2=10/10
1/2+1/5=7/10    1/2+1/10=6/10    1/3+1/6=5/10    1/3+1/15=4/10    1/4+1/4=5/10
1/4+1/20=3/10    1/5+1/5=4/10    1/5+1/10=3/10    1/6+1/30=2/10    1/10+1/10=2/10
1/11+1/110=1/10    1/12+1/60=1/10    1/14+1/35=1/10    1/15+1/30=1/10    1/20+1/20=1/10
How many solutions has this equation for 1 <= n <= 9?
============================================================
'''

from numpy import prod, log

'''A useful n-k proportion constant.''' 
PHI = log(2) / log(5)

def num_factors(n, a, b, c, d):
    #print n, (a, b, c, d), (2 ** a * 5 ** b , 2 ** c * 5 ** d) 
    f = factorize(2 ** a * 5 ** b + 2 ** c * 5 ** d)
    #print 2 ** a * 5 ** b + 2 ** c + 5 ** d, f
    f[2] = (f[2] if f.has_key(2) else 0) + n - a - c
    f[5] = (f[5] if f.has_key(5) else 0) + n - b - d
    #print f
    return prod([v + 1 for v in f.itervalues()])
    
num_solutions = lambda n: sum(num_factors(n, a, b, c, d)
                              for a in xrange(n + 1)
                              for b in xrange(n + 1)
                              for c in xrange(n - a + 1)
                              for d in xrange(n - b + 1)
                              if PHI * (a - c) <= d - b)
                              
#------------- DP Solution - Broken ----------------
import numpy as np, itertools as it
from problem012 import factorize
from problem007 import primes
from problem207 import is_int  # @UnusedImport

def factors(n, P):  # assuming n > 1
    '''Return set of factors of n that are co-prime with 2 and 5. P = prime list to use for factorization.'''
    # print 'n', n
    d = factorize(n, P)
    d_filtered = [(k, v) for k, v in d.iteritems() if k != 2 and k != 5] if d else []
    if not d_filtered: return set([1, n] if n != 2 and n != 5 else [1])
    keys, values, m = [f[0] for f in d_filtered], [f[1] for f in d_filtered], len(d_filtered)
    # print 'n', n, 'd', d, d_filtered, keys, values, 'm', m
    # print list(it.product(*(xrange(v + 1) for v in values)))
    return set([np.prod([keys[i] ** combo[i] for i in xrange(m)]) for combo in it.product(*(xrange(v + 1) for v in values))])

'''List of (a,p) pairs.'''
ap_pairs = lambda L, n, P: set([((L * n) / p, p) for p in factors(n, P)])
ap_pairs_term1 = lambda L, p_list: set([(L, p) for p in p_list])
ap_pairs_term2 = lambda L, n, p_list: set([((L * n) / p, p) for p in p_list])

'''For debugging only.'''
F_num = lambda N, K: np.array([[2 ** n * 5 ** k + 1 for k in xrange(K + 1)] for n in xrange(N + 1)])

'''F1(n,k) = set of factors of 2^n 5^k + 1 that are co-prime with 2 and 5. 0 <= n <= N, 0 <= k <= K.
This is term 1 of t (a not | b case).'''
F1 = lambda N, K, P: np.array([[reduce(set.union,
                                       (ap_pairs_term1(2 ** a, factors(2 ** a * 5 ** b + 2 ** (a - x) * 5 ** (b - y), P))
                                        for a in xrange(n + 1)  for b in xrange(k + 1)
                                        for x in xrange(int(np.ceil(2 * a - n)), a + 1)
                                        for y in xrange(int(np.ceil(2 * b - k)), min(b, int(np.floor(-PHI * x))) + 1)
                                        if x > 0 or y > 0),
                                       set()) for k in xrange(K + 1)] for n in xrange(N + 1)])

'''F2(n,k) = set of factors of 2^n 5^k + 1 that are co-prime with 2 and 5. 0 <= n <= N, 0 <= k <= K.
This is term 2 of t (a|b case).'''
F2 = lambda N, K, P: np.array([[factors(2 ** n * 5 ** k + 1, P) for k in xrange(K + 1)] 
                               for n in xrange(N + 1)])

'''G(n,k) = set of factors of (5^k+1)/2^(-n) that are co-prime with 5. n=-1,...,N+1, 0 <= k <= K.'''
G = lambda N, K, P: np.array([[set() if (5 ** k + 1) % 2 ** (-n) else  
                               ap_pairs(5 ** k, (5 ** k + 1) / 2 ** (-n), P) for k in xrange(K + 1)] 
                               for n in xrange(-1, N, -1)])

'''H(n,k) = set of factors of (2^n+1)/5^(-k) that are co-prime with 2. 0 <= n < N, k=-1,...,K+1.'''
H = lambda N, K, P: np.array([[set() if (2 ** n + 1) % 5 ** (-k) else  
                               ap_pairs(2 ** n, (2 ** n + 1) / 5 ** (-k), P) for k in xrange(-1, K, -1)] 
                               for n in xrange(N + 1)])

'''Union form of the second f-term of t.'''
F1_reduced = lambda f: np.vectorize(len)(f)
F2_reduced = lambda f: np.array([[len(reduce(set.union, (ap_pairs_term2(2 ** (n - a) * 5 ** (k - b), 2 ** a * 5 ** b + 1, f[a, b])
                                                         for a in xrange(n + 1) for b in xrange(k + 1)),
                                            set())) for k in xrange(f.shape[0])] for n in xrange(f.shape[1])])

def cummulative_union(N, K, P, f):
    '''Cumulative-union array of an 2-D array-of-set functor f, starting from the (0,0) element and
    accumulating along the n and k axes.'''
    t = f(N, K, P)
    a, b = t.shape
    print 'f', f, 't\n', np.flipud(t)
    n = 0
    for k in xrange(1, b): t[n, k] |= t[n, k - 1]
    for n in xrange(1, a):
        for k in xrange(1, b): t[n, k] |= t[n, k - 1]
    return np.vectorize(len)(t) if t.size else np.empty((a, b), dtype=object)

def s_bf(n, k):
    L = float(2 ** n * 5 ** k)
    max_a = 2 * int(L) if n >= 0 and k >= 0 else (5 ** k if k >= 0 else (2 ** n if n >= 0 else 1))
    return [(a, int(round(b)), p) for a, b, p in ((a, 1. / (p / L - 1. / a), p) for a in xrange(1, max_a + 1) for p in xrange(1, int(L * (a + 1) / a) + 1) if np.abs(p - L / a) > 1e-12) if b >= a and is_int(b)] 

pad = lambda a: np.pad(a, ((1, 0), (1, 0)), mode='constant', constant_values=((0, 0), (0, 0)))

def num_solutions_dp(N):
    result = 0
    K = N
    P = primes('lt', int(0.5 * (2 ** N * 5 ** K + 1)) + 1)
    print 'P', P
    
    N1 = -2  # int(np.floor(-1 - K * phi))
    K1 = -2  # int(np.floor(-(N + 1) / phi))
    print 'N1', N1, 'to N', N, 'x', 'K1', K1, 'to K', K
    
    # f_union = cummulative_union(N, K, P, F)
    f1 = F1(N, K, P)
    f2 = F2(N, K, P)
    f1_reduced = F1_reduced(F1(N, K, P))
    f2_reduced = F2_reduced(F2(N, K, P))
    f_union = f1_reduced + f2_reduced
    print 'F1\n', np.flipud(f1)
    print 'F2\n', np.flipud(f2)
    print 'F1_reduced\n', np.flipud(f1_reduced)
    print 'F2_reduced\n', np.flipud(f2_reduced)
    print 'F_reduced\n', np.flipud(f_union)
    
    g_union = cummulative_union(N1, K, P, G)
    # print 'g_union\n', np.flipud(g_union)
    
    h_union = cummulative_union(N, K1, P, H)
    # print 'h_union\n', np.flipud(h_union)
    
    t = np.zeros((N - N1 + 1, K - K1 + 1), dtype=int)
    t[-N1:, -K1:] = f_union
    t[1:-N1, -K1:] = np.flipud(g_union)
    t[-N1:, 1:-K1] = np.fliplr(h_union)
    print 't\n', np.flipud(t)
    
    s = np.zeros((N - N1 + 1, K - K1 + 1), dtype=long)
    for n in xrange(1, N - N1 + 1):
        for k in xrange(1, K - K1 + 1):
            if n >= 0 and k >= 0:  s[n, k] = s[n - 1, k] + s[n, k - 1] - s[n - 1, k - 1] + t[n, k]
            elif n < 0 and k >= 0: s[n, k] = s[n, k - 1] + t[n, k]
            elif k < 0 and n >= 0: s[n, k] = s[n - 1, k] + t[n, k]
            else: s[n, k] = 0
        if n >= -N1:
            result += s[n, n + N1 - K1]
            # print 'n', n, 'result', result
    print 's\n', np.flipud(s)
    return result

if __name__ == "__main__":
    print num_solutions(0)
    print num_solutions(1)
    print num_solutions(2)
#     n = 1
#     for x in [(
#             (a, b, c, d),
#             2 ** (n - a - c) * 5 ** (n - b - d) * (2 ** a * 5 ** b + 2 ** c * 5 ** d),
#             num_factors(n, a, b, c, d)) 
#            for a in xrange(n + 1)
#            for b in xrange(n + 1)
#            for c in xrange(n - a + 1)
#            for d in xrange(n - b + 1)
#            if PHI * (a - c) <= d - b]:
#         print x
    print sum(num_solutions(n) for n in xrange(10))
    
#     np.set_printoptions(linewidth=1000)
#     S_bf = np.array([[len(s_bf(n, k)) for k in xrange(-2, 4)] for n in xrange(-2, 4)])
#     print 'S_BF\n', np.flipud(S_bf)
#     # print num_solutions(1)
#     print num_solutions(3)
#     P = primes('lt', 100)
# 
#     a = s_bf(2, 1)
#     print 'F1 set'
#     for x in a:
#         if gcd(x[2], 2) == 1 and gcd(x[2], 5) == 1 and x[1] % x[0] != 0: print x
#     print 'F2 set'
#     for x in a:
#         if gcd(x[2], 2) == 1 and gcd(x[2], 5) == 1 and x[1] % x[0] == 0: print x
#     n, k = 2, 1
#     print [(a, 0.5 * (k + PHI * (n - 2 * a))) for a in xrange(n + 1)]
#     print F1(2, 2, P)[2, 1]
