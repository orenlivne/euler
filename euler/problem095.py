'''
============================================================
http://projecteuler.net/problem=95

The proper divisors of a number are all the divisors excluding the number itself. For example, the proper divisors of 28 are 1, 2, 4, 7, and 14. As the sum of these divisors is equal to 28, we call it a perfect number.

Interestingly the sum of the proper divisors of 220 is 284 and the sum of the proper divisors of 284 is 220, forming a chain of two numbers. For this reason, 220 and 284 are called an amicable pair.

Perhaps less well known are longer chains. For example, starting with 12496, we form a chain of five numbers:

12496  14288  15472  14536  14264 ( 12496  ...)

Since this chain returns to its starting point, it is called an amicable chain.

Find the smallest member of the longest amicable chain with no element exceeding one million.
============================================================
'''
import numpy as np
from problem021 import DCalculator
from collections import OrderedDict

def longest_amicable_chain_min_member(n):  # ), queue_size=600):
    '''Return the smallest member of the longest amicable chain with no element exceeding n-1. Assumed
    to be unique, with chain length <= queue_size.'''
    d, x, c = DCalculator(n).divisor_sum(), 1, np.zeros((n + 1,), dtype=np.int)
    c.fill(-1)  # Initially, set all nodes to unvisited. 0=visited. >0: cycle length at smallest element of the cycle
    while x < n:  # x points to next unvisited element
        #print 'x', x
        y, p = x, 0
        q = OrderedDict([(y, p)])
        #print '\t', y, p
        while y < n:
            # Advance along cycle
            y, p = d[y], p + 1
            appeared_before = q.has_key(y)
            #print '\t', y, p
            if y > n or c[y] > 0 or appeared_before: break
            q[y] = p
        #print '\tlast', y, p, q
        r = q.keys()
        c[r] = 0
        if appeared_before:
            i = q[y]
            z = r[i + np.argmin(r[i:])]
            c[z] = p - i 
            print x, '\t', 'c[%d] = %d, i=%d' % (z, c[z], i)
        while c[x] >= 0 and x < n: x += 1  # Advance to next unvisited element
#     np.set_printoptions(threshold=np.nan)
#     print c
    return np.argmax(c) 
    
if __name__ == "__main__":
#    print longest_amicable_chain_min_member(16000)
    print longest_amicable_chain_min_member(10 ** 6 + 1)
