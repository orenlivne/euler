'''
============================================================
http://projecteuler.net/problem=24

A permutation is an ordered arrangement of objects. For example, 3124 is one possible permutation of the digits 1, 2, 3 and 4. If all of the permutations are listed numerically or alphabetically, we call it lexicographic order. The lexicographic permutations of 0, 1 and 2 are:

012   021   102   120   201   210

What is the millionth lexicographic permutation of the digits 0, 1, 2, 3, 4, 5, 6, 7, 8 and 9?

Created on Feb 21, 2013
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
import time

def lexperm(d, n):
    '''Return the textual representation of the nth permutation of the digits 0..d-1, 0 <= n < d!.'''
    p = reduce(lambda x, y: x * y, range(1, d + 1)) # d!
    digits, remaining = [-1] * d, range(d)
    for i in xrange(d): # Recover perm digits left-to-right
        p /= (d - i) # So p=(d-1)! for i=0. p is the variable "base"
        di = remaining[n / p]
        digits[i] = di
        remaining.remove(di)
        n = n % p
    return ''.join(map(lambda x: str(x) if x < 10 else chr(ord('A') + x - 10), digits))
        
if __name__ == "__main__":
    start = time.time()
    print lexperm(10, 1000000 - 1) # Convert to 0-based n
    print '%.16f secs' % (time.time() - start,)
    # We support n > 10!
    print lexperm(12, 1000000 - 1) # Convert to 0-based n
