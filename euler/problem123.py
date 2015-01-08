'''
============================================================
http://projecteuler.net/problem=123

Let r be the remainder when (a1)n + (a+1)n is divided by a2.

For example, if a = 7 and n = 3, then r = 42: 63 + 83 = 728  42 mod 49. And as n varies, so too will r, but for a = 7 it turns out that rmax = 42.

For 3  a  1000, find sum of rmax.
============================================================
'''
from problem012 import Primes
from itertools import dropwhile

min_n = lambda R: dropwhile(lambda (n, p): (2 * n * p if n % 2 else 2) <= R, enumerate(Primes(), 1)).next()[0]

if __name__ == "__main__":
    print min_n(10 ** 10)
