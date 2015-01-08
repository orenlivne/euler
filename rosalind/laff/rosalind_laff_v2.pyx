# encoding: utf-8
# filename: laff.py
'''
============================================================
http://rosalind.info/problems/laff

A local alignment of two strings s and t is an alignment of substrings r and u of s and t, respectively. Let opt(r,u) denote the score of an optimal alignment of r and u with respect to some predetermined alignment score.

Given: Two protein strings s and t in FASTA format (each having length at most 1000 aa).

Return: A maximum alignment score along with substrings r and u of s and t, respectively, which produce this maximum alignment score (multiple solutions may exist, in which case you may output any one). Use:

The PAM250 scoring matrix.
Linear gap penalty equal to 5.
============================================================
'''
import rosalind.rosutil as ro, rosalind.rosalign as ra, numpy as np, time, sys
import pstats, cProfile
#from cython.view cimport array as cvarray

'''Minus infinity = smallest possible (integer) cost. A little larger than min integer so that we don\'t
wrap around when subtracting gap penalties.'''
cdef int MINUS_INFINITY = -sys.maxint - 1 + 10000

'''Index of alignment path beginning.'''  
cdef int NONE = -1

'''A complex type is easier to handle as a constant in Cython instead of passing it to optimal_alignment_array_form().'''
SCORE = ra.BLOSUM62

def optimal_alignment_array_form(char * x, char * y, int gap_init, int gap_ext, int debug, char * gap_symbol):
    '''Optimal alignment that maximizes the alignment score based on the (symmetric) ScoringMatrix score
    and, initial gap penalty \'gap_init\' < 0, and a gap extension penalty \'gap_ext\' < 0.
    If local=True, performs local alignment, otherwise global.
    Integrated DP+backtracking, O(mn) time+storage, but may be faster (separate score,path arrays).'''
    cdef int RESTART = 0  # if local else MINUS_INFINITY
    cdef int m = len(x)
    cdef int n = len(y)
    cdef int i
    cdef int j
    if debug >= 1:
        print m, n
        start = time.time()
#     carr = cvarray(shape=(m + 1, n + 1), itemsize=sizeof(int), format="i")
#     cdef int [:, :] c = carr
#     darr = cvarray(shape=(m + 1, n + 1), itemsize=sizeof(int), format="i")
#     cdef int [:, :] d = darr
#     earr = cvarray(shape=(m + 1, n + 1), itemsize=sizeof(int), format="i")
#     cdef int [:, :] e = earr
#     Iarr = cvarray(shape=(m + 1, n + 1), itemsize=sizeof(int), format="i")
#     cdef int [:, :] I = Iarr
#     Jarr = cvarray(shape=(m + 1, n + 1), itemsize=sizeof(int), format="i")
#     cdef int [:, :] J = Jarr
    c = [[0 for _ in xrange(n + 1)] for _ in xrange(m + 1)]  # Max score of paths ending at (i,j)
    d = [[0 for _ in xrange(n + 1)] for _ in xrange(m + 1)]  # Max score of paths ending at (i,j), ending with a sub\stitution
    e = [[0 for _ in xrange(n + 1)] for _ in xrange(m + 1)]  # Max score of paths ending at (i,j), ending with an in\s/del
    I = [[0 for _ in xrange(n + 1)] for _ in xrange(m + 1)]
    J = [[0 for _ in xrange(n + 1)] for _ in xrange(m + 1)]
    
    #-----------------------------------
    # Initial condition, first row
    #-----------------------------------
    for j in xrange(n + 1): d[0, j] = MINUS_INFINITY 
    # Best: empty substring alignment (score=0)
    for j in xrange(n + 1):
        e[0, j] = 0 
        I[0, j] = NONE
        J[0, j] = NONE

    #-----------------------------------
    # Initial condition, first column
    #-----------------------------------
    for i in xrange(m + 1): d[i, 0] = MINUS_INFINITY
    # Best: empty substring alignment (score=0)
    for i in xrange(m + 1):
        e[i, 0] = 0 
        I[i, 0] = NONE
        J[i, 0] = NONE
    
    #-----------------------------------
    # Dynamic programming
    #-----------------------------------
    for i, xi in enumerate(x, 1):
        if debug:
            if i % 100 == 0: print i, time.time() - start
        for j, yj in enumerate(y, 1):
            i1, j1 = i - 1, j - 1
            # Possible types of paths to extend to (i,j)
            d_max = c[i1, j1] + SCORE(xi, yj)
            e1, e2, e3, e4 = d[i1, j] + gap_init, e[i1, j] + gap_ext, d[i, j1] + gap_init, e[i, j1] + gap_ext
            e_max = max(e1, e2, e3, e4)
            c_max = max(d_max, e_max, RESTART)  # Pick best path (greedy approach)
            # Reconstruct the previous element along the best path             
            if c_max == d_max: ip = i1, j1
            elif c_max == e_max: ip = (i1, j) if e_max == e1 or e_max == e2 else (i, j1) 
            else: ip = NONE, NONE
            # Save (i,j) state in matrix
            d[i, j], e[i, j], c[i, j], (I[i, j], J[i, j]) = d_max, e_max, c_max, ip
        
    # Maximize score, back-track path
    i, j = divmod(np.argmax(c), n + 1)
    if debug >= 1: print 'Starting back-tracking at', (i, j)
    if debug >= 2:
        print c
        print I
        print J
    return c[i, j], alignment_array_form(x, y, c, I, J, i, j, gap_symbol)

def alignment_array_form(x, y, I, J, i, j, gap_symbol=''):
    '''Return the augmented-aligned strings of the original strings x and y
    from the DP matrix (result of global_alignment_matrix()) c.'''
    s, t = ''
    while True:
        ip, jp = I[i, j], J[i, j]
        if ip == NONE or jp == NONE: break
        if ip == i: 
            tmp = gap_symbol + s
            s = tmp
        else: s = x[i - 1] + s
        if jp == j:
            tmp = gap_symbol + t
            t = tmp
        else: t = y[j - 1] + t
        i, j = ip, jp
    return s, t

def laff(f, debug=0, out=sys.stdout):
    '''Main driver to solve the LOCA problem.'''
    x, y = ro.fafsa_values(f)
    d, (xx, yy) = optimal_alignment_array_form(x, y, -11, -1, debug, '')
    out.write(ro.join_list((d, xx, yy), delimiter='\n') + '\n')

# def a():
#     print laff('rosalind_laff_sample2.dat', debug=1)

if __name__ == "__main__":
    laff('rosalind_laff_sample.dat', debug=1)
    # print ra.optimal_alignment('PLS', 'MN', ra.BLOSUM62, -11, -1, local=True, debug=True)
    # print ra.score_of('LS', 'MN', ra.BLOSUM62, -11, -1, debug=True)
#     print ra.score_of('TLY', 'NLY', ra.BLOSUM62, -11, -1, debug=True)
# 
#     print ra.optimal_alignment('LEAS', 'MEAN', ra.BLOSUM62, -11, -1, local=True, debug=True)
    # print laff('rosalind_laff_sample.dat')
#  print laff('rosalind_laff.dat', debug=1)

#     cProfile.run('a()', 'a')
#     p = pstats.Stats('a').strip_dirs()
#     p.sort_stats('cumulative').print_stats(50)
