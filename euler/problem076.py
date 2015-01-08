'''
============================================================
http://projecteuler.net/problem=76

It is possible to write five as a sum in exactly six different ways:

4 + 1
3 + 2
3 + 1 + 1
2 + 2 + 1
2 + 1 + 1 + 1
1 + 1 + 1 + 1 + 1

How many different ways can one hundred be written as a sum of at least two positive integers?
============================================================
'''
import numpy as np

def num_ways(N):
    p = np.zeros((N + 1, N), dtype=np.uint)  # B.C. 2 in lower-right half
    p[2:N + 1, 1] = 1  # B.C. 1
    p[2, 2:] = 1
    for n in xrange(3, N + 1):
        n2 = (n + 1) / 2
        print n, n2
        for k in xrange(2, n):
            p[n, k] = p[n, k - 1] + p[n - k, k] + (1 if k >= n2 else 0)
        p[n, n:] = p[n, n - 1]
    print p
    return p[N, N - 1]

if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
    print num_ways(5)
    print num_ways(6)
    print num_ways(7)
    print num_ways(100)
    print num_ways(250)
