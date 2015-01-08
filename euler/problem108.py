'''
============================================================
http://projecteuler.net/problem=108

In the following equation x, y, and n are positive integers.

1/x+1/y=1/n

For n = 4 there are exactly three distinct solutions: ...

What is the least value of n for which the number of distinct solutions exceeds one-thousand?

NOTE: This problem is an easier version of problem 110; it is strongly advised that you solve this one first.
============================================================
'''
from numpy import prod
from itertools import count, dropwhile
from problem012 import factorize

def min_n(S):
    '''Brute-force, not terribly efficient. See Problem 110 for a better method.'''
    s = 2 * S + 1
    return dropwhile(prod(lambda n: prod([2 * k + 1 for k in factorize(n).itervalues()]) <= s), count(2)).next()

if __name__ == "__main__":
    print min_n(1000)
