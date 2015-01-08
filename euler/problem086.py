'''
============================================================
http://projecteuler.net/problem=86

A spider, S, sits in one corner of a cuboid room, measuring 6 by 5 by 3, and a fly, F, sits in the opposite corner. By travelling on the surfaces of the room the shortest "straight line" distance from S to F is 10 and the path is shown on the diagram.

However, there are up to three "shortest" path candidates for any given cuboid and the shortest route doesn't always have integer length.

By considering all cuboid rooms with integer dimensions, up to a maximum size of M by M by M, there are exactly 2060 cuboids for which the shortest route has integer length when M=100, and this is the least value of M for which the number of solutions first exceeds two thousand; the number of solutions is 1975 when M=99.

Find the least value of M such that the number of solutions first exceeds one million.
============================================================
'''
# import numpy as np, itertools as it
# from euler.problem005 import gcd
from itertools import count
from math import ceil, sqrt

is_int = lambda x: x - int(x) < 1e-12

def min_m_above(N):
    '''Returns the minimum M for which the number of integral solutions > N. The number of solution
    equals the number of integral Pythagorean triplets (a,b+c,L=sqrt(a^2+(b+c)^2) with 1 <= a <= M
    and s=b+c, 1 <= b <= c <= a.'''
    n = 0
    for a in count(1):  # Parameterization: M = a >= b >= c >= 1. #solutions depends on a,s=b+c only.
        a2 = a * a
        n += sum(min(s - 1, a) + 1 - int(ceil(0.5 * s)) for s in xrange(2, 2 * a + 1) if is_int(sqrt(a2 + s * s)))  # Add #solutions for each s=b+c
        if n > N: return a
if __name__ == "__main__":
    # print min_m_above(2000)
    import time
    start = time.time()
    print min_m_above(1000000)
    print time.time() - start, 'sec'

#------------------------------------------------------------------------------------------
# Try #1: O(M^2) but buggy 
# def num_solutions(M_max):
#     '''Returns the number of integral solutions for M=0..M_max-1. O(M_max)^3 complexity, brute force.'''
#     N = np.zeros((M_max,), dtype=np.uint)
#     for a in xrange(1, M_max):
#         a2 = a * a
#         for b in xrange(1, a + 1):
#             for c in xrange(1, b + 1):
#                 if is_int((a2 + (b + c) * (b + c)) ** 0.5): N[a] += 1
#     return np.cumsum(N)
#
# Try $2: O(M^3) correct but slow
# def num_solutions2(M_max):
#     '''Returns the number of integral solutions for M=0..M_max-1. O(M_max)^2 complexity, but broken.'''
#     N = np.zeros((M_max), dtype=np.uint)
#     print 'M_max', M_max
#     for m in xrange(1, M_max):
#         for n in (n for n in xrange(1 + m % 2, m, 2) if gcd(m, n) == 1):
#             A1, B1 = m * m - n * n, 2 * m * n
#             A1, B1 = min(A1, B1), max(A1, B1)
#             for d in xrange(1, int(float(M_max) / B1)):
#                 A, B = A1 * d, B1 * d
#                 # N[max(A, B - 1)] += (B - 1)
#                 # N[B] += (A - 1)
#                 print 'm', m, 'n', n, 'd', d, (A, B)
#                 # print '\tN[%d] += %d (total: %d)' % (max(A, B - 1), B - 1, N[max(A, B - 1)])
#                 a = A
#                 for b in xrange(int(ceil(0.5 * B)), B):
#                     c = B - b
#                     M = max(a, b, c)
#                     N[M] += 1
#                     print '\t(%d,%d,%d) L=%7.2f N[%d]++ (total: %d)' % (a, b, c, (a * a + (b + c) * (b + c)) ** 0.5, M, N[M])
#                 a = B
#                 N[B] += (A - int(ceil(0.5 * A)))
#                 for b in xrange(int(ceil(0.5 * A)), A):
#                     c = A - b
#                     print '\t(%d,%d,%d) L=%7.2f' % (a, b, c, (a * a + (b + c) * (b + c)) ** 0.5)                    
#                 print '\t\tN[%d] += %d (total: %d)' % (B, A - 1, N[B])
#     print 'N', np.array(N)
#     print 'cum N', np.cumsum(N)
#     return np.cumsum(N)
# 
# def first_num_not_satisfying(terms, criterion, n_min, fac=2):
#     n = n_min
#     while True:
#         try:
#             print 'n', n
#             return it.dropwhile(criterion, enumerate(terms(n))).next()[0]
#         except StopIteration: n *= fac
# 
# min_m_above = lambda N: first_num_not_satisfying(num_solutions, lambda (_, n): n <= N, int(N ** 0.5)) 
