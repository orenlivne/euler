'''
============================================================
http://projecteuler.net/problem=23

A perfect number is a number for which the sum of its proper divisors is exactly equal to the number. For example, the sum of the proper divisors of 28 would be 1 + 2 + 4 + 7 + 14 = 28, which means that 28 is a perfect number.

A number n is called deficient if the sum of its proper divisors is less than n and it is called abundant if this sum exceeds n.

As 12 is the smallest abundant number, 1 + 2 + 3 + 4 + 6 = 16, the smallest number that can be written as the sum of two abundant numbers is 24. By mathematical analysis, it can be shown that all integers greater than 28123 can be written as the sum of two abundant numbers. However, this upper limit cannot be reduced any further by analysis even though it is known that the greatest number that cannot be expressed as the sum of two abundant numbers is less than this limit.

Find the sum of all the positive integers which cannot be written as the sum of two abundant numbers.

Created on Feb 21, 2013
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
import numpy as np
from problem021 import DCalculator

def abundant(n):
    '''Return the list of abundant numbers less than n. Sorted ascending.'''
    D = DCalculator(n)
    a = np.arange(n)
    d = np.array([D.d(x) for x in a])
    return np.where(d > a)[0] # Boundary cases a=0,1 not included in returned list since d[a]=a for them - OK

def sieve_sum2(n, a):
    '''Return the list of numbers < n that cannot be written as the sum of two elements from a.
    Brute-force implementation.'''
    e = np.zeros((n,), dtype=np.bool)
    e.fill(False)
    for p in a[:(n + 1) / 2]: # Search half of the pairs - symmtry
        e[p + a[np.where(p + a < n)[0]]] = True
    return np.where(~e)[0]

if __name__ == "__main__":
    np.set_printoptions(threshold=np.nan)
    n = 28123
    a = abundant(n)
    print a
    print a[np.where(a % 2)[0]]
    print sum(sieve_sum2(n, a))
#    import doctest
#    doctest.testmod()
