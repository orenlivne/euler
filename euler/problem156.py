'''
============================================================
http://projecteuler.net/problem=156

Starting from zero the natural numbers are written down in base 10 like this: 
0 1 2 3 4 5 6 7 8 9 10 11 12....

Consider the digit d=1. After we write down each number n, we will update the number of ones that have occurred and call this number f(n,1). The first values for f(n,1), then, are as follows:

n    f(n,1)
0    0
1    1
2    1
3    1
4    1
5    1
6    1
7    1
8    1
9    1
10    2
11    4
12    5
Note that f(n,1) never equals 3. 
So the first two solutions of the equation f(n,1)=n are n=0 and n=1. The next solution is n=199981.

In the same manner the function f(n,d) gives the total number of digits d that have been written down after the number n has been written. 
In fact, for every digit d != 0, 0 is the first solution of the equation f(n,d)=n.

Let s(d) be the sum of all the solutions for which f(n,d)=n. 
You are given that s(1)=22786974071.

Find  SUM s(d) for 1 <= d <= 9.

Note: if, for some n, f(n,d)=n for more than one value of d this value of n is counted again for every value of d for which f(n,d)=n.
============================================================
'''
import itertools as it
from math import log10, ceil
from numpy import abs, linspace

def num_digits(n):
    '''Return the number of digits in the decimal number n >= 1.'''
    k = log10(n)
    return (int(k) + 1) if k < int(k) + 1e-12 else int(ceil(k))

def f(d, n):
    '''Evaluate f in O(log n) operations.'''
    if n == 0: return 0
    result, k = 0L, num_digits(n) - 1
    r = 10L ** k
    while k >= 0:
        p, q = divmod(n, r)
        result += (0 if k == 0 else p * k * (r / 10)) + (r if p > d else 0) + ((q + 1) if p == d else 0)
        k, r, n = k - 1, r / 10, q
    return result

'''We want to find the roots of this function.'''
g = lambda d, n: f(d, n) - n

'''Sum of roots for digit d.'''
S = lambda d: sum(all_roots(d))

'''Brute-force search within [n1,n2].'''
bf_search = lambda d, n1, n2: (n for n in it.islice(it.count(n1), n2 - n1 + 1) if g(d, n) == 0)

def all_roots(d, h=100000L, n_bf=100L, n_small=20):
    '''Return all roots for digit d. Assuming a minimum separation of n=h between root clusters.
    n <= n_small is done by brute-force. For smaller n, divide the range of feasible n''s into equal
    size intervals of size ~ h (=minimum root cluster separation; roots seems to come in clusters
    of consecutive n''s that are quite far from each other). Narrow down the search within each
    interval using bisection or derivative searches until the interval becomes at most n_bf wide.
    Then search the smaller interval with brute-force.'''
    # Small n
    for n in bf_search(d, 0, n_small - 1): yield n
    # Large n: break into interval
    n_max = upper_limit(d)
    N = map(long, linspace(n_small, n_max, n_max / h))
    for i in xrange(len(N) - 1):
        n1, n2 = N[i], N[i + 1] - 1
        # Decide which strategy to use based on endpoint g-signs
        search = bisection_search if g(d, n1) * g(d, n2) < 0 else deriv_search
        # Narrow down the large interval [n1,n2] into smaller sub-intervals [m1,m2]
        for m1, m2 in search(d, n1, n2, n_bf):
            # Search in each sub-interval using brute-force 
            for n in bf_search(d, m1, m2): yield n

def upper_limit(d, n_max=10 ** 11L, t=1e9, h=0.9):
    '''Find the upper limit on roots. We know g tends to infinity for n->infinity and > 0 for all
    n_max ~ 10**11 (by analysis and observation). Start at this n_max and cut it by a factor of h
    until |g|<t, where is a threshold.'''
    while g(d, n_max) > t: n_max = long(h * n_max)
    return long(n_max / h)

def bisection_search(d, n1, n2, n_bf, t=1000):
    '''Opposite-sign endpoints, assuming a single root cluster. Bisection search that
    narrows down the interval [n1,n2] where to a smaller interval |g|<=t, and yields its endpoints.'''
    g1, g2 = g(d, n1), g(d, n2)
    while abs(n1 - n2) > n_bf and max(abs(g1), abs(g2)) > t:
        mid = (n1 + n2) / 2
        gm = g(d, mid)
        n1, n2, g1, g2 = (n1, mid, g1, gm) if g1 * gm < 0 else (mid, n2, gm, g2)
    yield n1, n2

def deriv_search(d, n1, n2, n_bf, nd=10, t=10000):
    '''Same-sign endpoints. Likely a single root cluster where g touches zero without 
    (significantly) crossing it. Check where derivative changes sign or function is small.
    Yield all such sub-intervals (with |g|<=t) in case we are unlucky and there is more than one
    cluster in [n1,n2].''' 
    N = map(long, linspace(n1, n2, nd))
    G = [g(d, n) for n in N]
    d = [i for i in xrange(len(N) - 1) if G[i] * G[i + 1] < 0 or min(abs(G[i]), abs(G[i + 1])) < t]
    for i in d: yield N[i], N[i + 1]

if __name__ == "__main__":
    print sum(S(d) for d in xrange(1, 10))
