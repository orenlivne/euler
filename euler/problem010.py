'''
============================================================
http://projecteuler.net/problem=10

The sum of the primes below 10 is 2 + 3 + 5 + 7 = 17.

Find the sum of all the primes below two million.

Created on Feb 21, 2013
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
import problem007, time
from numpy.ma.testutils import assert_equal

if __name__ == "__main__":
    start = time.time()
    s = sum(problem007.primes('lt', 2e6))
    print s, time.time() - start, 'sec'
    assert_equal(s, 142913828922)
#    import doctest
#    doctest.testmod()
