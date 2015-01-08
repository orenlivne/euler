'''
============================================================
http://projecteuler.net/problem=148

We can easily verify that none of the entries in the first seven rows of Pascal's triangle are divisible by 7:

                               1
                          1          1
                     1          2          1
                1          3          3          1
           1          4          6          4          1
      1          5         10         10          5          1
1          6         15         20         15          6          1
However, if we check the first one hundred rows, we will find that only 2361 of the 5050 entries are not divisible by 7.

Find the number of entries which are not divisible by 7 in the first one billion (109) rows of Pascal's triangle.
============================================================
'''
from itertools import count
import numpy as np
from problem036 import base_digits
from problem101 import polyval

def binom():
    b = [1L]
    yield list(b)
    for n in count(1):
        a = list(b)
        for i in xrange(n - 1): b[i] = a[i] + a[i + 1]
        b.insert(0, 1L)
        yield list(b)

def num_bf(N):
    b, s = [1L], 1
    for n in xrange(1, N):
        a = list(b)
        for i in xrange(n - 1): b[i] = a[i] + a[i + 1]
        b.insert(0, 1L)
        # A.append(sum(1 for x in b if x % 7 != 0))
        s += sum(1 for x in b if x % 7 != 0)
    return s

def A(N):
    b, A = [1L], [1]
    for n in xrange(1, N):
        a = list(b)
        for i in xrange(n - 1): b[i] = a[i] + a[i + 1]
        b.insert(0, 1L)
        A.append(sum(1 for x in b if x % 7 != 0))
    return A

triangle = lambda n: n * (n + 1) / 2

def num_nondiv_binom(N, b):
    '''Number of binomial coefficients in rows 0-(N-1) not divisible by b. b must be prime.''' 
    a = np.array(base_digits(N, b), dtype=np.long)
    return polyval(np.array(map(triangle, a)) * np.flipud(np.cumprod(np.concatenate(([1], np.flipud(a[1:] + 1))))), triangle(b))

if __name__ == "__main__":
    for n in [100, 220, 343, 344, 345]:  # , 2000, 5000, 10000]:
        print num_bf(n), num_nondiv_binom(n, 7)
    print num_nondiv_binom(10 ** 9, 7)
