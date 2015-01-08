'''
============================================================
http://rosalind.info/problems/laff

A local alignment of two strings s and t is an alignment of
substrings r and u of s and t, respectively. Let opt(r,u)
denote the score of an optimal alignment of r and u with
respect to some predetermined alignment score.

Given: Two protein strings s and t in FASTA format (each
having length at most 1000 aa).

Return: A maximum alignment score along with substrings r
and u of s and t, respectively, which produce this maximum
alignment score (multiple solutions may exist, in which case
you may output any one). Use:

The PAM250 scoring matrix.
Linear gap penalty equal to 5.
============================================================
'''
import rosalind.rosutil as ro, rosalind.rosalign as ra, numpy as np, time, sys

'''Minus infinity = smallest possible (integer) cost. A little larger than min integer so that we don\'t
wrap around when subtracting gap penalties.'''
MINUS_INFINITY = -sys.maxint - 1 + 10000

'''Index of alignment path beginning.'''  
NONE = -1

def optimal_alignment_array_form(x, y, score, gap_init, gap_ext, debug=0, gap_symbol='-'):
    '''Optimal alignment that maximizes the alignment score based on the (symmetric) ScoringMatrix score
    and, initial gap penalty \'gap_init\' < 0, and a gap extension penalty \'gap_ext\' < 0.
    If align='local', performs local alignment, otherwise global.
    Integrated DP+backtracking, O(mn) time+storage, but may be faster (separate score,path arrays).'''
    RESTART = 0
    m, n = len(x), len(y)
    if debug >= 1:
        print m, n
        start = time.time()
    c = [[0 for _ in xrange(n + 1)] for _ in xrange(m + 1)]  # Max score of paths ending at (i,j)
    d = [[0 for _ in xrange(n + 1)] for _ in xrange(m + 1)]  # Max score of paths ending at (i,j), ending with a substitution
    e = [[0 for _ in xrange(n + 1)] for _ in xrange(m + 1)]  # Max score of paths ending at (i,j), ending with an ins/del
    p = [[0 for _ in xrange(n + 1)] for _ in xrange(m + 1)]
    
    #-----------------------------------
    # Initial condition, first row & col
    #-----------------------------------
    # Best: empty substring alignment (score=0)
    for j in xrange(n + 1):
        d[0][j] = MINUS_INFINITY
        e[0][j] = 0 
        p[0][j] = NONE
    # Best: empty substring alignment (score=0)
    for i in xrange(m + 1):
        d[i][0] = MINUS_INFINITY
        e[i][0] = 0 
        p[i][0] = NONE
    
    #-----------------------------------
    # Dynamic programming
    #-----------------------------------
    for i, xi in enumerate(x, 1):
        if debug:
            if i % 100 == 0: print i, time.time() - start
        for j, yj in enumerate(y, 1):
            i1, j1 = i - 1, j - 1
            # Possible types of paths to extend to (i,j)
            d[i][j] = d_max = c[i1][j1] + score(xi, yj)
            e1, e2, e3, e4 = \
            d[i1][j] + gap_init, e[i1][j] + gap_ext, \
            d[i][j1] + gap_init, e[i][j1] + gap_ext
            e[i][j] = e_max = max(e1, e2, e3, e4)
            c[i][j] = c_max = max(d_max, e_max, RESTART)  # Pick best path (greedy approach)
            # Reconstruct the previous element along the best path             
            if c_max == d_max: p_max = ra.EQ
            elif c_max == e_max: p_max = ra.T_GAP if e_max == e1 or e_max == e2 else ra.S_GAP 
            else: p_max = NONE
            # Save (i,j) state in matrix
            p[i][j] = p_max
        
    # Maximize score, back-track path
    i, j = divmod(np.argmax(c), n + 1)
    if debug >= 1: print 'Starting back-tracking at', (i, j)
    if debug >= 2:
        print np.array(c)
        print np.array(p)
    return c[i][j], alignment_array_form(x, y, c, p, (i, j), gap_symbol=gap_symbol)

