'''
============================================================
http://projecteuler.net/problem=62

The cube, 41063625 (3453), can be permuted to produce two other cubes: 56623104 (3843) and 66430125 (4053). In fact, 41063625 is the smallest cube which has exactly three permutations of its digits which are also cube.

Find the smallest cube for which exactly five permutations of its digits are cube.
============================================================
'''
from itertools import dropwhile, count, imap
from math import ceil

def smallest_cube(k, p):
    rk = 1.0 / k
    for n in count(dropwhile(lambda n: reduce(lambda x, y:x * y, xrange(1, n + 1)) < p, count(1)).next()):
        s = {}
        for x in imap(lambda y: y ** k, xrange(int(ceil((10 ** (n - 1)) ** rk)), int((10 ** n - 1) ** rk) + 1)):
            s.setdefault(''.join(sorted(str(x))), set([])).add(x)
        eligible = [min(v) for v in s.itervalues() if len(v) == p]
        if eligible:
            return min(eligible)
    
if __name__ == "__main__":
    print smallest_cube(3, 3)  # 41063625
    print smallest_cube(3, 5)  # 127035954683
