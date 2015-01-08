'''
============================================================
http://projecteuler.net/problem=70

Euler's Totient function, phi(n) [sometimes called the phi function], is used to determine the number of positive numbers less than or equal to n which are relatively prime to n. For example, as 1, 2, 4, 5, 7, and 8, are all less than nine and relatively prime to nine, phi(9)=6.
The number 1 is considered to be relatively prime to every positive number, so phi(1)=1.

Interestingly, phi(87109)=79180, and it can be seen that 87109 is a permutation of 79180.

Find the value of n, 1  n  107, for which phi(n) is a permutation of n and the ratio n/phi(n) produces a minimum.
============================================================
'''
import numpy as np
from problem069 import primes

def phi(n, prime_list=None):
    '''Return all values of phi(k), 0<=k<n. k=0,1 are dummy.'''
    c = np.arange(n, dtype=np.longlong); c[:2] = -1
    for p in (prime_list if prime_list is not None else primes(n)): c[p::p] /= p; c[p::p] *= (p - 1)
    return c

is_perm = lambda (x, y): ''.join(sorted(str(x))) == ''.join(sorted(str(y)))

def min_perm(n):
    f = phi(n)
    N = np.where(map(is_perm, enumerate(f)))[0]
    return N[np.argmin(N.astype(float) / f[N])] if N.size else 0

if __name__ == "__main__":
    for n in 10 ** np.arange(1, 8): print n, min_perm(n)  
