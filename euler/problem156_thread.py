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
from numpy import log10, ceil

def num_digits(n):
    '''Return the number of digits in the decimal number n >= 1.'''
    k = log10(float(n))
    return (int(k) + 1) if k < int(k) + 1e-12 else int(ceil(k))

def f(d, n, K=None):
    '''Evaluate f in O(log n) operations.'''
    if n == 0: return 0
    K = K if K else num_digits(n)
    result, k = 0L, K - 1
    r = 10L ** k
    while k >= 0:
        p, q = divmod(n, r)
        result += (0 if k == 0 else p * k * (r / 10)) + (r if p > d else 0) + ((q + 1) if p == d else 0)
        k, r, n = k - 1, r / 10, q
    return result

def all_roots(d):
    '''Return all roots for digit d.'''
    n, n_max = 1L, long(d * 10 ** (10 * (1 + 1. / d)))
    while n <= n_max:
        k = num_digits(n)
        g = f(d, n, k) - n
        if g == 0:
            yield n
            n += 1
        else: n += max(abs(g) / k, 1) 

'''Sum of roots for digit d.'''
S = lambda d: sum(all_roots(d))

if __name__ == "__main__":
    print sum(S(d) for d in xrange(1, 10))
