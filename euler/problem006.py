'''
============================================================
http://projecteuler.net/problem=6

The sum of the squares of the first ten natural numbers is,

12 + 22 + ... + 102 = 385
The square of the sum of the first ten natural numbers is,

(1 + 2 + ... + 10)2 = 552 = 3025
Hence the difference between the sum of the squares of the first ten natural numbers and the square of the sum is 3025  385 = 2640.

Find the difference between the sum of the squares of the first one hundred natural numbers and the square of the sum.

Created on Feb 21, 2013
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
def sum_sq_diff(n):
    '''Return etween the sum of the squares of the first n natural numbers and the square of the sum.

    >>> sum_sq_diff(10)
    2640

    >>> sum_sq_diff(100)
    25164150'''
    return n * (n - 1) * (n + 1) * (3 * n + 2) / 12

if __name__ == "__main__":
    import doctest
    doctest.testmod()
