'''
============================================================
http://projecteuler.net/problem=204

A Hamming number is a positive number which has no prime factor larger than 5.
So the first few Hamming numbers are 1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15.
There are 1105 Hamming numbers not exceeding 108.

We will call a positive number a generalised Hamming number of type n, if it has no prime factor larger than n.
Hence the Hamming numbers are the generalised Hamming numbers of type 5.

How many generalised Hamming numbers of type 100 are there which don't exceed 109?
============================================================
'''
from problem007 import primes
from itertools import takewhile
from problem012 import factorize

'''A dynamic programming solution.'''
class HammingCounter(object):
    def __init__(self, max_k): self.h, self.p = {}, primes('lt', max_k + 1)
    def H_of_prime(self, n, k): return self.H(n, sum(1 for _ in takewhile(lambda p:p <= k, self.p)) - 1)
    def H(self, n, k): return self.h.setdefault((n, k), self._H(n, k))
    def _H(self, n, k):
        if n == 1 or k < 0: return 1
        h, km, p = 0, k - 1, self.p[k]
        while n:
            h += self.H(n, km)
            n /= p
        return h

num_hamming = lambda n, k: HammingCounter(k).H_of_prime(n, k)

'''Brute-force counting.'''
num_hamming_bf = lambda n, k: sum(1 for x in xrange(2, n + 1) if max(factorize(x).iterkeys()) <= k) + 1
hamming_bf = lambda n, k: [1] + [x for x in xrange(2, n + 1) if max(factorize(x).iterkeys()) <= k]
    
if __name__ == "__main__":
    print hamming_bf(15, 5)
    print num_hamming(15, 5), num_hamming_bf(15, 5)
    print num_hamming(10000, 100), num_hamming_bf(10000, 100)
    print num_hamming(10 ** 8, 5)
    print num_hamming(10 ** 9, 100)
    print num_hamming(10 ** 10, 100)
