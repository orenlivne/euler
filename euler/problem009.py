'''
============================================================
http://projecteuler.net/problem=9

A Pythagorean triplet is a set of three natural numbers, a  b  c, for which,

a2 + b2 = c2
For example, 32 + 42 = 9 + 16 = 25 = 52.

There exists exactly one Pythagorean triplet for which a + b + c = 1000.
Find the product abc.

Created on Feb 21, 2013
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
def pythagorean1000():
    '''Return the product of the Pythagorean triplet whose sum is 1000.

    Can be generalized using Sivoh's solution, 27 Apr 2006 09:15 am (generalizes my method from d=1000 to any d)
    This algebraic solution is nowhere near as elegant as Pier's, but also requires no great intuition (brute force algebra?).
    
    let d = 1000
    substitute c = d - a - b into a^2+b^2 = c^2 to get:
    a^2+b^2=d^2 - 2ad + 2b(a - d) + a^2 + b^2
    or
    d^2 - 2ad +2b(a-d) = 0
    
    solve for b:
    b= (d^2 - 2ad) / 2(d-a) = d + d^2 / (2(a - d))
    
    a >= d/2 implies b <= d + d^2/2(d/2-d) = 0, so a < d/2
    
    since b is integral, u = (a-d) must be a factor of d^2/2 and 
    0 < a < d/2 => -d < u < -d/2
    
    so we're left to find factors of d^2/2 in the range (-d,-d/2) exclusive
    
    since the prime factorization of d^2/2=500000=5*10^5=5*(2*5)^5 is 2^5*5^6 and all factors
    must be composed of a subset of this factorization, we only have to look at numbers composed of
    5 or less 2's and 6 or less 5's which is only 42 numbers. 
    Of these, only -5^4=-625 and -2^5*5^2=-800 fall between -1000 and -500.
    
    u=600 => a =  375 => b = 200 => c = 425
    it should come as no surprise since a and b are symmetric that:
    u=800 => a = 200 => b = 375 => c = 425

    >>> pythagorean1000()
    31875000'''
    a, b, c = 200, 375, 425 
    return a * b * c

if __name__ == "__main__":
    import doctest
    doctest.testmod()
