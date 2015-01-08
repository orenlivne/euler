'''
============================================================
http://projecteuler.net/problem=168

Consider the number 142857. We can right-rotate this number by moving the last digit (7) to the front of it, giving us 714285.
It can be verified that 714285=5 x 142857.
This demonstrates an unusual property of 142857: it is a divisor of its right-rotation.

Find the last 5 digits of the sum of all integers n, 10 < n < 10**100, that have this property.
============================================================
'''
from math import ceil
from problem005 import gcd

def cyclic_numbers(N):
    '''A generator of numbers who are divisors of their right-rotation in [10,10**N).'''
    for n, a in ((n, a) for n in xrange(2, N + 1) for a in xrange(1, 10)):
        U, V = 10 ** (n - 1) - a, 10 * a - 1
        d = gcd(U, V)
        u, v = U / d, V / d
        c_min, c_max = int(ceil(max(1. / v, 10.**(n - 2) / u))), min(9 / v, (10 ** (n - 1) - 1) / u)
        for c in xrange(c_min, c_max + 1): yield c * (10 * u + v)

'''Sum the r-moduli of all numbers of interest in [10,10**N).'''
sum_cyclic = lambda N, r: reduce(lambda x, y: (x + y) % r, cyclic_numbers(N))

if __name__ == "__main__":
    print sum_cyclic(100, 10 ** 5L)
