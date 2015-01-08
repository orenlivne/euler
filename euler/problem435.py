'''
============================================================
http://projecteuler.net/problem=435

The Fibonacci numbers {fn, n >= 0} are defined recursively as fn = fn-1 + fn-2 with base cases f0 = 0 and f1 = 1.

Define the polynomials {Fn, n >= 0} as Fn(x) = sum fixi for 0 <= i <= n.

For example, F7(x) = x + x2 + 2x3 + 3x4 + 5x5 + 8x6 + 13x7, and F7(11) = 268357683.

Let n = 1015. Find the sum [sum 0<=x<=100 Fn(x)] mod 1307674368000 (= 15!).
============================================================
'''
import numpy as np
from problem381 import inv_mod
from problem104 import Fib
from problem171 import sum_mod

def Fnx(n, m, x):
    '''Yields Fn(x) mod m for x,m s.t. gcd(1-x-x^2,m)=1.'''
    F = Fib(r=m)
    xn = pow(x, n, m)
    return (inv_mod(1 - x - x * x, m) * ((x * (1 - F(n + 1) * xn - F(n) * xn * x)) % m)) % m

def polyval_mod(a, x, m):
    '''Horner''s rule for evaluating the kth degree polynomial (a[0] + a[1]*x + ... + a[k-1]*x^(k-1)) mod m
    where k=len(a).'''
    y = a[-1] % m
    for i in xrange(len(a) - 2, -1, -1): y = (x * y + a[i]) % m
    return y

def Fnx_bf(n, m, x_max):
    '''Brute force [Fn(x) mod m]_{x=0..x_max} (a bit faster, taking advantage of modulo reductions).'''
    F = Fib(r=m)
    f = np.array([F(i) for i in xrange(n + 1)])
    return map(long, (polyval_mod(f, x, m) for x in xrange(x_max + 1)))

def non_coprime_sum_pattern(m, x_max, k_max=4):
    '''Run this once to get an idea of what the sum of Fnx is for a non-co-prime factor m of 15!
    for n=10^k, k=0,1,2,3,... .'''
    for n in 10 ** np.arange(k_max):
        fnx_bf = Fnx_bf(n, m, x_max)
        s_bf = sum_mod(fnx_bf, m)
        print 'n %6d s %5d' % (n, s_bf), 'BF fnx', fnx_bf  # Turn on debugging printouts to observe pattern
    return s_bf, m  # Assuming constant s_bf for large k

def crt(a):
    '''Returns the basic solution to the system x = a[i][0] (mod a[i][1]), i=0..len(a)-1 using the Chinese
    Remainder Theorem. All a[i][1] must be co-prime (although a weaker condition involving the a[i][0]''s is
    also sufficient for a solution, this implementation is not guaranteed to work for it).'''
    a, n = zip(*a)
    N = np.prod(map(long, n))
    return sum(a[i] * (N / n[i]) * inv_mod(N / n[i], n[i]) for i in xrange(len(a))) % N

'''Decompose 15! into factors with co-prime denominators (using division of Fn terms)
and factors with non-co-prime denominators (using patterns observed for n=10^k)
Solve for sum modulo 15! using the Chinese remainder theorem.'''
sum_fnx_mod_fifteen_factorial = lambda n, x_max: crt([(sum_mod((Fnx(n, m, x) for x in xrange(x_max + 1)), m), m)
                                                      for m in [2 ** 11, 3 ** 6, 7 ** 2, 13]] + [non_coprime_sum_pattern(m, x_max) for m in [5 ** 3, 11]])
    
if __name__ == "__main__":
    n = 10 ** 15
    print sum_fnx_mod_fifteen_factorial(10 ** 15, 100)
