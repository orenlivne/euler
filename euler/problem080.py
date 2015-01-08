'''
============================================================
http://projecteuler.net/problem=80

It is well known that if the square root of a natural number is not an integer, then it is irrational. The decimal expansion of such square roots is infinite without any repeating pattern at all.

The square root of two is 1.41421356237309504880..., and the digital sum of the first one hundred decimal digits is 475.

For the first one hundred natural numbers, find the total of the digital sums of the first one hundred decimal digits for all the irrational square roots.
============================================================
'''
from itertools import imap
import sympy

def decimals1(x):
    '''A genertor of decimals of x>=1.'''
    b, a = x, int(x)
    while True:
        b = 10 * (b - a)
        if b < 1e-15: return
        a = int(b)
        yield a

decimals = lambda x, d: imap(int, ''.join(str(sympy.N(x, d + 10)).split('.'))[:d])  # First d digits of x, for 0<=x<1
sum_irrational_decimals = lambda d: sum(decimals) if len(decimals) > 1 else 0 

if __name__ == "__main__":
    # print sum(d for n in xrange(1, 101) for d in islice(decimals1(n ** 0.5), 100))  # Wrong
    for n in xrange(1, 101):
        print n, len(list(decimals(sympy.sqrt(n), 100))), sum(decimals(sympy.sqrt(n), 100)), list(decimals(sympy.sqrt(n), 100))
    print sum(d for n in xrange(1, 101) for d in decimals(sympy.sqrt(n), 100) if n ** 0.5 > int(n ** 0.5))
