'''
============================================================
http://projecteuler.net/problem=3

The prime factors of 13195 are 5, 7, 13 and 29.

What is the largest prime factor of the number 600851475143 ?

Created on Feb 19, 2013
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
from math import floor, sqrt

def largest_prime_factor(n):
    '''Return the largest prime factor of an integer n >= 2. If n is prime, returns 1.

    >>> largest_prime_factor(600851475143)
    6857'''
    # Divide-and-conquer approach: largest prime factor of n = maximum of largest prime factor of
    # a, largest prime factor b where n = a*b
    a, b = pair(n)
    if a == n:
        # n is prime
        return n
    p = largest_prime_factor(a)
    # If a >= b and has a largest factor larger than b, no need to search in the b-branch of the
    # divide-and-conquer tree.
    return max(p, largest_prime_factor(b)) if p < b else p
    
def pair(n):
    '''Find a pair of numbers such that n = a * b, a>=b and a and b are as close to each other
    as possible. This makes the divide-and-conquer more efficient.'''
    a = int(floor(sqrt(n)))
    while a >= 1:
        if n % a == 0:
            b = n / a
            return max(a, b), min(a, b)
        a -= 1
    raise ValueError('We shouldn''t be here; must have found a divisor >= 1, for any integer number') 

if __name__ == "__main__":
    import doctest
    doctest.testmod()
