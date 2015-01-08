'''
============================================================
http://projecteuler.net/problem=187

A composite is a number containing at least two prime factors. For example, 15 = 3  5; 9 = 3  3; 12 = 2  2  3.

There are ten composites below thirty containing precisely two, not necessarily distinct, prime factors: 4, 6, 9, 10, 14, 15, 21, 22, 25, 26.

How many composite integers, n  108, have precisely two, not necessarily distinct, prime factors?
============================================================
'''
from problem007 import primes
from itertools import takewhile
from math import ceil
from problem012 import factorize

def num_comp2(N):
    p_limit = int(ceil(N - 1) ** 0.5)
    P = primes('lt', int(ceil(N - 1) * 0.5) + 1)  # Sorted ascending
    return sum(sum(1 for _ in takewhile(lambda q: q <= q_limit, P[k:])) 
               for (k, q_limit) in ((k, N / p) for k, p in enumerate(takewhile(lambda p: p <= p_limit, P)))) 

num_comp2_bf = lambda N: sum(1 for (_, f) in ((n, factorize(n)) for n in xrange(2, N))  # @UnusedVariable
                             if (len(f) == 2 and f.values() == [1, 1]) or
                             (len(f) == 1 and f.values() == [2]))
    
if __name__ == "__main__":
    print num_comp2(10 ** 8)
