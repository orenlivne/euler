'''
============================================================
http://projecteuler.net/problem=40

An irrational decimal fraction is created by concatenating the positive integers:

0.123456789101112131415161718192021...

It can be seen that the 12th digit of the fractional part is 1.

If dn represents the nth digit of the fractional part, find the value of the following expression.

d1  d10  d100  d1000  d10000  d100000  d1000000
============================================================
'''
from operator import mul

max_digits = 8
p10 = [10 ** n for n in xrange(max_digits + 1)] # Or speed up using an x *= 10 loop
S = [0, 1] + [1 + n * p10[n - 1] - (p10[n] - 1) / 9 for n in xrange(2, max_digits + 1)]

def num_digits(i):
    '''Return the digit group that i belongs to (we group original integers with the same # digits).'''
    n = 1
    while S[n] <= i:
        n += 1
    return n - 1

def d(i):
    '''Return the ith digit in the fraction.'''
    #print 'd(%d)' % (i,)
    if i >= S[-1]:
        return ValueError('i too large, increase max_digits')
    n = num_digits(i)
    return _d(i - S[n], n)

def _d(j, n):
    '''A helper function: for a series n, relative index j, return d^n_j.'''
    #print '_d(%d,%d)' % (j, n)
    if n == 1:
        #print '\tn=1, %d' % (j + 1,)
        return j + 1
    k = j % n
    #print '\tk = j %% n %d' % (k,)
    if k == n - 1:
        #print '\tLast digit, %d' % (((j - n + 1) / n) % 10)
        return ((j - n + 1) / n) % 10
    else:
        #m = 10 * n
        #print '\tm %d j/m %d k %d' % (m, j / m, k)
        return _d((n - 1) * (j / (10 * n)) + k, n - 1)

if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
    #import numpy as np
    #np.set_printoptions(threshold=np.nan)
    #print S
    #print d(12)
    #print np.array([num_digits(n) for n in xrange(3000)])
    #print np.array([d(n) for n in xrange(1, 3000)])
    print reduce(mul, (d(10 ** n) for n in xrange(7)))
