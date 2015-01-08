'''
============================================================
http://projecteuler.net/problem=149

Problem 149
Looking at the table below, it is easy to verify that the maximum possible sum of adjacent numbers in any direction (horizontal, vertical, diagonal or anti-diagonal) is 16 (= 8 + 7 + 1).

2    5    3    2
9    6    5    1
3    2    7    3
1    8    4      8
Now, let us repeat the search, but on a much larger scale:

First, generate four million pseudo-random numbers using a specific form of what is known as a "Lagged Fibonacci Generator":

For 1  k  55, sk = [100003  200003k + 300007k3] (modulo 1000000)  500000.
For 56  k  4000000, sk = [sk24 + sk55 + 1000000] (modulo 1000000)  500000.

Thus, s10 = 393027 and s100 = 86613.

The terms of s are then arranged in a 20002000 table, using the first 2000 numbers to fill the first row (sequentially), the next 2000 numbers to fill the second row, and so on.

Finally, find the greatest sum of (any number of) adjacent entries in any direction (horizontal, vertical, diagonal or anti-diagonal).
============================================================
'''
import numpy as np, sys

MIN_INT = -sys.maxint - 1

def test_matrix():
    '''Generate the Lagged Fibonacci Generator test data.'''
    s = [(100003 - 200003 * k + 300007 * k ** 3) % 1000000 - 500000 for k in xrange(1, 56)]
    for k in xrange(56, 4000000): s.append((s[k - 25] + s[k - 56] + 1000000) % 1000000 - 500000)
    a = np.array(s)
    a.resize((2000, 2000))
    return a

def max_sub_sum(a):
    '''Maximum subsequence sum in the sequence a.'''
    max_ending_here = max_so_far = MIN_INT
    for x in a:
        max_ending_here = x + max(0L, max_ending_here)
        #max_ending_here = max(0L, max_ending_here + x)
        max_so_far = max(max_so_far, max_ending_here)
    return max_so_far

def max_sub_sum_2d(a):
    '''Max in any direction. a is an nxn numpy array.'''
    n = a.shape[0]
    return max(max(max_sub_sum(a[i, :]) for i in xrange(n)),
               max(max_sub_sum(a[:, i]) for i in xrange(n)),
               max(max_sub_sum(a[i, i + j] for i in xrange(n - j)) for j in xrange(n)),
               max(max_sub_sum(a[i + j, i] for i in xrange(n - j)) for j in xrange(1, n)),
               max(max_sub_sum(a[n - 1 - i, i + j] for i in xrange(n - j)) for j in xrange(n)),
               max(max_sub_sum(a[n - 1 - i - j, i] for i in xrange(n - j)) for j in xrange(1, n)))
    
max_subseq_sum_bf = lambda a: max(sum(a[i:j]) for i in xrange(len(a)) for j in xrange(i + 1, len(a) + 1))

if __name__ == "__main__":
    a = [9, 3, 7, 2, 4, 5, 8, 1, -10, 6]
    print max_subseq_sum_bf(a), max_sub_sum(a)
    print max_sub_sum_2d(test_matrix())
