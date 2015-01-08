'''
============================================================
http://projecteuler.net/problem=160

For any N, let f(N) be the last five digits before the trailing zeroes in N!.
For example,

9! = 362880 so f(9)=36288
10! = 3628800 so f(10)=36288
20! = 2432902008176640000 so f(20)=17664

Find f(1,000,000,000,000)
============================================================
'''
from itertools import count

def cycle(a):
    '''Return the initial sequence and cycle sequence of the iterable a.'''
    values, ind, b = set(), dict(), list()
    for k, x in enumerate(a):
        if x in values:
            k0 = ind[x]
            return b[:k0], b[k0:]
        values.add(x)
        ind[x] = k
        b.append(x)

MOD = 10 ** 5
TWO_INIT, TWO_PERIOD = map(len, cycle(pow(2, x, MOD) for x in count()))

C = lambda N, p: 0 if N == 0 else C(N / p, p) + N / p
f = lambda N: (pow(2, (C(N, 2) - C(N, 5) - TWO_INIT) % TWO_PERIOD + TWO_INIT, MOD) * F(N)) % MOD
F = lambda N: 1 if N == 0 else (F(N / 2) * Q(N)) % MOD
Q = lambda N: 1 if N == 0 else (Q(N / 5) * R(N)) % MOD
R = lambda N: reduce(lambda x, y: (x * y) % MOD, (n for n in xrange(1, N % MOD + 1) if n % 2 and n % 5), 1) 

def _f(x, d):
    count = 0
    while x % 10 == 0:
        x /= 10
        count += 1
    return x % d, count

fac = lambda n: reduce(lambda x, y:x * y, xrange(1, n + 1))
f_bf = lambda n: _f(fac(N), MOD)

if __name__ == "__main__":
    N = 40
    print f(N), f_bf(N)
    print f(10 ** 12)
