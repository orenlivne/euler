'''
============================================================
http://projecteuler.net/problem=174

We shall define a square lamina to be a square outline with a square "hole" so that the shape possesses vertical and horizontal symmetry.

Given eight tiles it is possible to form a lamina in only one way: 3x3 square with a 1x1 hole in the middle. However, using thirty-two tiles it is possible to form two distinct laminae.


If t represents the number of tiles used, we shall say that t = 8 is type L(1) and t = 32 is type L(2).

Let N(n) be the number of t  1000000 such that t is type L(n); for example, N(15) = 832.

What is sum N(n) for 1  n  10?
============================================================
'''
def sum_N(T, max_N):
    L, T = {}, 0.25 * T
    for x in xrange(1, int(T ** 0.5) + 1):
        for b in xrange(1, int(T / x) - x + 1):
            t = 4 * x * (x + b)
            if L.has_key(t): L[t] = L[t] + 1
            else: L[t] = 1
    return sum(1 for l in L.itervalues() if l <= max_N)

if __name__ == "__main__":
    print sum_N(10 ** 6, 10)
