'''
============================================================
http://rosalind.info/problems/smgb

A semiglobal alignment of strings s and t is an alignment in
which any gaps appearing as prefixes or suffixes of s and t
do not contribute to the alignment score.

Semiglobal alignment has sometimes also been called
'overlap alignment'. Rosalind defines overlap alignment
differently (see 'Overlap Alignment').

Given: Two DNA strings s and t in FASTA format, each having
length at most 10 kbp.

Return: The maximum semiglobal alignment score of s and t,
followed by an alignment of s and t achieving this maximum
score. Use an alignment score in which matching symbols count
+1, substitutions count -1, and there is a linear gap penalty of
1. If multiple optimal alignments exist, then you may return any one.

Sample Dataset
============================================================
'''
import rosalind.rosutil as ro, rosalind.rosalign as ra, numpy as np, time

def semi_global_alignment((x, y), debug=False):
    '''Optimal overlap alignment of the strings x,y. Returns the full DP matrix'''
    m, n = len(x), len(y)
    c = [[0 for _ in xrange(n + 1)] for _ in xrange(m + 1)]
    p = [[0 for _ in xrange(n + 1)] for _ in xrange(m + 1)]
    
    # Initial conditions on first row & column. c already set to 0 there
    for i in xrange(1, m + 1): p[i][0] = ra.T_GAP
    for j in xrange(1, n + 1): p[0][j] = ra.S_GAP
    # c[0, :] = [0 for _ in xrange(n + 1)] 
    # c[:, 0] = [0 for _ in xrange(m + 1)]
    
    # Dynamic programming
    if debug >= 2:
        print m, n
    if debug >= 1:
        start = time.time()
    for i, xi in enumerate(x, 1):
        if debug:
            if i % 100 == 0: print i, time.time() - start
        for j, yj in enumerate(y, 1):
            c1 = c[i - 1][j - 1] + (1 if xi == yj else -1)
            c2 = c[i - 1][j] - 1
            c3 = c[i][j - 1] - 1
            c_max = max(c1, c2, c3)
            if c_max == c1: p_max = ra.EQ
            elif c_max == c2: p_max = ra.T_GAP
            else: p_max = ra.S_GAP
            c[i][j] = c_max
            p[i][j] = p_max
    return c, p

def alignment_from_matrix((x, y), (i, j), c, p, gap_symbol='-'):
    '''Return the augmented-aligned strings of the original strings x and y
    from the DP matrix (result of global_alignment_matrix()) c. Start path back-tracking
    at element (i,j) in c.'''
    # print i, j
    # print x, y
    if j == len(y): s, t = x[i:], (len(x) - i) * gap_symbol  # End gap in y
    else: s, t = (len(y) - j) * gap_symbol, y[j:]  # End gap in x
    # print i, j, s, t
    while i > 0 or j > 0:
        ptr = p[i][j]
        #print i, j, ptr, s, t
        if ptr == ra.EQ: i, j, si, ti = i - 1, j - 1 , x[i - 1], y[j - 1]
        elif ptr == ra.T_GAP: i, si, ti = i - 1, x[i - 1], gap_symbol
        else: j, si, ti = j - 1, gap_symbol, y[j - 1]
        s, t = si + s, ti + t
    #print i, j, s, t
    return s, t

def smgb(f, debug=False):
    '''Main driver to solve this problem.'''
    x, y = ro.fafsa_values(f)  # [r.seq for r in SeqIO.parse('rosalind_smgb.dat', 'fasta')]
    
    c, p = semi_global_alignment((x, y), debug=debug)
    # row_max = (np.argmax(c[:, -1]), len(y))
    # col_max = (len(x), np.argmax(c[-1, :]))
    m, n = len(x), len(y)
    row_max = (np.argmax([c[i][n] for i in xrange(m + 1)]), n)
    col_max = (m, np.argmax(c[-1]))
    overall_max = row_max if c[row_max[0]][row_max[1]] > c[col_max[0]][col_max[1]] else col_max
    if debug >= 2:
        print np.array(c)
        print np.array(p)
        # print row_max, col_max
        print overall_max
    print c[overall_max[0]][overall_max[1]]
    print ro.join_list(alignment_from_matrix((x, y), overall_max, c, p), delimiter='\n')

if __name__ == '__main__':
    smgb('rosalind_smgb_sample.dat', debug=True)
    smgb('rosalind_smgb_sample2.dat')
    smgb('rosalind_smgb_sample3.dat', debug=True)
    smgb('rosalind_smgb.dat', debug=True)
