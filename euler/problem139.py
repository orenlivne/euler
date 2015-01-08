'''
============================================================
http://projecteuler.net/problem=138

============================================================
'''
from problem094 import pell_solutions
from problem005 import gcd
from itertools import islice, takewhile

def num_triples(N):
    count, do = 0, {-1: True, 1: True}
    for y, x in islice(pell_solutions(2, -1), 1, None):
        cont = False
        for t in (t for t in [-1, 1] if do[t]):
            g = gcd(x + t, y - x)
            if ((y + t) / g) % 2:
                s = 2 * (x + t) * (y + t) / (g * g)
                if s <= N:
                    count += (N / s)
                    cont = True
                else: do[t] = False
        if not cont: break
    return count

def num_triples_brute_force(N):
    count = 0
    for m in xrange(2, N):
        for n in (n for n in xrange(m % 2 + 1, m, 2) if gcd(m, n) == 1):
            A, B, C = m * m - n * n, 2 * m * n, m * m + n * n
            for k in takewhile(lambda k: (A + B + C) * k <= N, count(1)):
                a, b, c = k * A, k * B, k * C
                if c % (b - a) == 0:
                    count += 1
    return count

if __name__ == "__main__":
    print num_triples(100), num_triples_brute_force(100)
    print num_triples(10 ** 8 - 1)
