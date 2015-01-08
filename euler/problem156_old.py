'''
============================================================
http://projecteuler.net/problem=156

Starting from zero the natural numbers are written down in base 10 like this: 
0 1 2 3 4 5 6 7 8 9 10 11 12....

Consider the digit d=1. After we write down each number n, we will update the number of ones that have occurred and call this number f(n,1). The first values for f(n,1), then, are as follows:

n    f(n,1)
0    0
1    1
2    1
3    1
4    1
5    1
6    1
7    1
8    1
9    1
10    2
11    4
12    5
Note that f(n,1) never equals 3. 
So the first two solutions of the equation f(n,1)=n are n=0 and n=1. The next solution is n=199981.

In the same manner the function f(n,d) gives the total number of digits d that have been written down after the number n has been written. 
In fact, for every digit d != 0, 0 is the first solution of the equation f(n,d)=n.

Let s(d) be the sum of all the solutions for which f(n,d)=n. 
You are given that s(1)=22786974071.

Find  SUM s(d) for 1 <= d <= 9.

Note: if, for some n, f(n,d)=n for more than one value of d this value of n is counted again for every value of d for which f(n,d)=n.
============================================================
'''
import itertools as it
from math import log10, ceil
from numpy import abs

#---------------------------------------------
def num_digits(n):
    '''Return the number of digits in the decimal number n >= 1.'''
    k = log10(n)
    return (int(k) + 1) if k < int(k) + 1e-12 else int(ceil(k))

def f(d, n):
    if n == 0: return 0
    result, k = 0L, num_digits(n) - 1
    r = 10L ** k
    while k >= 0:
        p, q = divmod(n, r)
        result += (0 if k == 0 else p * k * (r / 10)) + (r if p > d else 0) + ((q + 1) if p == d else 0)
        k, r, n = k - 1, r / 10, q
    return result

def root_search(d, n, t, s):
    '''Brute-force linear root search starting at n and searching to the left (if s=-1)
    or the right (s=1).'''
    # print 'n', n, 'searching %s' % ('left' if s < 0 else 'right')
    while True:
        if n == 0: return
        gn = g(d, n)
        if gn == 0:
            #if n > 1: print 'solution', n
            yield n
        if abs(gn) >= t: return
        n += s

def centuries(p, n_max):
    if p % 10000 == 1: print '#' * 30, 'p', p, '#' * 30
    while p <= n_max:
        yield p
        p *= 10L
        
g = lambda d, n: f(d, n) - n
all_roots = lambda d, t = 500, p_max = 10L ** 7, n_max = 10L ** 11: \
set(n for p in (p for p in xrange(1, p_max + 1) if p % 10) \
    for m in centuries(p, n_max) \
    for s in (-1, 1) \
    for n in root_search(d, m, t, s))  # @UndefinedVariable

S = lambda d: sum(all_roots(d))

#---------------------------------------------
def root_search2(d, p, k, s, tol=100):
    '''Brute-force linear root search starting at p*10**k and searching to the left (if s=-1)
    or the right (s=1).'''
    n = p * 10L ** k + (-1 if s < 0 else 0)
    n_min = 0 if p == 1 and k == 1 else (p - 1 if k == 0 else (9 * 10L ** (k - 1) if p == 1 else (p - 1) * 10L ** k)) 
    n_max = (p + 1) * 10L ** k - 1
    # print 'Searching %d -> %d' % (n, n_max if s > 0 else n_min)
    gn = g(d, n)
    while abs(gn) <= tol:
        if gn == 0:
            print n 
            yield n
        n += s
        if n <= n_min or n >= n_max: return  # Should really be checked only for p=1,k=0
        gn = g(d, n)

all_roots2 = lambda d, k_max = 12, tol = 10: (n for k in xrange(1, k_max + 1) \
                                              for p in xrange(1, 10) \
                                              for s in (-1, 1) \
                                              for n in root_search(d, p, k, s, tol=tol))

