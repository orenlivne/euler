'''
============================================================
http://projecteuler.net/problem=82

NOTE: This problem is a more challenging version of Problem 81.

The minimal path sum in the 5 by 5 matrix below, by starting in any cell in the left column and finishing in any cell in the right column, and only moving up, down, and right, is indicated in red and bold; the sum is equal to 994.

131    673    234    103    18
201    96    342    965    150
630    803    746    422    111
537    699    497    121    956
805    732    524    37    331

Find the minimal path sum, in matrix.txt (right click and 'Save Link/Target As...'), a 31K text file containing a 80 by 80 matrix, from the left column to the right column.
============================================================
'''
import numpy as np

def min_path_sum2(A):
    a = A[0]
    s, n = a.copy(), len(a)
    for a in A[1:, :]:
        s[0] += a[0]
        for j in xrange(1, n): s[j] = min(s[j], s[j - 1]) + a[j]
        for j in xrange(n - 2, -1, -1): s[j] = min(s[j], s[j + 1] + a[j])
    return min(s)

if __name__ == "__main__":
    # print min_path_sum2(np.loadtxt('problem082-sample.dat', delimiter=',', dtype=int).transpose())
    print min_path_sum2(np.loadtxt('problem081.dat', delimiter=',', dtype=int).transpose())