def alignment_array_form(x, y, c, p, (i, j), gap_symbol='-'):
    '''Return the augmented-aligned strings of the original strings x and y
    from the DP matrix (result of global_alignment_matrix()) c.'''
    s, t, ptr = '', '', ra.EQ
    while ptr != NONE:
        ptr = p[i][j]
        # print i, j, ptr, s, t
        if ptr == ra.EQ: i, j, si, ti = i - 1, j - 1 , x[i - 1], y[j - 1]
        elif ptr == ra.T_GAP: i, si, ti = i - 1, x[i - 1], gap_symbol
        else: j, si, ti = j - 1, gap_symbol, y[j - 1]
        s, t = si + s, ti + t
    return s, t

def laff(f, debug=0):
    '''Main driver to solve the LOCA problem.'''
    x, y = ro.fafsa_values(f)
    d, (xx, yy) = optimal_alignment_array_form(x, y, ra.BLOSUM62, -11, -1, debug=debug, gap_symbol='-')
    if debug:
        print x
        print y 
        print ra.score_of(xx, yy, ra.BLOSUM62, -11, -1)  # , debug=True)
    return ro.join_list((d, xx, yy), delimiter='\n')

from itertools import product

def laff_yesimon(f):
    score = ra.BLOSUM62
    s, t = ro.fafsa_values(f)
    sl, tl = len(s), len(t)
    T = np.zeros((sl + 1, tl + 1), dtype=np.character)
    V = np.zeros((sl + 1, tl + 1))
    F = np.zeros((sl + 1, tl + 1))
    G = np.zeros((sl + 1, tl + 1))
    for i, j in product(xrange(1, sl + 1), xrange(1, tl + 1)):
        cost = score(s[i - 1], t[j - 1])
        F[i, j] = V[i - 1, j - 1] + cost
        G[i, j] = max(F[i - 1, j] - 12, G[i - 1, j] - 1, F[i, j - 1] - 12, G[i, j - 1] - 1)
        V[i, j] = v = max(F[i, j], G[i, j], 0)
        if v == F[i, j]: T[i, j] = 'D'
        elif v == G[i, j]:
            if v == F[i - 1, j] - 12 or G[i - 1, j] - 1: T[i, j] = 'L'
            else: T[i, j] = 'U'
        elif v == 0: T[i, j] = ''
    i, j = np.unravel_index(np.argmax(V), V.shape)
    print(int(V[i, j]))
    sa = ''
    ta = ''
    while T[i, j]:
        direction = T[i, j]
        if direction == 'D':
            sa += s[i - 1]
            ta += t[j - 1]
            i, j = i - 1, j - 1
        elif direction == 'L':
            ta += t[j - 1]
            i = i - 1
        elif direction == 'U':
            sa += s[i - 1]
            j = j - 1
    print(''.join(reversed(sa)))
    print(''.join(reversed(ta)))
    
if __name__ == "__main__":
    # print ra.optimal_alignment('PLS', 'MN', ra.BLOSUM62, -11, -1, debug=True)
    # print ra.score_of('LS', 'MN', ra.BLOSUM62, -11, -1, debug=True)
#     print ra.score_of('TLY', 'NLY', ra.BLOSUM62, -11, -1, debug=True)
# 
#     print ra.optimal_alignment('LEAS', 'MEAN', ra.BLOSUM62, -11, -1, debug=True)
    # print laff('rosalind_laff_sample.dat')
#  print laff('rosalind_laff.dat', debug=1)

#     cProfile.run('a()', 'a')
#     p = pstats.Stats('a').strip_dirs()
#     p.sort_stats('cumulative').print_stats(50)
    print laff('rosalind_laff_sample4.dat', debug=2)
    print laff_yesimon('rosalind_laff_sample4.dat')

#     print laff('rosalind_laff_sample5.dat', debug=1)
#     print ra.score_of('SAVAKC------HQR', 'SAKQKCARIENSHQR', ra.BLOSUM62, -11, -1, debug=True)
    
    print laff('rosalind_laff_sample3.dat', debug=2)
    print laff_yesimon('rosalind_laff_sample3.dat')
