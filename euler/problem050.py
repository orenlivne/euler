'''
============================================================
http://projecteuler.net/problem=50

The prime 41, can be written as the sum of six consecutive primes:

41 = 2 + 3 + 5 + 7 + 11 + 13
This is the longest sum of consecutive primes that adds to a prime below one-hundred.

The longest sum of consecutive primes below one-thousand that adds to a prime, contains 21 terms, and is equal to 953.

Which prime, below one-million, can be written as the sum of the most consecutive primes?
============================================================
'''
from problem007 import primes

def max_sum(a):
    '''Return a max sum element in a sorted list a.'''
    n, L, max_s, limit = len(a), 0, a[0] - 1, a[-1]
    for i in xrange(n):
        s = sum(a[i:i + L])
        if s > limit or i + L + 1 >= n:
            return max_s
        for j, q in enumerate(a[i + L:], L + 1):
            s += q
            if s > limit:
                break
            if s > max_s and s in a:
                L, max_s = j, s
                #print 'i', i, 'L', L, 'max_s', max_s, sum(a[i:i + L]), a[i:i + L]
    return None  # Should only be reached if n=0

def max_sum_with_set_lookup(a):
    '''Return a max sum element in a sorted list a.'''
    a_set = set(a)
    n, L, max_s, limit = len(a), 0, a[0] - 1, a[-1]
    for i in xrange(n):
        s = sum(a[i:i + L])
        if s > limit or i + L + 1 >= n:
            return max_s
        for j, q in enumerate(a[i + L:], L + 1):
            s += q
            if s > limit:
                break
            if s > max_s and s in a_set:
                L, max_s = j, s
                #print 'i', i, 'L', L, 'max_s', max_s, sum(a[i:i + L]), a[i:i + L]
    return None  # Should only be reached if n=0

if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
    import time

    start = time.time()
    print max_sum(primes('lt', 1000000))
    print time.time() - start, 'sec'

    start = time.time()
    print max_sum_with_set_lookup(primes('lt', 1000000))
    print time.time() - start, 'sec'