#---------------------------------------------
import unittest, numpy as np
from numpy.ma.testutils import assert_equal

def f_bf(d):
    f = 0L
    yield f
    for n in it.count(1):
        f += sum(1 for x in map(int, str(n)) if x == d)
        yield f

def f_century(d, k, p):
    '''Return f(p*10**k-1). Exact formula obtained by solving a recurrence relation.'''
    f = 0 if k == 0 else p * k * 10L ** (k - 1)
    if p > d: f += 10L ** k
    return f

def f_recursive(d, n):
    if n == 0: return 0
    k = num_digits(n) - 1
    p, q = divmod(n, 10L ** k)
    return f_century(d, k, p) + f(d, q) + ((q + 1) if p == d else 0)

class TestProblem156(unittest.TestCase):
    #---------------------------------------------
    # Constants
    #---------------------------------------------
    
    #---------------------------------------------
    # Setup Methods
    #---------------------------------------------
    def setUp(self):
        '''Init brute-force array of f-values.'''
        self.K = 3
        self.n_max = 10 ** (self.K + 1)
        self.F = [[]] + [list(it.islice(f_bf(d), 0, self.n_max)) for d in xrange(1, 10)]
        # Base.metadata.create_all(self.engine) 
        
    def tearDown(self):
        '''Drop the database.'''
        pass
    
    #---------------------------------------------
    # Test Methods
    #---------------------------------------------
    def test_f_century(self):
        for d in xrange(1, 10):
            for k in xrange(self.K):
                for p in xrange(1, 11):
                    n = p * 10L ** k - 1
                    f1, f2 = self.F[d][n], f_century(d, k, p)
                    assert_equal(f2, f1, 'Wrong f evaluation at century number d=%d, k=%d, p=%d' % (d, k, p))

    def test_f_recursive(self):
        for d in xrange(1, 10):
            for n in xrange(self.n_max):
                f1, f2 = self.F[d][n], f_recursive(d, n)
                assert_equal(f2, f1, 'Wrong f recursive evaluation at d=%d, n=%d' % (d, n))

    def test_f_iterative(self):
        for d in xrange(1, 10):
            for n in xrange(self.n_max):
                f1, f2 = self.F[d][n], f(d, n)
                assert_equal(f2, f1, 'Wrong f iterative evaluation at d=%d, n=%d' % (d, n))

    def test_f_at_century_points(self):    
        d = 1
        # K = 6
        # n_max = 10 ** K
        # F = np.array([f(d, n) for n in xrange(n_max)])
        # F = np.array(list(it.islice(f_bf(d), 0, n_max)))
        for d in xrange(1, 10):
            print '-' * 80
            print 'd', d
            for k in xrange(100):
                for p in xrange(1, 11):
                    n = p * 10L ** k - 1
                    fc = f_century(d, k, p)
                    if fc <= (p + 1) * 10L ** k - 1:
                        print 'k', k, 'p', p, n, fc, fc - n
        
def secant(f, x0, x1, tol):
    '''Secant method for f(x)=0, starting from x0,x1.'''
    if abs(x0 - x1) < tol: return 0.5 * (x0 + x1)
    f0, f1 = f(x0), f(x1)
    print x0, x1, f0, f1
    while abs(x0 - x1) >= tol:
        x0, x1 = x1, (x0 * f1 - x1 * f0) / (f1 - f0)
        f0, f1 = f1, f(x1)
        print x0, x1, f0, f1
    return 0.5 * (x0 + x1)

#------ testing ------
def test_s_1():
    a = all_roots(1)
    for x in sorted(a):
        print x
    print sum(a)
    return a

G = lambda n: np.array([g(1,x) for x in n])

if __name__ == "__main__":
    pass
    # print sum(S(d) for d in xrange(1, 10))
#     for d in xrange(1, 10):
#         print 'd', d
#         print S(d)
    
