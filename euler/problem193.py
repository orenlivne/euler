'''
============================================================
http://projecteuler.net/problem=193

A positive integer n is called squarefree, if no square of a prime divides n,
thus 1, 2, 3, 5, 6, 7, 10, 11 are squarefree, but not 4, 8, 9, 12.
How many squarefree numbers are there below 2**50?
============================================================
'''
from problem007 import primes
from math import ceil

def sf(N):
    '''Returns the number of square-free numbers <= N.'''
    # Count the number of NON-square-free numbers x <= N of the form x = q^2 * y. q is composed of
    # primes <= sqrt(N), so we first enumerate all q = a single prime; thus we've counted q's of the
    # form p1*p2 twice, so we subtract combinations of two primes, add back combinations of three, etc.
    # (the inclusion-exclusion principle). 
    N2 = N ** 0.5
    P = map(long, primes('lt', int(ceil(N2)) + 1))
    s, combos, count, index_of = 1, [((p,), p) for p in P], sum(N / (q * q) for q in P), dict((v, k) for k, v in enumerate(P))
    while combos:
        # While there exist combinations (seq) of primes whose product (q) <= sqrt(N), append
        # all possible primes to each such combinations such that the product remains <= sqrt(N).
        c = []
        for seq, q in combos:
            r_max = int(N2 / q)
            for j in xrange(index_of[seq[-1]] + 1, len(combos)):
                r = P[j]
                if r > r_max: break
                c.append((seq + (r,), q * r))
        combos = c
        # Flip sign of these sequences' contributions - the inclusion- exclusion principle
        s = -s
        tot = s * sum(N / (q * q) for _, q in combos)
        count += tot
    # Return the complement of non-square-free numbers
    return N - count

if __name__ == "__main__":
    print sf(2 ** 50 - 1)
