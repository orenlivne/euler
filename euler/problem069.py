'''
============================================================
http://projecteuler.net/problem=69

Euler's Totient function, phi(n) [sometimes called the phi function], is used to determine the number of numbers less than n which are relatively prime to n. For example, as 1, 2, 4, 5, 7, and 8, are all less than nine and relatively prime to nine, phi(9)=6.

n    Relatively Prime    phi(n)    n/phi(n)
2    1    1    2
3    1,2    2    1.5
4    1,3    2    2
5    1,2,3,4    4    1.25
6    1,5    2    3
7    1,2,3,4,5,6    6    1.1666...
8    1,3,5,7    4    2
9    1,2,4,5,7,8    6    1.5
10    1,3,7,9    4    2.5
It can be seen that n=6 produces a maximum n/phi(n) for n  10.

Find the value of n  1,000,000 for which n/phi(n) is a maximum.
============================================================
'''
import numpy as np, itertools as it

def primes(n):
    '''Return all primes <= n.'''
    s = np.ones((n + 1,), dtype=np.bool); s[0:2] = False  # Sieving array. First two entries are dummy.
    for p in xrange(2, int(n ** 0.5) + 1): s[2 * p::p] = False
    return np.where(s)[0]

'''Return the number <= n for which n/phi(n) attains its maximum. Runs in about O(1) time.'''
argmax_phi_rat = lambda n: list(it.takewhile(lambda x: x <= n, np.cumprod(primes(int(2 * np.log(n))))))[-1]

if __name__ == "__main__":
    print argmax_phi_rat(1000)  # 510510
    import timeit 
    for n in 10 ** np.arange(1, 7):
        print '%-8d %.2e' % (n, timeit.timeit('print argmax_phi_rat(%s)' % (n,), 'from __main__ import argmax_phi_rat', number=1))
