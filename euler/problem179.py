'''
============================================================
http://projecteuler.net/problem=179

Find the number of integers 1  n  107, for which n and n + 1 have the same number of positive divisors. For example, 14 has the positive divisors 1, 2, 7, 14 while 15 has 1, 3, 5, 15.
============================================================
'''
import numpy as np

def num_divisors(N):
    d = np.ones((N,), dtype=np.uint)
    for n in xrange(2, N): d[n::n] += 1
    d[0] = 0
    return d

num_consecutive_eq = lambda a: sum(1 for k in xrange(len(a) - 1) if a[k] == a[k + 1])

def num_divisors_bf(n):
    '''O(sqrt(n))-complexity brute force to find the list of divisors of n.'''
    #if n % 10000 == 0: print n
    i, count = 2, 1 if n == 1 else 2  # accounts for 'n' and '1'
    while i ** 2 < n:
        if n % i == 0: count += 2
        i += 1
    if i ** 2 == n: count += 1
    return count

if __name__ == "__main__":
    import time
    N = 10 ** 7
    start = time.time()    
    print num_consecutive_eq(num_divisors(N))
    print time.time() - start, 'sec'
    start = time.time()    
    print num_consecutive_eq(map(num_divisors_bf, xrange(2, N)))
    print time.time() - start, 'sec'
