'''
============================================================
http://projecteuler.net/problem=345

We define the Matrix Sum of a matrix as the maximum sum of matrix elements with each element being the only one in his row and column. For example, the Matrix Sum of the matrix below equals 3315 ( = 863 + 383 + 343 + 959 + 767):

  7  53 183 439 863
497 383 563  79 973
287  63 343 169 583
627 343 773 959 943
767 473 103 699 303
Find the Matrix Sum of:

  7  53 183 439 863 497 383 563  79 973 287  63 343 169 583
627 343 773 959 943 767 473 103 699 303 957 703 583 639 913
447 283 463  29  23 487 463 993 119 883 327 493 423 159 743
217 623   3 399 853 407 103 983  89 463 290 516 212 462 350
960 376 682 962 300 780 486 502 912 800 250 346 172 812 350
870 456 192 162 593 473 915  45 989 873 823 965 425 329 803
973 965 905 919 133 673 665 235 509 613 673 815 165 992 326
322 148 972 962 286 255 941 541 265 323 925 281 601  95 973
445 721  11 525 473  65 511 164 138 672  18 428 154 448 848
414 456 310 312 798 104 566 520 302 248 694 976 430 392 198
184 829 373 181 631 101 969 613 840 740 778 458 284 760 390
821 461 843 513  17 901 711 993 293 157 274  94 192 156 574
 34 124   4 878 450 476 712 914 838 669 875 299 823 329 699
815 559 813 459 522 788 168 586 966 232 308 833 251 631 107
813 883 451 509 615  77 281 613 459 205 380 274 302  35 805
============================================================
'''
# '''ith row, jth column removed.'''
# minor = lambda arr, i, j: arr[np.array(range(i) + range(i + 1, arr.shape[0]))[:, np.newaxis],
#                np.array(range(j) + range(j + 1, arr.shape[1]))]
# 
# '''Brute-force minimum search. For an nxn matrix a, the complexity is O(n!).'''
# max_perm_sum_bf = lambda a: a[0][0] if a.size == 1 else \
# max(a[0][j] + max_perm_sum_bf(minor(a, 0, j)) for j in xrange(a.shape[1]))
# 
# min_perm_sum_bf = lambda a: a[0][0] if a.size == 1 else \
# min(a[0][j] + min_perm_sum_bf(minor(a, 0, j)) for j in xrange(a.shape[1]))
# 
# def max_perm_sum(a):
#     n = len(a)
#     b, is_remaining, remaining, col = a.copy(), np.array([True] * n, dtype=bool), set(range(n)), np.zeros((n,), dtype=int)
#     # Row reduction steps (top-down)
#     print b
#     for i in xrange(n - 1):
#         b[i + 1:] -= np.tile(b[i], (n - i - 1, 1))
#         print b
#     # Back-tracking to recover locations of max-sum permutation (bottom-up)
#     for i in xrange(n - 1, -1, -1):
#         r = np.array(list(remaining))
#         j_max = r[np.argmax(b[i][is_remaining])]
#         col[i] = j_max
#         is_remaining[j_max] = False
#         remaining.remove(j_max)
#     return sum(a[np.arange(n), col])
# 
# assignment_sum = lambda a, x: sum(a[np.arange(a.shape[0]), x])
# 
# def min_assignment(a):
#     '''Implementation of the Hungarian Algorithm for min-sum assignment in the square array a.'''
#     n, b = a.shape[0], a.copy()
#     for i in xrange(n): b[i] -= min(b[i])
#     for j in xrange(n): b[:, j] -= min(b[:, j])
#     while True:
#         print b
#         uncovered_rows = np.array([len(np.where(b[i] == 0)[0]) > 0 for i in xrange(n)])
#         lines = (np.where(~uncovered_rows)[0], np.unique(np.where(b[uncovered_rows] == 0)[1]))
#         print 'lines', lines
#         if sum(map(len, lines)) == n: return assignment_sum(a, assignment(b))
#         uncovered_cols = np.array(list(set(np.arange(n)) - set(lines[1])))
#         if uncovered_rows.size and uncovered_cols.size:
#             b_min = min(b[uncovered_rows, uncovered_cols])
#             b[uncovered_rows] -= b_min
#             b[:, lines[1]] += b_min
#     
# assignment = lambda a: _assign(zip(*np.where(a == 0)), [], a.shape[0])
# 
# def _assign(z, assigned, n, count=0):
#     '''Depth-first search to create an assignment of rows and columns from a list of zero-entry
#     locations in the nxn array n. Returns an array of column indices of rows 0..n-1 in the assignment.'''
#     # If current branch a leaf or a dead-end, return a result
#     print '  ' * count, 'z', z, 'assigned', assigned
#     if len(assigned) == n:
#         return np.array([x[1] for x in sorted(assigned)])
#     if not z: return None  # Optimization, contained in the next condition
#     print '  ' * count, [len(np.unique([x[m] for x in z])) < n for m in (0, 1)]
#     #if any(len(np.unique([x[m] for x in z])) < n for m in (0, 1)): return None
#     # Search branches
#     for x in z:
#         print '  ' * (count + 1), 'Assigning x', x 
#         complete = _assign([(a, b) for a, b in z if a != x[0] and b != x[1]], assigned + [x], n, count + 1)
#         if complete is not None: return complete

import numpy as np
from munkres import Munkres

min_cost_munkres = lambda a: sum(a[row][column] for row, column in Munkres().compute(a.tolist()))
    
def min_to_max(min_computer, a):
    a_max = a.max()
    return len(a) * a_max - min_computer(a_max - a) 

if __name__ == "__main__":
    print min_to_max(min_cost_munkres, np.loadtxt('problem345-large.dat', dtype=long))
