'''
============================================================
http://rosalind.info/problems/mgap

For the computation of an alignment score generalizing the edit alignment score, let m denote the score assigned to matched symbols, d denote the score assigned to mismatched non-gap symbols, and g denote the score assigned a symbol matched to a gap symbol '-' (i.e., g is a linear gap penalty).

Given: Two DNA strings s and t in FASTA format (each of length at most 5000 bp).

Return: The maximum number of gap symbols that can appear in any maximum score alignment of s and t with score parameters satisfying m>0, d<0, and g<0.
============================================================
'''
import rosalind.rosutil as ro, numpy as np

def max_gap_length(x, y, p=100, d= -100, g= -1, debug=False):
    '''Integrated DP+backtracking, O(mn) time, O(min(m,n)) storage.'''
    m, n = len(x), len(y)
    if m < n: return max_gap_length(y, x, p=p, d=d, g=g, debug=debug)
    f, f_old = zip(g * np.arange(n + 1), range(n + 1)), [None] * (n + 1)
    if debug: print f
    for xi in x:
        f_old[:] = f[:]  # Advance to next row
        f[0] = (f_old[0][0] + g, 0, f_old[0][1] + 1)  # Initial condition 
        for j, yj in enumerate(y, 1):
            f[j] = max((f_old[j - 1][0] + (p if xi == yj else d), f_old[j - 1][1]),
                       (f_old[j][0] + g, f_old[j][1] + 1), (f[j - 1][0] + g, f[j - 1][1] + 1))
        if debug: print f
    return f[-1][1]

def mgap(f, debug=False):
    '''Main driver to solve this problem.'''
    x, y = ro.fafsa_values(f)
    return max_gap_length(x, y, debug=debug)

if __name__ == "__main__":
    print mgap('rosalind_mgap_sample.dat')
    print mgap('rosalind_mgap.dat')
