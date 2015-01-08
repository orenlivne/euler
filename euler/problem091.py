'''
============================================================
http://projecteuler.net/problem=91

The points P (x1, y1) and Q (x2, y2) are plotted at integer co-ordinates and are joined to the origin, O(0,0), to form OPQ.

There are exactly fourteen triangles containing a right angle that can be formed when each co-ordinate lies between 0 and 2 inclusive; that is,
0 <= x1, y1, x2, y2 <= 2.

Given that 0 <= x1, y1, x2, y2 <= 50, how many right triangles can be formed?
============================================================
'''
# import itertools as it
#
# is_int = lambda x: x - int(x) < 1e-12
# mdict = lambda a: dict((k, set(v for _, v in pairs)) for k, pairs in it.groupby(sorted(a), lambda pair: pair[0]))
# squares_dict = lambda N: mdict((a * a + b * b, (a, b)) for a, b in it.product(xrange(2 * N + 1), xrange(2 * N + 1)))
# 
# def f(m, n, i, S):
#     '''Returns f(m,n,i). S = squares dictionary.'''
#     mi, count = m * m + i * i, 0
#     #print 'f[%d,%d,%d]' % (m, n, i)
#     if n == 0: return 0
#     if S.has_key(mi):
#         for a, _ in S[mi]:
#             x = 0.5 * (m - (mi - a * a) ** 0.5)
#             if is_int(x):
#                 x = int(x)
#                 if x >= 0 and x < m:
#                     y = 0.5 * (i + (i * i + 4 * (m - x) * x) ** 0.5)
#                     if is_int(y):
#                         y = int(y)
#                         if y >= 0 and y <= n:
#                             count += 1
#     print 'f[%d,%d,%d] = %d' % (m, n, i, count)
#     return count
# 
# g = lambda k, S: sum(f(k, k - 1, i, S) for i in xrange(k)) + sum(f(k, k, i, S) for i in xrange(k + 1))
# 
# def num_triangles(N):
#     S, G = squares_dict(N), 0
#     for n in xrange(1, N + 1):
#         gn = g(n, S)
#         G += gn
#         print 'n', n, 'g[n]', gn, 'S[n]', n * n + G
#         yield n * n + G
# 
# if __name__ == "__main__":
#     N = 2
#     print [(a * a + b * b, (a, b)) for a, b in it.product(xrange(2 * N + 1), xrange(2 * N + 1))]
#     S = squares_dict(N)
#     print f(2, 2, 2, S)
#     print list(num_triangles(2))  # [-1]

from euler.problem005 import gcd

num_triangles = lambda n: 3 * n * n + 2 * sum(min(y * f / x, (n - x) * f / y) for x, y, f in ((x, y, gcd(x, y)) for x in xrange(1, n + 1) for y in xrange(1, n + 1)))
                                        
if __name__ == "__main__":
    print num_triangles(50)
