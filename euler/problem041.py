'''
============================================================
http://projecteuler.net/problem=41

We shall say that an n-digit number is pandigital if it makes
use of all the digits 1 to n exactly once. For example,
2143 is a 4-digit pandigital and is also prime.

What is the largest n-digit pandigital prime that exists?
============================================================
'''
import itertools
from problem037 import is_prime

def max_pan_prime():
    '''Returns the largest pandigital prime, or 0 if not found (it should exist
    according to the example given in the problem).'''
    for digits in [7, 4]:
        for x in itertools.permutations(range(digits, 0, -1)):
            y = int(''.join(map(str, x)))
            if is_prime(y):
                return y
    return 0

if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
    print max_pan_prime()
