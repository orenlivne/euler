'''
============================================================
http://projecteuler.net/problem=1

If we list all the natural numbers below 10 that are
multiples of 3 or 5, we get 3, 5, 6 and 9. The sum of these 
multiples is 23.

Find the sum of all the multiples of 3 or 5 below 1000.

Created on Feb 19, 2013
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
def sum_multiples35(n, divisors):
    '''Return sum of the sums of multiples of 3 or 5.
    Works for any non-negative integer n.

    >>> sum_multiples(1000, [3,5])
    233168'''
    # Wrong
    # return sum(len(xrange(p, n, p)) for p in divisors)
    
    # Wrong
    # return sum(sum(xrange(p, n, p)) for p in divisors)

    # OK, but not general and slow
    sum_multiples_of_p = lambda p: sum(xrange(p, n, p))
    return sum_multiples_of_p(3) + sum_multiples_of_p(5) - sum_multiples_of_p(15) 
    
    # Faster, but O(2^p) for p divisors
    def sum_multiples_of_p(p):
        m = (n - 1) / p
        lambda p: p * m * (m + 1) / 2
    return sum_multiples_of_p(3) + sum_multiples_of_p(5) - sum_multiples_of_p(15) 

def sum_multiples(n, divisors):
    '''Return sum of the sums of multiples of p1 or p2 or ... pk (for p in divisors).
    Works for any non-negative integer n and an iterable of divisors divisors.

    >>> sum_multiples(1000, [3,5])
    233168'''
    raise ValueError('To be written')

if __name__ == "__main__":
    import doctest
    doctest.testmod()
