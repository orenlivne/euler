'''
============================================================
http://projecteuler.net/problem=4

A palindromic number reads the same both ways. The largest palindrome made from the product of two 2-digit numbers is 9009 = 91 99.

Find the largest palindrome made from the product of two 3-digit numbers.

Created on Feb 20, 2013
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
# Strategy: assuming first that the largest palindrome has 6-digit. If not, we'll have to write
# the corresponding code for 5 digits.
#
# P.S. the largest MUST have 6-digits since there exists a 6-digits palindrome: 111111 = 143 x 777.

def cf_opts():
    '''Return a multi-valued dictionary of possible c,f values for each z.
    Note: d[0] is computed but not subsequently used, because z >= 1.'''
    D = {}
    for c in xrange(1, 10):
        for f in xrange(1, 10):
            D.setdefault((c * f) % 10, []).append((c, f))
    return D

def maxpal6z(z, ad_opts, cf_opts):
    # Could be made faster by somehow sorting n's?
    n_max = 100000  # Ensures n has 6 digits
    k = 0
    for a, d in ad_opts:
        for c, f in cf_opts:
            # Could reduce cost of b, e loops by using the fact that either abc or def must be
            # divisible by 11, since the palindrome is (zyxxyz = 11*(9091*z+910*y+x))
            for b in xrange(10):
                for e in xrange(10):
                    n = (10 * (10 * a + b) + c) * (10 * (10 * d + e) + f)
                    if n > n_max and is_palindrome6(n):
                        n_max = n
                    k += 1
    print k
    return n_max if n_max > 100000 else None  # None means not found

def is_palindrome6(n):
    if n % 10 != n / 100000:
        return False
    n = (n / 10) % 10000

    if n % 10 != n / 1000:
        return False
    n = (n / 10) % 100
    
    return n % 10 == n / 10

def ad_opts():
    '''Return a multi-valued dictionary of possible a,d values for each z.'''
    D = {}
    for a in xrange(1, 10):
        for d in xrange(1, 10):
            low = max(1, (a * d) / 10)  # z must be >= 1
            high = ((a + 1) * (d + 1) - 1) / 10
            for z in xrange(low, high + 1): D.setdefault(z, []).append((a, d))
    return D

def maxpal6():
    '''Return the largest 6-digit palindrome made from the product of two 3-digit numbers.

    >>> maxpal6()
    906609'''
    ad = ad_opts()
    cf = cf_opts()
    for z in xrange(9, 0, -1):
        n = maxpal6z(z, ad[z], cf[z])
        if n:
            return n
    return None

if __name__ == "__main__":
    import doctest
    doctest.testmod()
