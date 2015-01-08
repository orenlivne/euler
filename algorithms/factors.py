#!/usr/bin/python
'''
============================================================
Number of factors

Created on Oct 16, 2013
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
import unittest
from numpy.ma.testutils import assert_equal
from nose.tools import raises

#---------------------------------------
# Oren Solution
#---------------------------------------

'''Number of times the prime p appears in the prime factorization of n!. Recursive implementation.
O(log_p(n)) runtime, O(log_p(n)) storage.'''
num_divisors = lambda n, p: 0 if n == 0 else num_divisors(n / p, p) + n / p

def num_divisors_nr(n, p):
    '''Non-recursive counterpart of num_divisors. O(log_p(n)) runtime, O(1) storage.'''
    s = 0
    while n:
        n /= p
        s += n
    return s

#---------------------------------------
# William, Solution 1, October 10
#---------------------------------------
def william1(n,p):
    counts = dict()
    [counts.update([(x, 1 + counts.setdefault(x/p, 0))]) for x in xrange(n) if x % p == 0]
    return sum(counts.values())

#---------------------------------------
# William, Solution 2, October 15
#---------------------------------------

# http://docs.python.org/2/tutorial/datastructures.html#using-lists-as-queues
from collections import deque

def william2(n, p):
    count = 0
    counts = deque()
    pop = 0

    for x in xrange(p, n + 1, p):
        print x, count, counts
        if (x / p) % p == 0:
            i = counts.popleft() + 1
            pop += 1
        else:
            i = 1
        if x <= (n / p): counts.append(i)
        count += i
        print x, count, counts
        print "=-=-=-"
    print "popped %d elements" % pop

    return count

#-----------------------
# Tests        
#-----------------------
class TestRecursion(unittest.TestCase):
    #---------------------------------------------
    # Test Methods
    #---------------------------------------------
    def test_num_divisors(self):
        n, p = 10 ** 12, 11
        assert_equal(num_divisors(n, p), num_divisors_nr(n, p))

    @raises(AssertionError)
    def test_william1(self):
        n, p = 100, 3
        assert_equal(william1(n, p), num_divisors_nr(n, p))

    def test_william2(self):
        n, p = 100, 3
        assert_equal(william2(n, p), num_divisors_nr(n, p))
    
# if __name__ == "__main__":
#     pass
