'''
============================================================
http://projecteuler.net/problem=7

By listing the first six prime numbers: 2, 3, 5, 7, 11, and 13, we can see that the 6th prime is 13.

What is the 10 001st prime number?

Created on Feb 21, 2013
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
import numpy as np, math, itertools as it

def primes(bound, value):
    '''Return a list of the first value primes (value >= 1), if bound='first'.
    Return a list of the all primes < value, if bound='lt'.

    >>> primes('first', 10001)[-1]
    104743

    >>> primes('first', 1000)[-1]
    7919

    >>> len(primes('lt', 1000))
    168

    >>> len(primes('lt', 1000000))
    78498
    '''
    p, n_min = np.array([], np.int), 2
    if bound == 'first': n_max, cond, trim = 3 * value, lambda p: len(p) < value, lambda p: p[:value]
    elif bound == 'lt': n_max, cond, trim = int(math.ceil(math.log(value))) + 2, lambda p: not p.size or p[-1] < value, lambda p: p[np.where(p < value)[0]]  # Ensure n_max >= 2
    else: raise ValueError('Unrecognized bound type')
    
    while cond(p):
        p = np.append(p, primes_in_range(n_min, n_max, p))
        n_min = n_max
        n_max = 2 * n_min
    return trim(p)

def primes_in_range(n_min, n_max, p):
    '''Return a list of the primes in the range [n_min,n_max) given the list p of all primes < n_min.'''
    candidate = np.empty((n_max - n_min,), dtype=np.bool)
    candidate.fill(True)  # Initially, all are potentially prime
    for b in it.chain(p, xrange(n_min, int(math.floor(math.sqrt(n_max))) + 1)):
        # Remove multiples of b from candidate list
        i = b - n_min
        if b < n_min or candidate[i]:
            r = n_min % b
            # TODO: 
            # - Restrict start to at least b^2, since any smaller multiple of b has
            #   a smaller prime divisor < p, thus has already been crossed out
            # - Also, can step by 2*b, since all other b-multiples are even.
            # - Use a boolean array a instead of 
            start = (b - r) if r > 0 else 0
            if start == i:
                start += b
            candidate[np.where(candidate[start::b])[0] * b + start] = False
    return n_min + np.where(candidate)[0]

if __name__ == "__main__":
    import doctest
    doctest.testmod()
