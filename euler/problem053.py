'''
============================================================
http://projecteuler.net/problem=53

There are exactly ten ways of selecting three from five, 12345:

123, 124, 125, 134, 135, 145, 234, 235, 245, and 345

In combinatorics, we use the notation, 5C3 = 10.

In general,

nCr =    
n!
r!(nr)!
,where r  n, n! = n(n1)...321, and 0! = 1.
It is not until n = 23, that a value exceeds one-million: 23C10 = 1144066.

How many, not necessarily distinct, values of  nCr, for 1  n  100, are greater than one-million?
============================================================
'''
import math, itertools

'''log(n!)'''
log_fac = lambda n: sum(map(math.log, xrange(2, n + 1)))

'''Number of C^n_r > F.'''
def num_greater(n, F):
    G = log_fac(n) - math.log(F)
    try:
        return n + 1 - 2 * itertools.dropwhile(lambda r: log_fac(r) + log_fac(n - r) >= G, xrange(1, n / 2 + 1)).next()
    except StopIteration:
        return 0
                        
if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
    print sum(num_greater(n, 1000000) for n in xrange(1, 101))
