'''
============================================================
http://rosalind.info/problems/ctea

Recall from "Edit Distance Alignment" that if s' and t' are
the augmented strings corresponding to an alignment of
strings s and t, then the edit alignment score of s' and t'
was given by the Hamming distance dH(s',t') (because s' and
t' have the same length and already include gap symbols to
denote insertions/deletions).

As a result, we obtain dE(s,t)=mins',t'dH(s',t'), where the minimum is taken over all alignments of s and t. Strings s' and t' achieving this minimum correspond to an optimal alignment with respect to edit alignment score.

Given: Two protein strings s and t in FASTA format, each of length at most 1000 aa.

Return: The total number of optimal alignments of s and t with respect to edit alignment score, modulo 134,217,727 (2**27-1).
============================================================
'''
import rosalind.rosutil as ro

def cost(x, y):
    '''A cost function.'''
    if x == None: return 1  # Cost of insertion of y
    if y == None: return 1  # Cost of deletion of x
    return 0 if x == y else 1  # Cost of substituting y for x

def edit_distance_and_count(x, y, r, debug=False):
    '''Integrated DP+backtracking, O(mn) time, O(min(m,n)) storage.'''
    m, n = len(x), len(y)
    if m < n: return edit_distance_and_count(y, x, r, debug=debug)
    c, c_old = zip(range(n + 1), [1] * (n + 1)), [None] * (n + 1)
    if debug: print c
    for xi in x:
        c_old[:] = c[:]
        # Initial condition
        c[0] = (c_old[0][0] + 1, c_old[0][1]) 
        for j, yj in enumerate(y, 1):
            c_prev = ((cost(xi, yj), c_old[j - 1]), (cost(None, yj), c_old[j]), (cost(xi, None), c[j - 1]))
            d = min((z[0] + z[1][0]) for z in c_prev)
            c[j] = (d, ro.sum_mod((z[1][1] for z in c_prev if z[0] + z[1][0] == d), r))
        if debug: print c
    return c[-1][1]

def ctea(f, debug=False):
    '''Main driver to solve this problem.'''
    x, y = ro.fafsa_values(f)
    return edit_distance_and_count(x, y, 2 ** 27 - 1, debug=debug)

if __name__ == "__main__":
    print ctea('rosalind_ctea_sample.dat')
    print ctea('rosalind_ctea.dat')
