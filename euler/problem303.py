'''
============================================================
http://projecteuler.net/problem=303

For a positive integer n, define f(n) as the least positive multiple of n that, written in base 10, uses only digits 2.

Thus f(2)=2, f(3)=12, f(7)=21, f(42)=210, f(89)=1121222.

Also, sum(f(n)/n), n=1 to 100 = 11363107.

Find sum(f(n)/n), n=1 to 10000.
============================================================
'''
# import itertools as it, numpy as np
# from problem233 import prime_factors
# from problem007 import primes
# from euler.problem036 import base_digits
# 
# G = lambda n, a: not all(x <= '2' for x in str(a * n))
# 
# def F_bf(n, max_a=100):
#     try:
#         return it.dropwhile(lambda a: not all(x <= '2' for x in str(a * n)), xrange(1, max_a + 1)).next()
#     except StopIteration:
#         return -1
#     
# def test_brute_force(N):
#     '''Brute force: for each n, multiply by all a's until we find a good a*n.'''
#     left = xrange(1, N + 1)
#     max_a = 50
#     for _ in xrange(2): 
#         left = [n for n in left if F_bf(n, max_a) < 0]
#         print max_a, len(left), left
#         max_a *= 2
# 
# def test_back_tracking(N):
#     '''Loop over permissible ranges of F, backtracking to n's for which f(n)=F.'''
#     f = np.zeros((N + 1), dtype=int)
#     f[0] = -1
#     q = [(1, 2)]
#     i = 0
#     current = 0
#     done = False
#     P = primes('lt', N + 1)
#     print P
#     M = 10 ** 7
#     while not done:
#         while current < len(q):
#             if q[current][0] >= M:
#                 done = True
#                 break
#             r = q[current]
#             print r
#             if r[1] <= N:
#                 for n in xrange(r[0], r[1] + 1): f[n] = 1
#             for F in xrange(r[0], r[1] + 1):
#                 print '  ', F, ''.join(str(x) for x in reversed(base_digits(F, 2)))
# #                factors = list(prime_factors(F, P))
# #                print 'F', F, 'factors', factors
# #                # print '  ', 'candidates', [np.prod(x) for k in xrange(1, len(factors) + 1) for x in it.combinations(factors, k)]
# #                for n in (np.prod(x) for k in xrange(1, len(factors) + 1) for x in it.combinations(factors, k)):
# #                    # print '  ', 'n', n, (repr(f[n]) if (n <= N) else '-')
# #                    if n <= N and f[n] == 0:
# #                        f[n] = F / n
# #                        print '    ', 'Setting', n, f[n]
#             current += 1
#         if done: break
#         for x in xrange(q[i][0], q[i][1] + 1): q.append((10 * x, 10 * x + 2))
#         i += 1
#     print len(np.where(f == 0)[0]), np.where(f == 0)[0]

import itertools as it

'''Brute-force done the better way: for every n, loop over all possible 012-numbers in order, and stop
when we find one that's divisible by n. The only exception is for numbers n composed of 9''s, for which
brute-force is slow but we guessed the pattern of F(n) from 9,99,999.''' 
sf = lambda N: sum((long('1' * len(str(n)) + '2' * (4 * len(str(n)))) if all(x == '9' for x in str(n)) else it.dropwhile(lambda f: f % n, it.imap(lambda s: long(''.join(s)), it.chain.from_iterable(it.product('12', *('012' for _ in xrange(d - 1)))  for d in it.count(len(str(n)))))).next()) / n for n in xrange(1, N + 1))

if __name__ == "__main__":
    print sf(100)  # 11363107
    print sf(10000)  # 1111981904675169
    
    # N = 100
    # test_brute_force(N)
    # test_back_tracking(N)
