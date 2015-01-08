# encoding: utf-8
# filename: problem433_backtracking.py
'''
============================================================
http://projecteuler.net/problem=433
============================================================
'''
# http://projecteuler.net/thread=433
# By ken, 25 Jun 2013 07:13 pm 

# Even this optimized code is expected to run for 17 days on my machine. Scales like O(N^2).

cdef inline long pair(int N, int n, int d, int s) except? - 2:
    cdef long result
    result = (N // d) * (2 * s + 1)
    for nn in xrange(n + d, N + 1, d): result += pair(N, d, nn, s + 1)
    return result

def branches(N, n, d, s, s_max):
    print N, n, d, s, s_max
    branches = [(n, d)]
    result = (N // d) * (2 * s + 1)
    print 'here'
    if s <= s_max:
        for nn in xrange(n + d, N + 1, d):
            r, b = branches(N, d, nn, s + 1)
            print r, b
            result += r
            branches += b
    return result, branches

def S(N): return pair(N, 1, 1, 0)

if __name__ == "__main__":
    print S(100)
    # import timeit, numpy as np
    # for n in 10 ** np.arange(1, 5):
        # print n, timeit.timeit('print S(' + repr(n) + ')', 'from __main__ import S', number=1)
