'''
============================================================
http://projecteuler.net/problem=047

The first two consecutive numbers to have two distinct prime factors are:

14 = 2  7
15 = 3  5

The first three consecutive numbers to have three distinct prime factors are:

644 = 2^2  7  23
645 = 3  5  43
646 = 2  17  19.

Find the first four consecutive integers to have four distinct prime factors. What is the first of these numbers?
============================================================
'''
import itertools as it, numpy as np
from problem012 import factorize, Primes

#-----------------------------------------------
# IMPLEMENTATION #1: SLOW
#-----------------------------------------------
def first_in_seq(L, limit=None):
    '''Will run indefinitely if a sequence of size L does not exist.'''
    y = 1
    for x in (it.count(2) if limit is None else xrange(2, limit + 1)):
        if x % 10000 == 0:
            print x
        # if is_not_admissible(x, L):
        if len(set(factorize(x).keys())) != L:
            y = x
        if x - y == L:  # L consecutive successes
            return y + 1
    return None

def is_not_admissible(x, L):
    count = 0
    for p in Primes():
        if x <= 1:
            break
        if x % p == 0:
            count += 1
            if count > L:
                return True
            x /= p
            while x % p == 0: x /= p  # itertools.divmod() faster?
    return count != L

#-----------------------------------------------
# IMPLEMENTATION #2: SIEVING
#-----------------------------------------------
def num_factors(limit):
    '''Return an array with the number of factors of the integers 0..limit-1. 0,1 are dummy entries.'''
    n = np.zeros((limit,), dtype=np.byte)  # more than 256 distinct prime factors is a LOT
    for x in xrange(2, limit):
        if n[x] == 0:  # x is prime
            n[x::x] += 1  # y is divisible by x <==> y = ax for some a
    return n 

first_in_seq_sieve = lambda n, L: it.dropwhile(lambda x: np.any(n[x - L + 1:x + 1] != L), xrange(max(L, 2), len(n))).next() - L + 1

if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
    print first_in_seq(1)  # 2
    print first_in_seq(2)  # 14
    print first_in_seq(3)  # 644

    # Slow
#     print first_in_seq(4)
#     import cProfile, pstats
#     cProfile.run('print first_in_seq(4, 40000)', 'problem047')
#     p = pstats.Stats('problem047').strip_dirs()
#     p.sort_stats('cumulative').print_stats(50)
    
    n = num_factors(1000000)
    for L in xrange(1, 5):
        print first_in_seq_sieve(n, L)
