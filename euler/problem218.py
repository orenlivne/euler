'''
============================================================
http://projecteuler.net/problem=218

Consider the right angled triangle with sides a=7, b=24 and c=25. The area of this triangle is 84, which is divisible by the perfect numbers 6 and 28.
Moreover it is a primitive right angled triangle as gcd(a,b)=1 and gcd(b,c)=1.
Also c is a perfect square.

We will call a right angled triangle perfect if
-it is a primitive right angled triangle
-its hypotenuse is a perfect square

We will call a right angled triangle super-perfect if
-it is a perfect right angled triangle and
-its area is a multiple of the perfect numbers 6 and 28.

How many perfect right-angled triangles with c <= 10**16 exist that are not super-perfect?
============================================================
'''
from problem005 import gcd
import itertools

def num_perfect(L):
    '''Enumerate primitive triples whose hypotenuse is a perfect square r^2 (i.e., r is the hypotenuse
    the primitive triplet (m,n,r), where m,n parametrize the original triples. Look for those that
    don''t yield an area divisible by 84.'''
    s, L2 = 0, L ** 0.5
    for N in (N for N in xrange(1, int((L2 / 2) ** 0.5) + 1) if N % 4 != 0):
        N2 = N * N
        for M in (M for M in xrange(N + 1, int(L2 - N2) + 1, 2) if M % 4 != 0 and gcd(M, N) == 1):
            m, n = M * M - N2, 2 * M * N
            if ((m * m - n * n) * m * n % 84 != 0): s += 1
    return s

if __name__ == "__main__":
    # The easy way: if no combination of remainders s = m mod 42, t = n mod 42 yields an area/2 that's
    # not divisible by 42, no non-super-perfect triplet can exist. Note: the area is always even. 
    p = 42
    if not [(s, t) for (s, t) in itertools.product(xrange(p), xrange(p)) if (s * t * (t * t - s * s) * ((2 * t * s) ** 2 - (t * t - s * s) ** 2)) % p]:
        print 0
    # The hard way
    #print num_perfect(10 ** 16)
