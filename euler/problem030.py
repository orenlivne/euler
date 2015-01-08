'''
============================================================
http://projecteuler.net/problem=30

Surprisingly there are only three numbers that can be written as the sum of fourth powers of their digits:

1634 = 14 + 64 + 34 + 44
8208 = 84 + 24 + 04 + 84
9474 = 94 + 44 + 74 + 44
As 1 = 14 is not a sum it is not included.

The sum of these numbers is 1634 + 8208 + 9474 = 19316.

Find the sum of all the numbers that can be written as the sum of fifth powers of their digits.
============================================================
'''
import itertools, time

def digit_sum(x, k, b=10):
    '''Sum of kth powers of digits of x >= 1 in base b.'''
    s = 0
    while x > 0:
        s += (x % b) ** k
        x /= b
    return s

eq_pow_sum = lambda k: sum(x for x in xrange(10, 9 ** k * list(itertools.takewhile(lambda n: 10 ** (n - 1) <= 9 ** k * n, xrange(1, 10 * k)))[-1]) if x == digit_sum(x, k))

#is_eq_pow = lambda x, k : x == sum(map(lambda a: a ** k, digits(x)))
# Suggested by other people, but slower than the above line
#is_eq_pow = lambda x, k : x == sum(int(s) ** k for s in str(x))
    
if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
    start = time.time()
    print eq_pow_sum(4)
    print time.time() - start, 'sec'

    start = time.time()
    print eq_pow_sum(5)
    print time.time() - start, 'sec'
