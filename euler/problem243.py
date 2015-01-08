'''
============================================================
http://projecteuler.net/problem=243

http://projecteuler.net/problem=243
============================================================
'''
from problem007 import primes
from numpy import prod

if __name__ == "__main__":
    # Calculated that 2*3*...*23 is not large enough and 29*this number is. So trying
    # multiples of this number until becomes large enough.
    print 4 * prod(primes('lt', 29))
