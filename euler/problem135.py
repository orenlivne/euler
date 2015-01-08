'''
============================================================
http://projecteuler.net/problem=135

Given the positive integers, x, y, and z, are consecutive terms of an arithmetic progression, the least value of the positive integer, n, for which the equation, x2  y2  z2 = n, has exactly two solutions is n = 27:

342  272  202 = 122  92  62 = 27

It turns out that n = 1155 is the least value which has exactly ten solutions.

How many values of n less than one million have exactly ten distinct solutions?
============================================================
'''
from __future__ import division
import numpy as np

def num_solutions(N):
    s = np.zeros((N,), dtype=np.uint)
    for x in xrange(1, N):
        if x % 100000 == 0: print x 
        s[(4 * np.arange(int(x / 4) + 1, min(x, int(np.ceil((N / x + x) / 4)))) - x) * x] += 1
    return s

if __name__ == "__main__":
    s = num_solutions(1156)
    print s[2], s[27], s[1155]
    print len(np.where(num_solutions(10 ** 6) == 10)[0])
