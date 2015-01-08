'''
============================================================
http://projecteuler.net/problem=18

By starting at the top of the triangle below and moving to adjacent numbers on the row below, the maximum total from top to bottom is 23.

3
7 4
2 4 6
8 5 9 3

That is, 3 + 7 + 4 + 9 = 23.

Find the maximum total from top to bottom of the triangle below:

75
95 64
17 47 82
18 35 87 10
20 04 82 47 65
19 01 23 75 03 34
88 02 77 73 07 63 67
99 65 04 28 06 16 70 92
41 41 26 56 83 40 80 70 33
41 48 72 33 47 32 37 16 94 29
53 71 44 65 25 43 91 52 97 51 14
70 11 33 28 77 73 17 78 39 68 17 57
91 71 52 38 17 14 91 43 58 50 27 29 48
63 66 04 68 89 53 67 30 73 16 69 87 40 31
04 62 98 27 23 09 70 98 73 93 38 53 60 04 23

NOTE: As there are only 16384 routes, it is possible to solve this problem by trying every route. However, Problem 67, is the same challenge with a triangle containing one-hundred rows; it cannot be solved by brute force, and requires a clever method! ;o)

Created on Feb 21, 2013
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
import numpy as np
from numpy.ma.testutils import assert_equal

def read_triangle(f):
    '''Read triangle data from input Stream. Stream rows.'''
    return (np.array(map(int, line.split(' ')), dtype=np.int) for line in f)

def max_total(triangle):
    '''Max total of path in a triangle, top to bottom.'''
    prev = []           # Could be omitted, but PyDev will rightfully complain
    for a in triangle:  # Loop over rows, top to bottom
        i = len(a) - 1
        p = np.zeros_like(a)
        if i == 0:                                               # Initial condition
            p[0] = a[0]
        else:
            p[0] = prev[0] + a[0]                                # Left boundary
            p[i] = prev[i - 1] + a[i]                            # Right boundary
            p[1:i] = np.maximum(prev[0:-1], prev[1:]) + a[1:i]   # Recursion
        prev = p
    return np.max(prev)                                          # Final condition

if __name__ == "__main__":
    assert_equal(max_total(read_triangle(open('problem018-small.dat', 'rb'))), 23, 'Wrong sum')
    assert_equal(max_total(read_triangle(open('problem018.dat', 'rb'))), 1074, 'Wrong sum')
#    import doctest
#    doctest.testmod()
