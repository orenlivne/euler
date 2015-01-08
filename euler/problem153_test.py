'''
============================================================
http://projecteuler.net/problem=153

============================================================
'''
import numpy as np, time
from problem005 import gcd
from numpy.testing.utils import assert_equal

#-------------------------------
# Real (rational) divisors
#-------------------------------
def sum_divisors_rational_formula_fast(n):
    '''Returns the sum of rational divisors of all numbers between 1 and n, inclusive. A fast
    implementation that decomposes the requested sum, sum_{a=1}^n a*floor(n/a) into local
    and smooth parts, because floor(n/.) becomes increasingly smoother for larger values of
    the argument. Runtime complexity: O(sqrt(n)).'''
    # Optimal split to balance local and smoth work
    q = int(n ** 0.5)
    # Local part
    s_local = sum(a * (n / a) for a in xrange(1L, n / q + 1))
    # Smooth part
    s_smooth = 0L
    for k in xrange(1L, q):
        r1, r2 = n / (k + 1), n / k
        # print '\t', r1, r2
        s_smooth += k * (r1 + r2 + 1) * (r2 - r1)
    s_smooth /= 2
    # print n, K, s_local, s_smooth
    
    return s_local + s_smooth

def sum_divisors_rational_formula(n):
    s = 0L
    for a in xrange(1L, n + 1):
        k = n / a
        s += a * k
    return s

def sum_divisors_rational(n):
    '''Return the sum of the number of rational and Gaussian divisors with positive real part
    of all k, k=1..n.'''
    d = np.zeros((n + 1,), dtype=long)
    # Real factors a
    for a in xrange(1, n + 1): d[a::a] += a
    return sum(d)

def sum_divisors_rational_func_bf(n):
    '''O(sqrt(n))-complexity brute force to find the sum of divisors of n.'''
    # if n % 10000 == 0: print n
    i, count = 2, 1 if n == 1 else (n + 1)  # accounts for 'n' and '1'
    while i ** 2 < n:
        if n % i == 0: count += (i + n / i)
        i += 1
    if i ** 2 == n: count += i
    return count

sum_divisors_rational_bf = lambda n: sum(sum_divisors_rational_func_bf(k) for k in xrange(1, n + 1))

#-------------------------------
# Complex divisors
#-------------------------------
def g_sum(n, p):
    '''Return the inner-most sum of complex Gaussian divisors with positive real part of all k, k=1..n.
    Using a summation formula. Runtime complexity: O(n^(1/2)).'''
    # Optimal split to balance local and smoth work
    q, s = int((n / p) ** 0.5), 0L
    # Local part
    for g in xrange(1L, n / (p * q) + 1):
        K = n / (p * g)
        # print 'g', g, 'K', K
        s += (K * g + K * (K + 1) / 2)
    # Smooth part
    for k in xrange(1L, q):
        r1, r2 = n / (p * (k + 1)), n / (p * k)
        # print '\t', r1, r2, 'k', k
        G = (r1 + r2 + 1) * (r2 - r1) / 2
        s += (k * G + k * (k + 1) * (r2 - r1) / 2)
    # print n, K, s_local, s_smooth
    return s

def g_sum_bf(n, p):
    s, N = 0L, n / p
    for g in xrange(1, N + 1):
        K = n / (p * g)
        # print K
        s += (K * g + K * (K + 1) / 2)
    return s
    
def sum_divisors_complex_formula(n):
    '''Return the sum of complex Gaussian divisors with positive real part of all k, k=1..n.
    Using a summation formula. Runtime complexity: O(n).'''
    s = 0L
    for a in xrange(1, int((n - 1) ** 0.5) + 1):
        a2, sa = a * a, 0L
        # print 'a', a, 'b_max', int((n - a2) ** 0.5)
        for b in (b for b in xrange(1, int((n - a2) ** 0.5) + 1) if gcd(a, b) == 1):
            N = n / (a2 + b * b)
            # print '\t', (a, b), 'N', N
            for g1 in xrange(1, N + 1):
                K = n / ((a2 + b * b) * g1)
                sa += (K * g1 + K * (K + 1) / 2)
                # print '\t\t', (a, b), 'g1', g1, 'K', K, 'term', a * (K * g1 + K * (K + 1) / 2)
        s += a * sa
    return s

'''Return the sum of complex Gaussian divisors with positive real part of all k, k=1..n.
Using a summation formula. Runtime complexity: O(n).'''
sum_divisors_complex_formula_fast2 = lambda n: \
sum(a * sum(g_sum(n, a * a + b * b) for b in xrange(1, int((n - a * a) ** 0.5) + 1) if gcd(a, b) == 1)
    for a in xrange(1, int((n - 1) ** 0.5) + 1))

def sum_divisors_complex_formula_fast(n):
    s = 0L
    print 'a_max', int((n - 1) ** 0.5)
    for a in xrange(1, int((n - 1) ** 0.5) + 1):
        a2 = a * a
        if (a % 100) == 0: print 'a', a, 'b_max', int((n - a2) ** 0.5)
        s += a * sum(g_sum(n, a * a + b * b) for b in xrange(1, int((n - a * a) ** 0.5) + 1) if gcd(a, b) == 1)
    return s

