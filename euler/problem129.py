'''
============================================================
http://projecteuler.net/problem=129

A number consisting entirely of ones is called a repunit. We shall define R(k) to be a repunit of length k; for example, R(6) = 111111.

Given that n is a positive integer and GCD(n, 10) = 1, it can be shown that there always exists a value, k, for which R(k) is divisible by n, and let A(n) be the least such value of k; for example, A(7) = 6 and A(41) = 5.

The least value of n for which A(n) first exceeds ten is 17.

Find the least value of n for which A(n) first exceeds one-million.
============================================================
'''
import itertools as it
from problem005 import gcd
from problem007 import primes
from math import log

def A(n):
    x, p = 1, 9 * n
    for k in it.count(1):
        x = (10 * x) % p
        if x == 1: return k

def min_a_with_A_ge(N):
    '''Return the minimum n for which A(N)>=N.'''
    logN = log(N) / log(3)
    if logN < int(logN) + 1e-12: return N  # N is a power of 3
    p_low = 3 ** (int(logN))
    p_high = 3 * p_low
    p = primes('lt', p_high)
    p = p[p > p_low]
    
    lim = lambda P: it.dropwhile(lambda (n, a): a != n - 1, ((n, A(n)) for n in P)).next()[0]
    # Find largest prime 3^[log3(N)] < p_min <= N such that A(n)=n-1
    try: p_min = lim(reversed(p[p <= N]))
    except StopIteration: p_min = p_high
    # Find smallest prime N <= p_max < 3^([log3(N)]+1) such that A(n)=n-1
    try: p_max = lim(p[p >= N])
    except StopIteration: p_max = p_high
    
    # Search between p_min and p_max 
    return it.dropwhile(lambda (_, a): a < N, ((n, A(n)) for n in xrange(p_min, p_max + 1) if gcd(n, 10) == 1)).next()[0]
    
if __name__ == "__main__":
    print min_a_with_A_ge(10 ** 6 + 1)
    # print min_a_with_A_ge_brute_force(10 ** 6 + 1)
    # print dropwhile(lambda (n, a): a <= 10, ((n, A(n)) for n in count(1) if gcd(n, 10) == 1)).next()[0]
    # print dropwhile(lambda (n, a): a <= 1000000, ((n, A(n)) for n in count(1) if gcd(n, 10) == 1)).next()[0]

# def min_a_with_A_ge_brute_force(N):
#     '''Return the minimum n for which A(N)>=N. Brute-force search for all n.'''
#     a_max = 0
#     for n in it.ifilter(lambda n: gcd(n, 10) == 1, it.count(1)):
#         a = A(n)
#         if a > a_max:
#             a_max = a
#             print n, a  # , is_prime(n)
#         if a >= N: return n
