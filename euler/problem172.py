'''
============================================================
http://projecteuler.net/problem=172

How many 18-digit numbers n (without leading zeros) are there such that no digit occurs more than three times in n?
============================================================
'''
from itertools import islice
from problem203 import binom
import numpy as np

class NumCounter(object):
    '''Counts number of numbers of a certain #digits, with at most d occurrences of each decimal digit 0-9.''' 
    def __init__(self, n_max):
        '''Allocate memoization and binomial coefficient arrays for up to n = n_max digits in the number.'''
        self._b = list(islice(binom(), n_max + 1))
        # Memoization array. x[n,i] = # n-digit numbers composed of the digits i through 9
        # that satisfy the problem constraints (i.e. no digit appears more than d times.
        # The condition only affects the DP's initial condition, so it is set in the num_numbers() 
        # call below and this memo can be reused for multiple d values given n_max.
        # a -1 value indicates that the entry has not been computed yet.
        self._x = -np.ones((n_max + 1, 10), dtype=long)
        self._x[1, :] = np.arange(10, 0, -1)  # Initial condition #1
    
    def x(self, n, i, d):
        '''Dynamic programming.'''
        cached = self._x[n, i]
        if cached < 0:
            a = n if i > 0 else n - 1
            self._x[n, i] = sum(self._b[a][k] * self.x(n - k, i + 1, d) for k in xrange(min(d, a) + 1))
        return self._x[n, i]

    def num_numbers(self, n, d):
        '''Main call that calculates the number of n-digit numbers with at most d occurrences of
        each decimal digit.'''
        self._x[:d + 1, 9] = 1  # Initial condition #2
        self._x[d + 1:, 9] = 0  # Initial condition #2
        return self.x(n, 0, d)  # DP root call
    
if __name__ == "__main__":
    c = NumCounter(18)
    for n in xrange(1, 19):
        print n, c.num_numbers(n, 3)
