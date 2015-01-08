'''
============================================================
http://projecteuler.net/problem=125

The palindromic number 595 is interesting because it can be written as the sum of consecutive squares: 62 + 72 + 82 + 92 + 102 + 112 + 122.

There are exactly eleven palindromes below one-thousand that can be written as consecutive square sums, and the sum of these palindromes is 4164. Note that 1 = 02 + 12 has not been included as this problem is concerned with the squares of positive integers.

Find the sum of all the numbers less than 108 that are both palindromic and can be written as the sum of consecutive squares.
============================================================
'''
import itertools as it
from euler.problem086 import is_int

def is_cube(t):
    T, n, e = 6 * t, (3 * t) ** (1. / 3), 1
    # print 'is_cube(t=%d)' % (t,)
    while e > 0.1:
        n_old = n
        m = n * (n + 1)
        n -= (m * (2 * n + 1) - T) / (6 * m + 1)
        e = abs(n - n_old)
    # print n
    n = round(n)
    return T == n * (n + 1) * (2 * n + 1)
        
def special_nums(digits):
    N = 10 ** digits
    T = [(n * (n + 1) * (2 * n + 1)) / 6 for n in xrange(int((0.5 * N) ** 0.5) + 1)]
    T_max = T[-1]
    for d in xrange(1, digits + 1):
        for x in it.product(xrange(2 if d == 1 else 1, 10), *(xrange(10) for _ in xrange((d + 1) / 2 - 1))):
            xs = map(str, x)
            n = int(''.join(xs + list(reversed(xs))[d % 2:]))
            if not is_int(n ** 0.5) and any(is_cube(t) for t in it.takewhile(lambda x: x <= T_max, (n + t for t in T))):
                print n
                yield n

def special_nums_bf(digits):
    N = 10 ** digits
    l, r = [i ** 2 for i in xrange(1, int(N ** 0.5) + 1)], set([])
    L = len(l)
    for i in xrange(L) :
        s = 0
        for j in xrange(i, L):
            if s > N: break
            s += l[j]
            ss = str(s)
            if ss == ss[::-1] and j > i and s not in r: r.add(s)
    return sum(r)

if __name__ == "__main__":
    print special_nums_bf(8)
#     a = list(special_nums(3))
#     print len(a), sum(a), a
#    print sum(special_nums(8))
