'''
============================================================
http://projecteuler.net/problem=75

It turns out that 12 cm is the smallest length of wire that can be bent to form an integer sided right angle triangle in exactly one way, but there are many more examples.

12 cm: (3,4,5)
24 cm: (6,8,10)
30 cm: (5,12,13)
36 cm: (9,12,15)
40 cm: (8,15,17)
48 cm: (12,16,20)

In contrast, some lengths of wire, like 20 cm, cannot be bent to form an integer sided right angle triangle, and other lengths allow more than one solution to be found; for example, using 120 cm it is possible to form exactly three different integer sided right angle triangles.

120 cm: (30,40,50), (20,48,52), (24,45,51)

Given that L is the length of the wire, for how many values of L  1,500,000 can exactly one integer sided right angle triangle be formed?
============================================================
'''
from itertools import ifilter
from math import ceil
from euler.problem005 import gcd

def is_unique_perimeter(s):
    if s % 100000 == 0: print s
    s2, count = s / 2, 0
    for m in ifilter(lambda m: s2 % m == 0, xrange(2, int(ceil(s2 ** 0.5)))):
        sm = s2 / m  # s/(2m), need to find odd factor k of
        while sm % 2 == 0: sm /= 2  # Reduce search space of odd factors kby removing all 2-factors
        for k in xrange(m + 1 + (m % 2), min(2 * m, sm + 1), 2):
            if sm % k == 0 and gcd(k, m) == 1:
                d, n = s2 / (k * m), k - m
                m2, n2 = m * m, n * n
                a, b = d * (m2 - n2), 2 * d * m * n
                if a > b: a, b = b, a
                count += 1
                if count == 1: a1, b1 = a, b
                elif count == 2 and a == a1 and b == b1: return False
    return count == 1
            
if __name__ == "__main__":
    print sum(1 for x in xrange(2, 1500000, 2) if is_unique_perimeter(x))
