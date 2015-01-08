'''
============================================================
http://projecteuler.net/problem=77

It is possible to write ten as the sum of primes in exactly five different ways:

7 + 3
5 + 5
5 + 3 + 2
3 + 3 + 2 + 2
2 + 2 + 2 + 2 + 2

What is the first value which can be written as the sum of primes in over five thousand different ways?
============================================================
'''
import itertools as it
from problem007 import primes

def num_ways(n, terms):
    '''Return the number of ways to write each 0<=x<n as a sum of primes.'''
    w = [1] + [0] * (n - 1)
    for p in terms:
        for y in xrange(p, n): w[y] += w[y - p]
        print p, w
    return w

def first_num(terms, criterion, W, n_min):
    n = n_min(W)
    while True:
        try:
            return it.dropwhile(lambda (_, w): criterion(w, W), enumerate(num_ways(n, terms(n)))).next()[0]
        except StopIteration:
            n *= 2
    
if __name__ == "__main__":
    print first_num(lambda n: primes('lt', n), lambda w, W: w <= W, 5000, lambda W: max(W / 10, 5))
