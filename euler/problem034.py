'''
============================================================
http://projecteuler.net/problem=34

145 is a curious number, as 1! + 4! + 5! = 1 + 24 + 120 = 145.

Find the sum of all numbers which are equal to the sum of the factorial of their digits.

Note: as 1! = 1 and 2! = 2 are not sums they are not included.
============================================================
'''
import math

F = dict((x, math.factorial(x)) for x in xrange(10))

def is_fac(x, b=10):
    '''Is x the sum of factorials of digits of x >= 1 in base b.'''
    s, y = 0, x
    while x > 0:
        s += F[x % b]
        x /= b
    return y == s
         
if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
    import time
    
    start = time.time()
    print sum(filter(is_fac, xrange(10, 7 * F[9])))
    print time.time() - start, 'sec'
