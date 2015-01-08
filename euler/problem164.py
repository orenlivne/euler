'''
============================================================
http://projecteuler.net/problem=164

How many 20 digit numbers n (without any leading zero) exist such that no three consecutive digits of n have a sum greater than 9?
============================================================
'''
import numpy as np

def initial_counts(s):
    '''Dynamic programming - initial condition (n=2).'''
    x = np.zeros((10, 10), dtype=np.long)
    for i in xrange(1, 10):
        for j in xrange(min(9, s - i) + 1): x[i, j] = 1
    return x

def extend_counts(x, s):
    '''Dynamic programming - extend from length n-1 to length n.'''
    y = np.zeros((10, 10), dtype=np.long)
    for i in xrange(10):
        for j in xrange(min(9, s - i) + 1):
            xc = x[i, j]
            for k in xrange(min(9, s - i - j) + 1): y[j, k] += xc
    return y

def num_nums(s, n):
    '''Return the number of numbers of length n s.t. the sum of each 3 consecutive digits <= s.''' 
    s = max(0, min(9 * 3, s))
    x = initial_counts(s)
    for _ in xrange(n - 2): x = extend_counts(x, s)
    return sum(x.flatten())

if __name__ == "__main__":
    print num_nums(9, 20)  # 378158756814587
    print num_nums(12, 22)  # 1901304701829726005
