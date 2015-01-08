'''
============================================================
http://projecteuler.net/problem=233

Let f(N) be the number of points with integer coordinates that are on a circle passing through (0,0), (N,0),(0,N), and (N,N).
It can be shown that f(10000) = 36.
What is the sum of all positive integers N <= 1011 such that f(N) = 420?

https://raw.github.com/eterevsky/euler/master/233.py
============================================================
'''
from __future__ import division
import math
from problem012 import factorize
from euler.problem049 import primes_in_range

def divisors(n):
    f = factorize(n).items()
    d = 1
    p = [0] * len(f)
    while True:
        yield d
        i = 0
        while i < len(f) and p[i] == f[i][1]:
            p[i] = 0
            d //= f[i][0] ** f[i][1]
            i += 1
            if i >= len(f): break
            p[i] += 1
        d *= f[i][0]
      
min_divisors_sum_save = {}

def min_divisors_sum(n):
    """min(d1 + d2 + ... + dk - k | d1 * d2 * ... * dk == n)"""
    if n not in min_divisors_sum_save:
        s = 0
        for p, k in factorize(n).iteritems():
            s += (p - 1) * k
        min_divisors_sum_save[n] = s
    return min_divisors_sum_save[n]


def gen_4p1_dnum(dnum, minp, hi):
    """Generate numbers with 4k+1 prime divisors and given sum of divisors.

    Generate all such n that:
    1. n < hi.
    2. All prime divisors of n are of the form 4*k + 1.
    3. All prime divisors of n are >= minp.
    4. d(n) = dnum.
    """
    if hi <= 1:
        return
    elif dnum == 1:
        yield 1
        return

    print list(divisors(dnum))
    for d in divisors(dnum):
        # p^a * (p + 4)^min_d(dnum/d) < hi
        if d > 1:
            a = d - 1
            maxp = int(hi ** (1 / (a + min_divisors_sum(dnum / d))))
            for p in primes_in_range(minp, maxp + 1):
                if p % 4 == 1:
                    for x in gen_4p1_dnum(dnum // d, p + 4, (hi - 1) // p ** a + 1):
                        yield p ** a * x

# def test_gen_4p1_dnum():
#     for dnum in range(2, 16):
#         dset = set()
#         for n in gen_4p1_dnum(dnum, 1, 10000):
#             assert n < 10000
#             assert primes.ndivs(n) == dnum
#         for p, _ in factorize(n).iteritems():
#             assert p % 4 == 1
#         dset.add(n)
#     for n in range(1, 10000):
#         is4k1 = True
#         for p, _ in factorize(n).iteritems():
#             if p % 4 != 1:
#                 is4k1 = False
#                 break
#         if not is4k1: continue
#         if primes.ndivs(n) == dnum:
#             assert n in dset

sum_4p3_save = [0, 1, 3]

def sum_4p3(n):
    """Sum of all the numbers <= n with prime divs 2, 4k + 3."""
    if n >= len(sum_4p3_save):
        for k in range(len(sum_4p3_save), n + 1):
            no_4k1 = True
            for p, _ in factorize(k).iteritems():
                if p % 4 == 1:
                    no_4k1 = False
                    break
        if no_4k1: sum_4p3_save.append(sum_4p3_save[-1] + k)
        else: sum_4p3_save.append(sum_4p3_save[-1])
    return sum_4p3_save[n]

N = 10 ** 11
s = 0

for n in gen_4p1_dnum(105, 1, N * N + 1):
    k = int(math.sqrt(n) + 0.5)
    print n, k
    assert k * k == n
    print(k, N // k)
    s += sum_4p3(N // k) * k

print(s)
