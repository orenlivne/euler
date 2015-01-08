'''
============================================================
http://projecteuler.net/problem=234

For an integer n >= 4, we define the lower prime square root of n, denoted by lps(n), as the largest prime <= sqrt n and the upper prime square root of n, ups(n), as the smallest prime >= sqrt n.

So, for example, lps(4) = 2 = ups(4), lps(1000) = 31, ups(1000) = 37.
Let us call an integer n >= 4 semidivisible, if one of lps(n) and ups(n) divides n, but not both.

The sum of the semidivisible numbers not exceeding 15 is 30, the numbers are 8, 10 and 12.
15 is not semidivisible because it is a multiple of both lps(15) = 3 and ups(15) = 5.
As a further example, the sum of the 92 semidivisible numbers up to 1000 is 34825.

What is the sum of all semidivisible numbers not exceeding 999966663333 ?
============================================================
'''
from __future__ import division
import itertools as it
from problem012 import Primes
from problem007 import primes
from math import ceil

'''integer-valued ceiling of an integer.'''
int_ceil = lambda x: int(ceil(x))

def primes_encompassing(N):
    '''Return the list of primes covering [2,N]. There's one more prime larger than
    N in the returned list.'''
    for p in Primes():
        yield p
        if p > N: break
    
'''Sum of b + (b+1) + ... + e.'''
arithmetic_sum = lambda b, e: (e + b) * (e - b + 1) // 2

def upper_bound(a, b):
    '''Upper bound (e) of multiple.'''
    q, r = divmod(a, b)
    return q if r else q - 1

'''Closed-form formula for multiples of l in the interval (l,t**0.5) (if t=None, in (l,u)).''' 
S1 = lambda l, u, t: l * arithmetic_sum(l + 1, upper_bound(u * u if t is None else t, l))
'''Closed-form formula for multiples of u in the interval (l,t**0.5) (if t=None, in (l,u)).''' 
S2 = lambda l, u, t: u * arithmetic_sum(int_ceil((l * l) / u), u - 1 if t is None else upper_bound(t, u))
'''Closed-form formula for multiples of l*u in the interval (l,t**0.5) (if t=None, in (l,u)).''' 
S3 = lambda l, u, t: l * u * arithmetic_sum(int_ceil(l / u), u // l if t is None else upper_bound(t, l * u))

def sum_semi_divisible(N):
    P, count = map(long, primes_encompassing(N ** 0.5)), 0  # Primes start at 2 <==> n>=4 so that's good
    num_p = len(P)
    for i in xrange(num_p - 1):  # Loop over [l,u] intervals
        l, u = P[i], P[i + 1]
        t = None if (i < num_p - 2) else (N + 1)  # Truncate last interval so that we don't consider n > N
        count += (S1(l, u, t) + S2(l, u, t) - 2 * S3(l, u, t))  # Since we counted l*u multiples twice (once in S1, once in S2), remove them twice since they are not semidivisible
    return count

'''Brute-force implementation, for validation on small problem sizes.'''
def is_semi_divisible(n, P):
    s = n ** 0.5
    if s == int(s): return False
    i, u = it.dropwhile(lambda (_, x): x < s, enumerate(P)).next()
    l = P[i - 1]
    result = ((n % l) == 0) ^ ((n % u) == 0)
    return result  

def sum_semi_divisible_bf(N):
    P = primes('lt', 2 * N ** 0.5)
    return sum(n for n in xrange(4, N + 1) if is_semi_divisible(n, P))

if __name__ == "__main__":
    for N in [15, 1000]:
        print N, sum_semi_divisible_bf(N), sum_semi_divisible(N)
    print sum_semi_divisible(999966663333)
