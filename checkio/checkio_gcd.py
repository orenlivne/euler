'''
============================================================
http://www.checkio.org/mission/gcd/
https://factorable.net/weakkeys12.extended.pdf

Created on Mar 29, 2015
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
def gcd(m, n):
    '''Returns the greatest common divisor of m and n. Eulid''s algorithm.'''
    while n: m, n = n, m % n
    return m

def greatest_common_divisor(*args):
    '''Returns the greatest common divisor of *args.'''
    return reduce(gcd, args)

if __name__ == '__main__':
    # These "asserts" using only for self-checking and not necessary for auto-testing
    assert greatest_common_divisor(6, 4) == 2, "Simple"
    assert greatest_common_divisor(2, 4, 8) == 2, "Three arguments"
    assert greatest_common_divisor(2, 3, 5, 7, 11) == 1, "Prime numbers"
    assert greatest_common_divisor(3, 9, 3, 9) == 3, "Repeating arguments"
