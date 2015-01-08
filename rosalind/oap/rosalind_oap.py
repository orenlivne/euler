'''
============================================================
http://rosalind.info/problems/oap

An overlap alignment between two strings s and t is a local
alignment of a suffix of s with a prefix of t. An optimal
overlap alignment will therefore maximize an alignment score
over all such substrings of s and t.

The term "overlap alignment" has also been used to describe
what Rosalind defines as a semiglobal alignment. See
"Semiglobal Alignment" for details.

Given: Two DNA strings s and t in FASTA format, each having
length at most 10 kbp.

Return: The score of an optimal overlap alignment of s and
t, followed by an alignment of a suffix s' of s and a prefix
t' of t achieving this optimal score. Use an alignment score
in which matching symbols count +1, substitutions count -2,
and there is a linear gap penalty of 2. If multiple optimal
alignments exist, then you may return any one.
============================================================
'''
import rosalind.rosutil as ro, numpy as np, time

def semi_global_alignment((x, y), score, gap_score, debug=False):
    '''Optimal overlap alignment of the strings x,y. Returns the full DP matrix'''
    m, n = len(x), len(y)
    c = np.zeros((m + 1, n + 1), dtype=int)
    I = np.zeros((m + 1, n + 1), dtype=int)
    J = np.zeros((m + 1, n + 1), dtype=int)
    # Initial conditions on first row & column
    c[0, :] = [0 for _ in xrange(n + 1)] 
    c[:, 0] = [0 for _ in xrange(m + 1)]
    # Dynamic programming
    if debug:
        print m, n
        start = time.time()
    for i, xi in enumerate(x, 1):
        if debug:
            if i % 100 == 0: print i, time.time() - start
        for j, yj in enumerate(y, 1):
            c1 = c[i - 1, j - 1] + (1 if xi == yj else -2)
            c2 = c[i - 1, j] + gap_score
            c3 = c[i, j - 1] + gap_score
            c_max = max(c1, c2, c3)
            if c_max == c1: i_prev, j_prev = i - 1, j - 1
            elif c_max == c2: i_prev, j_prev = i - 1, j
            else: i_prev, j_prev = i, j - 1
            c[i, j] = c_max
            I[i, j] = i_prev
            J[i, j] = j_prev
    return c, I, J

def alignment_from_matrix((x, y), (i, j), c, I, J, gap_symbol='-'):
    '''Return the augmented-aligned strings of the original strings x and y
    from the DP matrix (result of global_alignment_matrix()) c. Start path back-tracking
    at element (i,j) in c.'''
    s, t = '', ''
    while i and j:  # Stop when the first row or column is hit
        ip, jp = I[i, j], J[i, j]
        s, t = (gap_symbol if ip == i else x[i - 1]) + s, (gap_symbol if jp == j else y[j - 1]) + t
        i, j = ip, jp
    return s, t

def oap(f, debug=False):
    '''Main driver to solve this problem.'''
    x, y = ro.fafsa_values(f)
    score = lambda x, y: 1 if x == y else -2
    c, I, J = semi_global_alignment((x, y), score, -2, debug=debug)
    row_max = (np.argmax(c[:, -1]), len(y))
    col_max = (len(x), np.argmax(c[-1, :]))
    print c
    print row_max, col_max
    overall_max = row_max if c[row_max[0], row_max[1]] > c[col_max[0], col_max[1]] else col_max
    print c[overall_max[0], overall_max[1]]
    print ro.join_list(alignment_from_matrix((x, y), overall_max, c, I, J), delimiter='\n')

def a(): 
    oap('rosalind_oap_data1.dat')
    
if __name__ == "__main__":
    oap('oap/rosalind_oap_sample.dat')
    #oap('rosalind_oap.dat')
    
#     cProfile.run('a()', 'oap')
#     p = pstats.Stats('oap').strip_dirs()
#     p.sort_stats('cumulative').print_stats(50)
