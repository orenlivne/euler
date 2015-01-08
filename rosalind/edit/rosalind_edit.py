'''
============================================================
http://rosalind.info/problems/edit

Given two strings s and t (of possibly different lengths), the edit distance dE(s,t) is the minimum number of edit operations needed to transform s into t, where an edit operation is defined as the substitution, insertion, or deletion of a single symbol.

The latter two operations incorporate the case in which a contiguous interval is inserted into or deleted from a string; such an interval is called a gap. For the purposes of this problem, the insertion or deletion of a gap of length k still counts as k distinct edit operations.

Given: Two protein strings s and t in FASTA format (each of length at most 1000 aa).

Return: The edit distance dE(s,t).
============================================================
'''
import rosalind.rosutil as ro, numpy as np

def edit_distance(x, y):
    '''DP to find LCS length of all sub-problems.
    Note: no need to store a 2-D array as done here, really, we can do row by row, cf. below.'''
    m, n = len(x), len(y)
    c = np.zeros((m + 1, n + 1), dtype=int)
    # Initial conditions
    c[:, 0] = np.arange(m + 1)
    c[0, :] = np.arange(n + 1)
    # Dynamic programming
    for i in xrange(1, m + 1):
        for j in xrange(1, n + 1): c[i, j] = c[i - 1, j - 1] if x[i - 1] == y[j - 1] else min(c[i - 1, j], c[i, j - 1], c[i - 1, j - 1]) + 1
    return c[-1, -1]

def edit_distance_lean(x, y):
    '''Lean storage row-by-row DP, O(mn) time, O(min(m,n)) storage.'''
    m, n = len(x), len(y)
    if m < n: return edit_distance_lean(y, x)
    c, c_old = range(n + 1), [0] * (n + 1)
    for i, xi in enumerate(x, 1):
        c_old[:] = c[:]
        c[0] = i
        for j, yj in enumerate(y, 1): c[j] = c_old[j - 1] if xi == yj else min(c_old[j - 1], c_old[j], c[j - 1]) + 1
    return c[-1]

def edit(f):
    '''Main driver to solve this problem.'''
    return edit_distance(*ro.fafsa_values(f)), edit_distance_lean(*ro.fafsa_values(f))

if __name__ == "__main__":
    print edit('rosalind_edit_sample.dat')
    print edit('rosalind_edit.dat')
