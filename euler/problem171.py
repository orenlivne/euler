'''
============================================================
http://projecteuler.net/problem=171

For a positive integer n, let f(n) be the sum of the squares of the digits (in base 10) of n, e.g.

f(3) = 32 = 9,
f(25) = 22 + 52 = 4 + 25 = 29,
f(442) = 42 + 42 + 22 = 16 + 16 + 4 = 36

Find the last nine digits of the sum of all n, 0 < n < 10**20, such that f(n) is a perfect square.
============================================================
'''
from problem092 import multinom
import numpy as np

def occur_dict(a):
    '''A dictionary of item occurrences in the iterable a.'''
    d = {}
    for x in a: d[x] = d.setdefault(x, 0) + 1
    return d

list_minus = lambda a, i: np.concatenate((a[:i], a[i + 1:]))
C = lambda a: multinom(len(a), occur_dict(a).values())
s_tilde = lambda a, r: ((10 ** min(len(a), r) - 1) / 9) * sum(long(b) * C(list_minus(a, i)) for b, i in zip(*np.unique(a, return_index=True)))

def ss(a, r): 
    '''Sum of all numbers that can be composed of the digits in a. a must be non-increasing.'''
    a = np.array(a, dtype=int)
    return (s_tilde(a, r) - (0 if a[0] else s_tilde(a[1:], r))) % 10L ** r 

is_square = lambda x: int(x ** 0.5) ** 2 == x
sum_mod = lambda seq, r: reduce(lambda x, y: (x + y) % r, seq, 0)
sum_ss_mod = lambda k_max, r: SSWays(int(9 * k_max ** 0.5) ** 2, k_max).sum_ss_mod(r)

class SSWays(object):
    def __init__(self, x_max, k_max):
        self._g = {}
        self._x_max = x_max
        self._k_max = k_max
    
    def g(self, x, k, b=9):
        if not self._g.has_key((x, k, b)):
            self._g[(x, k, b)] = [a + (c,) for c in xrange(min(b, int(x ** 0.5)) + 1) 
                             for a in self.g(x - c * c, k - 1, c)] \
                             if k >= 2 else ([(int(x ** 0.5),)] if x <= b * b and is_square(x) else [])
        return self._g[(x, k, b)]

    def sum_ss_mod(self, r):
        return sum_mod((ss(a, r) for y in xrange(1, int(self._x_max ** 0.5) + 1) 
                        for k in xrange(1, self._k_max + 1)
                        for a in self.g(y * y, k)), 10L ** r)
    
if __name__ == "__main__":
    print sum_ss_mod(20, 9)