def sum_divisors_complex(n):
    '''Return the sum of complex Gaussian divisors with positive real part of all k, k=1..n.'''
    d = np.zeros((n + 1,), dtype=long)

    # Complex factors a+bi with a > 0; use symmetry b/-b
    # print 'a_max', int((n - 1) ** 0.5)
    for a in xrange(1, int((n - 1) ** 0.5) + 1):
        a2 = a * a
        # print 'a', a, 'b_max', int((n - 1 - a2) ** 0.5)
        for b in (b for b in xrange(1, int((n - a2) ** 0.5) + 1) if gcd(a, b) == 1):
            p0 = a2 + b * b
            for g in xrange(1, n / p0 + 1):
                p = p0 * g
                d[p] += p
                d[2 * p::p] += 2 * p
                # print '\t', (a, b), 'p', p, 'd', d
    # print np.arange(1, n + 1)
    # print d[1:]
    return sum(d)

def sum_divisors_func_complex_bf(n):
    '''Return the number of divisors a+bi of n with a,b integers and a > 0. A brute-force
    implementation.'''
    count = 0
    # print n
    for a in xrange(1, n + 1):
        for b in xrange(1, n + 1):
            p = a * a + b * b
            if (n * a) % p == 0 and (n * b) % p == 0:
                # print '\t', (a, b), 'p', p, 'c', n * a / p, 'term', a + n * a / p
                count += a + n * a / p
    return count

sum_divisors_complex_bf = lambda n: sum(sum_divisors_func_complex_bf(k) for k in xrange(1, n + 1))
sum_divisors_array_complex_bf = lambda n: np.array(map(sum_divisors_func_complex_bf, xrange(1, n + 1)))

#-------------------------------
# Total sum of divisors
#-------------------------------
sum_divisors_gaussian_bf = lambda n: sum_divisors_rational_bf(n) + sum_divisors_complex_bf(n)
sum_divisors_gaussian = lambda n: sum_divisors_rational_formula_fast(n) + sum_divisors_complex_formula_fast(n)

def test_sum_divisors_rational():
    for n in np.concatenate((np.arange(2L, 10L), 10L ** np.arange(1, 7)), axis=0):
        print 'n', n
        
        if n <= 10000:
            start = time.time()
            s1 = sum_divisors_rational(n)
            print 'BF', s1, 'time', time.time() - start, 'sec'

        start = time.time()
        s2 = sum_divisors_rational_formula(n)
        print 'Formula slow', s2, 'time', time.time() - start, 'sec'

        start = time.time()
        s3 = sum_divisors_rational_formula_fast(n)
        print 'Formula fast', s3, 'time', time.time() - start, 'sec'
        print ''

        if n <= 10000:
            assert_equal(s1, s3, 'Fast evaluation does not match BF')
        assert_equal(s2, s3, 'Fast evaluation does not match linear-time formula')

def test_sum_divisors_complex():
    for n in np.arange(2L, 200L):
        print 'n', n
        
        if n <= 10000:
            start = time.time()
            s1 = sum_divisors_complex_bf(n)
            print 'BF', s1, 'time', time.time() - start, 'sec'
            # print sum_divisors_array_complex_bf(n)

#         start = time.time()
#         s2 = sum_divisors_complex(n)
#         print 'Sieve', s2, 'time', time.time() - start, 'sec'

        start = time.time()
        s3 = sum_divisors_complex_formula_fast(n)
        print 'Formula fast', s3, 'time', time.time() - start, 'sec'

        if n <= 10000:
            assert_equal(s3, s1, 'Complex divisor sum formula does not match BF for n = %d' % (n,))
        # assert_equal(s3, s2, 'Complex divisor sum does not match formula')
        print '-' * 80
    
def test_sum_divisors_gaussian():
    '''Test entire sum-of-Gaussian-divisors vs. a brute-force implementation.'''
    for n in np.concatenate((np.arange(2, 201), 10 ** np.arange(1, 4)), axis=0):
        if n <= 100: s1 = sum_divisors_gaussian_bf(n)
        start = time.time()
        s2 = sum_divisors_gaussian(n)
        t2 = time.time() - start
        
        if n <= 100:
            print 'n', n, 'bf', s1, 'fast', s2
            if s1 != s2:
                print sum_divisors_array_complex_bf(n)
                raise ValueError('Wrong value in fast method')
                # print '#' * 30, 'Wrong value in fast method'
        else:
            print 'n', n, 's_bf', s2, 'time', t2, 'sec'

def test_g_sum():
    n, p = 8, 2
    print g_sum(n, p)
    print g_sum_bf(n, p)
    assert_equal(g_sum(n, p), g_sum_bf(n, p), 'Wrong fast g_sum result')
 
if __name__ == "__main__":
#    test_g_sum()
#    test_sum_divisors_rational()
#    test_sum_divisors_complex()
    test_sum_divisors_gaussian()
    print sum_divisors_gaussian(10L ** 8)
