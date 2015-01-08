'''
============================================================
http://projecteuler.net/problem=207

For some positive integers k, there exists an integer partition of the form   4**t = 2**t + k,
where 4t, 2t, and k are all positive integers and t is a real number.

The first two such partitions are 4**1 = 2**1 + 2 and 4**1.5849625... = 2**1.5849625... + 6.

Partitions where t is also an integer are called perfect.
For any m >= 1 let P(m) be the proportion of such partitions that are perfect with k <= m.
Thus P(6) = 1/2.

In the following table are listed some values of P(m)

   P(5) = 1/1
   P(10) = 1/2
   P(15) = 2/3
   P(20) = 1/2
   P(25) = 1/2
   P(30) = 2/5
   ...
   P(180) = 1/4
   P(185) = 3/13

Find the smallest m for which P(m) < 1/12345
============================================================
'''
from __future__ import division
import itertools as it
from math import ceil, log
from numpy import round, abs

is_int = lambda x: abs(x - round(x)) < 1e-12
S = lambda m: int((-1 + (1 + 4 * m) ** 0.5) * 0.5)

def min_m(r):
    '''Fast solution that searches for 2-power k-interval first, then locates the appropriate m value
    within that interval.'''
    p = it.dropwhile(lambda (i, k): S(k - 1) <= r * i, enumerate((2 ** t * (2 ** t - 1) for t in it.count(2)), 1)).next()[0]
    d = p * r
    d = (d + 1) if is_int(d) else int(ceil(d))
    return d * (d + 1)

def min_m_bf(r):
    '''Brute-force over all odd squares, for comparison.
    from https://github.com/hughdbrown/Project-Euler/blob/master/euler-207.py'''
    intCount, log2 = 0, log(2)
    for root in it.count(2):
        if is_int(log(root) / log2): intCount += 1
        if r * intCount < root - 1: return int(((2 * root - 1) ** 2 - 1) / 4)
        
if __name__ == "__main__":
    print min_m(12345), min_m_bf(12345)  # 44043947822 44043947822
    print min_m(123456), min_m_bf(123456)  # 6721458093506 6721458093506
    print min_m(123456789)  # 14647157190414572060
