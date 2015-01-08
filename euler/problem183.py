'''
============================================================
http://projecteuler.net/problem=183

Let N be a positive integer and let N be split into k equal parts, r = N/k, so that N = r + r + ... + r.
Let P be the product of these parts, P = r x r x ... x r = rk.

For example, if 11 is split into five equal parts, 11 = 2.2 + 2.2 + 2.2 + 2.2 + 2.2, then
P = 2.25 = 51.53632.

Let M(N) = Pmax for a given value of N.

It turns out that the maximum for N = 11 is found by splitting eleven into four equal parts which
leads to Pmax = (11/4)**4; that is, M(11) = 14641/256 = 57.19140625, which is a terminating decimal.

However, for N = 8 the maximum is achieved by splitting it into three equal parts, so M(8) = 512/27,
which is a non-terminating decimal.

Let D(N) = N if M(N) is a non-terminating decimal and D(N) = -N if M(N) is a terminating decimal.

For example, SUM D(N) for 5 <= N <= 100 is 2438.

Find SUM D(N) for 5 <= N <= 10000.
============================================================
'''
from problem005 import gcd
from math import e, log

f = lambda N, k: k * (log(N) - log(k))

def is_term(q):
    '''Is q the denominator of a terminating decimal.'''
    while q % 2 == 0: q = q // 2
    while q % 5 == 0: q = q // 5
    return q == 1

def D(N):
    k = int(N / e)
    k1 = k + 1
    k = k if f(N, k) > f(N, k + 1) else k1
    return (-N) if is_term(k / gcd(N, k)) else N

S = lambda N: sum(D(n) for n in xrange(5, N + 1))

if __name__ == "__main__":
    print D(11), D(8)
    print S(100), S(10000)
