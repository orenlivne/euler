'''
============================================================
http://projecteuler.net/problem=271

For a positive number n, define S(n) as the sum of the integers x, for which 1xn and
x^3=1 mod n.

When n=91, there are 8 possible values for x, namely : 9, 16, 22, 29, 53, 74, 79, 81.
Thus, S(91)=9+16+22+29+53+74+79+81=363.

Find S(13082761331670030).
============================================================
'''
from itertools import product
from problem012 import factorize
from problem435 import crt

def sum_roots_of_unity(n, k):
    '''Sum of all kth-order roots of unit of n using the Chinese Remainder Theorem.''' 
    f = map(int, [p ** l for p, l in factorize(n).iteritems()])
    return sum(crt(zip(r, f)) for r in product(*(filter(lambda x: pow(x, k, p) == 1, xrange(1, p)) for p in f)))

if __name__ == "__main__":
    print sum_roots_of_unity(91, 3) - 1
    print sum_roots_of_unity(13082761331670030, 3) - 1
