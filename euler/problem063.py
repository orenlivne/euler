'''
============================================================
http://projecteuler.net/problem=63

The 5-digit number, 16807=75, is also a fifth power. Similarly, the 9-digit number, 134217728=89, is a ninth power.

How many n-digit positive integers exist which are also an nth power?
============================================================
'''
from math import ceil, log

if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
    print sum(10 - int(ceil(10 ** (1 - 1. / n))) for n in xrange(1, int(1. / (1 - log(9) / log(10))) + 1))
