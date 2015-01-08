'''
============================================================
http://projecteuler.net/problem=124

The radical of n, rad(n), is the product of distinct prime factors of n. For example, 504 = 23  32  7, so rad(504) = 2  3  7 = 42.

If we calculate rad(n) for 1  n  10, then sort them on rad(n), and sorting on n if the radical values are equal, we get:

Unsorted
     
Sorted

n

rad(n)


n

rad(n)

k
1
1
     
1
1
1
2
2
     
2
2
2
3
3
     
4
2
3
4
2
     
8
2
4
5
5
     
3
3
5
6
6
     
9
3
6
7
7
     
5
5
7
8
2
     
6
6
8
9
3
     
7
7
9
10
10
     
10
10
10
Let E(k) be the kth element in the sorted n column; for example, E(4) = 8 and E(6) = 9.

If rad(n) is sorted for 1  n  100000, find E(10000).
============================================================
'''
import numpy as np
# from problem012 import factorize
from problem007 import primes

def E(n):
    # Slow!
    #     r = np.array(list(enumerate([0] + [np.prod(factorize(x).keys()) for x in xrange(1, n + 1)])), dtype=np.uint)
    #     return r[np.lexsort((r[:, 0], r[:, 1]))]
    r = np.ones((n + 1,), dtype=np.uint)
    for p in primes('lt', n + 1): r[p::p] *= p
    return sorted(enumerate(r), key=lambda (n, r): (r, n))

if __name__ == "__main__":
    print E(100000)[10000][0]
