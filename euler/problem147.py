'''
============================================================
http://projecteuler.net/problem=147

In a 3x2 cross-hatched grid, a total of 37 different rectangles could be situated within that grid as indicated in the sketch.


There are 5 grids smaller than 3x2, vertical and horizontal dimensions being important, i.e. 1x1, 2x1, 3x1, 1x2 and 2x2. If each of them is cross-hatched, the following number of different rectangles could be situated within those smaller grids:

1x1: 1 
2x1: 4 
3x1: 8 
1x2: 4 
2x2: 18

Adding those to the 37 of the 3x2 grid, a total of 72 different rectangles could be situated within 3x2 and smaller grids.

How many different rectangles could be situated within 47x43 and smaller grids?
============================================================
'''
import numpy as np

def type1(M, N):
    '''# of rectangles aligned with the vertical and horizontal axes. R[m,n] is the count for a mxn grid,
    m <= M, n <= N.'''
    n, m = np.meshgrid(xrange(N + 1), xrange(M + 1))
    return n * (n + 1) * m * (m + 1) / 4

def type2(M, N):
    '''# of tilted rectangles. R[m,n] is the count for a mxn grid, m <= M, n <= N.'''
    R = np.zeros((M + 1, N + 1), dtype=long)
    R[1, 1:N + 1] = np.arange(N)  # Initial Condition
    # Dynamic programming
    for m in xrange(2, M + 1):
        for n in xrange(1, min(N, m) + 1): R[m, n] = R[m - 1, n] + n * (4 * n * n - 1) / 3
        if m <= N: R[m, m] -= m
        t = m * (4 * m * m - 1) / 3
        for n in xrange(m + 1, N + 1): R[m, n] = R[m, n - 1] + t
    return R

'''Total number of rectangles in an MxN grid and smaller grids.'''
all_rect = lambda M, N: np.sum(type1(M, N) + type2(M, N))

if __name__ == "__main__":
    print all_rect(47, 43)
