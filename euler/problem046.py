'''
============================================================
http://projecteuler.net/problem=046

It was proposed by Christian Goldbach that every odd composite number can be written as the sum of a prime and twice a square.

9 = 7 + 2*1^2
15 = 7 + 2*2^2
21 = 3 + 2*3^2
25 = 7 + 2*3^2
27 = 19 + 2*2^2
33 = 31 + 2*1^2

It turns out that the conjecture was false.

What is the smallest odd composite that cannot be written as the sum of a prime and twice a square?
============================================================
'''
import math, itertools as it
from problem007 import primes

is_int = lambda x: x - int(x) < 1e-15

def min_counterexample(limit):
    p = primes('lt', limit)
    is_composable = lambda x: any(it.imap(lambda y : is_int(math.sqrt((x - y) / 2)), 
                                          it.takewhile(lambda y: y < x, p)))
    return it.dropwhile(is_composable, it.chain.from_iterable(xrange(p[k] + 2, p[k + 1], 2) 
                                                              for k in xrange(1, len(p) - 1))).next()
                                     
if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
    print min_counterexample(1000000)
