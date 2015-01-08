'''
============================================================
http://projecteuler.net/problem=27

Euler published the remarkable _quadratic formula:

n^2 + n + 41

It turns out that the formula will produce 40 primes for the consecutive values n = 0 to 39. However, when n = 40, 402 + 40 + 41 = 40(40 + 1) + 41 is divisible by 41, and certainly when n = 41, 41^2 + 41 + 41 is clearly divisible by 41.

Using computers, the incredible formula  n^2 - 79n + 1601 was discovered, which produces 80 primes for the consecutive values n = 0 to 79. The product of the coefficients, 79 and 1601, is 126479.

Considering _quadratics of the form:

n^2 + an + b, where |a|  1000 and |b|  1000

where |n| is the modulus/absolute value of n
e.g. |11| = 11 and |4| = 4
Find the product of the coefficients, a and b, for the _quadratic expression that produces the maximum number of primes for consecutive values of n, starting with n = 0.
Created on Feb 21, 2013
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
import numpy as np, problem021

def max_pair(a_max, b_max, n_min, max_iter=5, sieve=False):
    '''Return (a,b),number of n's with max n**2+a*n+b consecutive primes starting at n=0.
    Searches in the range |a|<=a_max,|b|<=b_max,assumes n_min<n and a unique maximizer (a,b).'''
    n, n_max, i = n_min, n_min, 0
    while n == n_max and i < max_iter:
        n_max *= 2  # Convenient growth factor thanks to the 80-consecutive-primes hint
        (a, b), n = _max_pair(a_max, b_max, n_min, n_max, sieve)
        i += 1
        print (a, b), n, n_max
    if n == n_max: raise ValueError('Did not ensure finding the maximum sequence within %d iterations' % (max_iter,))
    return (a, b), n

def _max_pair(a_max, b_max, n_min, n_max, sieve):
    '''A helper method, assumes n_min <n < n_max.'''
    # Prime list, reused for b list and _quadratics primailty tests
    primes = problem021.primes('lt', _quad(a_max, b_max, n_max) + 1)
    # A-sieve allocated once per all b-values. Faster, but a slightly increases storage.
    a_start = _min_a(b_max, n_max - 1)
    # print 'a_start', a_start
    # print 'a_max', a_max
    a_size = a_max - a_start
    A = np.zeros((a_size,), dtype=np.bool)
    
    res, n_res = (0, 0), -1
    for b in primes:
        if b >= b_max:
            break
        # print 'b', b
        
        # Search for max prime sequence among remaining A-values
        # where the _quadratic is positive for -this- b value 
        A.fill(True)
        this_start = _min_a(b, n_max - 1)
        # print 'this_start', this_start
        A[0:this_start - a_start] = False
        # print A
        
        # Sieve using further conditions
        if sieve:
            bp = b + 1
            print np.where(A)[0]
            for k in xrange(2, n_min + 2):  # Sieve a-values based on (1),k=n+1
                _sieve(A, a_start, a_size, bp % k, k)
                print '(1) k', k, np.where(A)[0]
            
            for k in xrange(2, n_min + 2):  # Sieve a-values based on (1),k=n+1
                _sieve(A, a_start, a_size, (-bp) % k, k)
                print '(2) k', k, np.where(A)[0]
     
        # Search for max prime sequence among remaining A-values
        # where the _quadratic is positive for -this- b value 
        # print 'Final a-values', np.where(A)[0]
        for i in np.where(A)[0]:
            a = a_start + i
            # print 'i', i, 'a', a
            # Debugging mode - extra checks
            if sieve:
                for k in xrange(n_min + 1):
                    num = _quad(a, b, k)
                    print a, b, k, num
                    if not is_prime(num, primes):
                        raise ValueError('k=%d, num=%d is not prime but should be - sieving bug' % (k, num))
                
            k = n_min + 1 if sieve else 0
            num = _quad(a, b, k)
            # print '\t\tnum', num, 'is_prime', is_prime(num, primes)
            while is_prime(num, primes):
                k += 1
                num = _quad(a, b, k)
                # print '\t\tnum', num, 'is_prime', is_prime(num, primes)
            # print '\ta', a, 'b', 'k', k
            if k > n_res:
                res, n_res = (a, b), k
    if n_res < 0:
        raise ValueError('Did not find a pair with consecutive prime sequence length >= %d' % (n_min,))
    return res, n_res

def _quad(a, b, n):
    '''Return n**2+a*n+b.'''
    return n * (n + a) + b

def _sieve(a, a_start, a_size, offset, k):
    '''Sieve a-values based on a single modulus condition.'''
    s = offset if a_start % k <= offset else offset + k
    print 'k', k, 'offset', offset, 's', s
    a[np.arange(s - a_start, a_size, k)] = False

def _min_a(b, n):
    '''Minimum a s.t. k**2+a*k+1 > 1 for all k=0..n.'''
    nc = np.sqrt(b - 1)  # Critical n-value above which fmin(a) shifts from the quadratic region in to the linear region in a
    return int(np.ceil(1e-10 + (-2 * nc if n >= nc else (1 - n * n - b) / n)))

def is_prime(n, primes):
    '''Primality test. 1 <= n <= (max prime)^2. 1 is NOT prime.'''
    if n < 1: raise ValueError('Primality test supported only for n >= 1. n=%d passed in' % (n,))
    if n == 1: return False  # Standard convention
    if n <= 3: return True
    if n % 2 == 0: return False
    k = n % 6
    if k != 1 and k != 5: return False
    p_max = int(np.floor(np.sqrt(n)))
    for p in primes:
        if p > p_max: break
        if n % p == 0: return False
    return True

def max_pair_stuhr(b_max):
    '''Brilliant analysis by a person on the Euler project thread.'''
    n = int(np.floor(0.5 * (-1 + (1 + 4 * (b_max - 41)) ** 0.5)))
    a, b = -(2 * n + 1), n * (n + 1) + 41
    return (a, b), n
    
if __name__ == "__main__":
    (a, b), n = max_pair_stuhr(1000)
    print a, b, n, a * b
    (a, b), n = max_pair(1000, 1000, 40)
    print a, b, n, a * b
    # Broken
    # print max_pair(1000, 1000, 40, sieve=True)
    
    
