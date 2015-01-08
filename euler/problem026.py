'''
============================================================
http://projecteuler.net/problem=26

A unit fraction contains 1 in the numerator. The decimal representation of the unit fractions with denominators 2 to 10 are given:

1/2    =     0.5
1/3    =     0.(3)
1/4    =     0.25
1/5    =     0.2
1/6    =     0.1(6)
1/7    =     0.(142857)
1/8    =     0.125
1/9    =     0.(1)
1/10    =     0.1
Where 0.1(6) means 0.166666..., and has a 1-digit recurring cycle. It can be seen that 1/7 has a 6-digit recurring cycle.

Find the value of d  1000 for which 1/d contains the longest recurring cycle in its decimal fraction part.

Created on Feb 21, 2013
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
def repeating_cycle(d):
    '''Returns the cycle size of 1/d. d >= 0. Returns 0 if d = 0.'''
    if d == 0:
        return 0
    # Remove multiples of 2,5, which don't change the cycle size
    while d % 2 == 0: 
        d /= 2
    while d % 5 == 0:
        d /= 5
    # Non-repeating=terminating decimal
    if d == 1:
        return 0
    # Calculate ord(1) mod d
    # http://en.wikipedia.org/wiki/Repeating_decimal
    n, x = 1, 10 % d        # x keeps track of 10**n mod d
    while x != 1:
        while x < d:
            x *= 10
            n += 1
        x = x % d
    return n

def mymax(it):
    '''Return max of it and argmax. it must be non-empty.'''
    i, i_max, x_max = 0, 0, it.next()
    try:
        while True:
            x = it.next()
            i += 1
            if x > x_max:
                i_max = i
                x_max = x
    except StopIteration:
        pass
    return x_max, i_max

if __name__ == "__main__":
    print mymax(iter(map(repeating_cycle, xrange(1000))))
#    import doctest
#    doctest.testmod()
