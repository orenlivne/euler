'''
============================================================
My Rosalind alignment library.
An alignment of two strings s and t is defined by two strings s' and t' satisfying the following three conditions: 1. s' and t' must be formed from adding gap symbols "-" to each of s and t, respectively; as a result, s and t will form subsequences of s' and t'. 2. s' and t' must have the same length. 3. Two gap symbols may not be aligned; that is, if s'[j] is a gap symbol, then t'[j] cannot be a gap symbol, and vice-versa.

We say that s' and t' augment s and t. Writing s' directly over t' so that symbols are aligned provides us with a scenario for transforming s into t. Mismatched symbols from s and t correspond to symbol substitutions; a gap symbol s'[j] aligned with a non-gap symbol t'[j] implies the insertion of this symbol into t; a gap symbol t'[j] aligned with a non-gap symbol s'[j] implies the deletion of this symbol from s.

Thus, an alignment represents a transformation of s into t via edit operations. We define the corresponding edit alignment score of s' and t' as dH(s',t') (Hamming distance is used because the gap symbol has been introduced for insertions and deletions). It follows that dE(s,t)=mins',t'dH(s',t'), where the minimum is taken over all alignments of s and t. We call such a minimum score alignment an optimal alignment (with respect to edit distance).
============================================================
'''
import sys, numpy as np, rosutil as ro, time

'''Alignment codes'''
EQ, T_GAP, S_GAP, BEGIN = range(4)

'''Minus infinity = smallest possible (integer) cost. A little larger than min integer so that we don\'t
wrap around when subtracting gap penalties.'''
MINUS_INFINITY = -sys.maxint - 1 + 10000
INFINITY = sys.maxint - 10000

'''Index of alignment path beginning.'''  
NONE = -1

'''Useful initial conditions'''
empty = lambda n: [[0, ()] for _ in xrange(n + 1)]
undefined = lambda n: [[MINUS_INFINITY, ()] for _ in xrange(n + 1)]

def score_of(xx, yy, score, gap_init, gap_ext, gap_symbol='-', debug=False):
    '''Return the score of an alignment of x, y encoded in xx,yy.'''    
    s_total = 0
    for i, (x, y) in enumerate(zip(xx, yy)):
        if x != gap_symbol and y != gap_symbol: s = score(x, y)
        elif x == gap_symbol: s = gap_ext if i > 0 and xx[i - 1] == gap_symbol else gap_init  
        else: s = gap_ext if i > 0 and yy[i - 1] == gap_symbol else gap_init
        if debug: print x, y, s
        s_total += s
    return s_total

def copy_list(a, b):
    '''Deep-copy the list a into b in-place.'''
    for i in xrange(len(a)): b[i][:] = a[i][:]
    
def optimal_alignment(x, y, score, gap_init, gap_ext, debug=0, align='global', gap_symbol='-'):
    '''Optimal alignment that maximizes the alignment score based on the (symmetric) ScoringMatrix score
    and, initial gap penalty \'gap_init\' < 0, and a gap extension penalty \'gap_ext\' < 0.
    If align='global' (default), performs global alignment.
    If align='local', performs local alignment.
    If align='fit', returns fitting alignment.
    Integrated DP+backtracking, O(mn) time, O(max(m,n)) storage.'''
    # If local alignment, allow restarting the optimal subsequence during DP;
    # otherwise, consider only suffixes.
    # RESTART is a restart state c[j] is compared with at each relaxation step.
    local = align == 'local'
    RESTART = [0 if local else MINUS_INFINITY, (BEGIN,)]
    m, n = len(x), len(y)
    # Use leaner storage, unless we are performer fitting alignment. In this case it'd be possible, too,
    # but it's easier to fix the max over the last column in both cases m < n, m >= n. 
    if align != 'fit' and m < n:
        max_score, (yy, xx) = optimal_alignment(y, x, score, gap_init, gap_ext, debug=debug, align=align, gap_symbol=gap_symbol)
        return max_score, (xx, yy)
    
    # In state arrays, we keep tuples = (score, path) for alignment reconstruct
    # Initial condition (first row)
    d, d_old, e_old, c, c_old = undefined(n), empty(n), empty(n), empty(n), empty(n)
    e = [[0, ()]  for _ in xrange(n + 1)] if local \
    else [[0 if j == 0 else (gap_init + (j - 1) * gap_ext), tuple([S_GAP] * j)]  for j in xrange(n + 1)]
    copy_list(e, c)
    if debug >= 1:
        print m, n
        start = time.time()
    if debug >= 2: print np.array([z[0] for z in c])
    if align == 'fit':
        c_max = (tuple(c[0]), (0, n))
    elif local:
        c_max = (tuple(max(c)), (0, np.argmax([z[0] for z in c])))
    
    for i, xi in enumerate(x, 1):
        if debug >= 1:
            if i % 100 == 0: print i, time.time() - start
        copy_list(d, d_old); copy_list(e, e_old); copy_list(c, c_old)  # Advance to next row
        # Initial condition (first column)
        d[0] = [MINUS_INFINITY, ()]
        e[0] = [0, ()] if local or align == 'fit' else [gap_init + (i - 1) * gap_ext, c_old[0][1] + (T_GAP,)]
        c[0][:] = e[0][:]
        for j, yj in enumerate(y, 1):
            # Possible types of paths to extend to (i,j)
            d[j][0] = c_old[j - 1][0] + score(xi, yj)
            e1, e2, e3, e4 = d_old[j][0] + gap_init, e_old[j][0] + gap_ext, \
            d[j - 1][0] + gap_init, e[j - 1][0] + gap_ext
            e_max = max(e1, e2, e3, e4)
            e[j][0] = e_max
            
            d[j][1] = c_old[j - 1][1] + (EQ,)
            if e_max == e1: e[j][1] = d_old[j][1] + (T_GAP,)
            elif e_max == e2: e[j][1] = e_old[j][1] + (T_GAP,)
            elif e_max == e3: e[j][1] = d[j - 1][1] + (S_GAP,)
            else: e[j][1] = e[j - 1][1] + (S_GAP,)
            
            # Pick best path (greedy approach)
            #c[j] = max(d[j], e[j], [c0[j][0], (BEGIN,)] if align == 'fit' else RESTART)
            c[j] = max(d[j], e[j], RESTART)
        if debug >= 2:
            print np.array([z[0] for z in c])            
        if align == 'fit':
            # Maximize over last column
            if c[-1][0] > c_max[0][0]: c_max = (tuple(c[-1]), (i, n))
        elif local:
            # Maximize over entire matrix
            ci_max = max(c)
            if ci_max[0] > c_max[0][0]: c_max = (tuple(ci_max), (i, np.argmax([z[0] for z in c])))
    # If global alignment, solution is at the end of the string. Otherwise it is the max over all
    # c[j] over all j over all i
    if local or align == 'fit': return c_max[0][0], alignment(x, y, (c_max[1][0] - 1, c_max[1][1] - 1), c_max[0][1], gap_symbol=gap_symbol)
    else: return c[-1][0], alignment(x, y, (m - 1, n - 1), c[-1][1], gap_symbol=gap_symbol)

def alignment(x, y, (i, j), a, gap_symbol='-'):
    '''Return the alignment strings from the original strings x and y and the alignment coding vector a.'''
    s, t = '', ''
    for ai in reversed(a):
        if ai == EQ: si, ti, i, j = x[i], y[j], i - 1, j - 1 
        elif ai == T_GAP: si, ti, i = x[i], gap_symbol, i - 1
        elif ai == S_GAP: si, ti, j = gap_symbol, y[j], j - 1
        elif ai == BEGIN: break
        else: raise ValueError('Unrecognized alignment code %d' % (ai,))
        s, t = si + s, ti + t
    return s, t

def global_alignment_matrix((x, y), score, gap_score= -1, debug=False):
    '''Global alignment of two strings. Returns the full DP matrix of (score,path) elements.
    gap init = gap extend = gap_score here. Entries contain score and back-tracking information.'''
    m, n = len(x), len(y)
    c = np.zeros((m + 1, n + 1), dtype=object)
    # Initial conditions
    c[:, 0] = zip(gap_score * np.arange(m + 1), [None] + [(i - 1, 0) for i in xrange(1, m + 1)])
    c[0, :] = zip(gap_score * np.arange(n + 1), [None] + [(j - 1, 0) for j in xrange(1, n + 1)])
    # Dynamic programming
    for i, xi in enumerate(x, 1):
        for j, yj in enumerate(y, 1):
            c[i, j] = max((c[i - 1, j - 1][0] + score(xi, yj), (i - 1, j - 1)),
                          (c[i - 1, j][0] + gap_score, (i - 1, j)),
                          (c[i, j - 1][0] + gap_score, (i, j - 1)))
    return c

def global_alignment_score_matrix((x, y), score, gap_score= -1, debug=False):
    '''Global alignment of two strings. Returns the full DP matrix of (score,path) elements.
    gap init = gap extend = gap_score here. Entries contain optimal scores for prefix alignments.'''
    m, n = len(x), len(y)
    c = np.zeros((m + 1, n + 1), dtype=int)
    # Initial conditions
    c[:, 0] = gap_score * np.arange(m + 1)
    c[0, :] = gap_score * np.arange(n + 1)
    # Dynamic programming
    for i, xi in enumerate(x, 1):
        for j, yj in enumerate(y, 1):
            c[i, j] = max(c[i - 1, j - 1] + score(xi, yj), c[i - 1, j] + gap_score, c[i, j - 1] + gap_score)
    return c

def local_alignment_score_matrix((x, y), score, gap_penalty= -1, debug=False):
    '''Local alignment of two strings. Returns the full DP matrix of (score,path) elements.
    gap init = gap extend = gap_penalty here. Entries contain minimum scores for prefix alignments.'''
    m, n = len(x), len(y)
    c = np.zeros((m + 1, n + 1), dtype=int)
    # Initial conditions
    c[:, 0] = gap_penalty * np.arange(m + 1)
    c[0, :] = gap_penalty * np.arange(n + 1)
    # Dynamic programming
    for i, xi in enumerate(x, 1):
        for j, yj in enumerate(y, 1):
            c[i, j] = min(c[i - 1, j - 1] + score(xi, yj), c[i - 1, j] + gap_penalty, c[i, j - 1] + gap_penalty, 0)
    return c

def alignment_from_matrix((x, y), c, gap_symbol='-'):
    '''Return the augmented-aligned strings of the original strings x and y
    from the DP matrix (result of global_alignment_matrix()) c.'''
    s, t, i, j = '', '', len(x), len(y)
    while i > 0 or j > 0:
        ip, jp = c[i, j][1]
        s, t = (gap_symbol if ip == i else x[i - 1]) + s, (gap_symbol if jp == j else y[j - 1]) + t
        i, j = ip, jp
    return s, t

def optimal_alignment_matrix_form((x, y), score, gap_init, gap_ext, debug=0, align='global', gap_symbol='-'):
    '''Optimal alignment that maximizes the alignment score based on the (symmetric) ScoringMatrix score
    and, initial gap penalty \'gap_init\' < 0, and a gap extension penalty \'gap_ext\' < 0.
    If align='local', performs local alignment, otherwise global.
    Integrated DP+backtracking, O(mn) time+storage, but may be faster (separate score,path arrays).'''
    local = (align == 'local')
    RESTART = 0 if local else MINUS_INFINITY
    m, n = len(x), len(y)
    if debug >= 1:
        print m, n
        start = time.time()
    c = np.zeros((m + 1, n + 1), dtype=int)  # Max score of paths ending at (i,j)
    d = np.zeros((m + 1, n + 1), dtype=int)  # Max score of paths ending at (i,j), ending with a substitution
    e = np.zeros((m + 1, n + 1), dtype=int)  # Max score of paths ending at (i,j), ending with an ins/del
    I = np.zeros((m + 1, n + 1), dtype=int)
    J = np.zeros((m + 1, n + 1), dtype=int)
    
    #-----------------------------------
    # Initial condition, first row
    #-----------------------------------
    d[0, :] = [MINUS_INFINITY for _ in xrange(n + 1)] 
    if local:
        # Best: empty substring alignment (score=0)
        e[0, :] = [0 for _ in xrange(n + 1)] 
        I[0, :] = [NONE for _ in xrange(n + 1)]
        J[0, :] = [NONE for _ in xrange(n + 1)]
    else:
        # Best: aligning y against gaps
        e[0, :] = [0 if j == 0 else (gap_init + (j - 1) * gap_ext) for j in xrange(n + 1)]
        I[0, :] = [0 for _ in xrange(n + 1)]
        J[0, :] = [NONE] + np.arange(n)
    c[0, :] = e[0, :]
    
    #-----------------------------------
    # Initial condition, first column
    #-----------------------------------
    d[:, 0] = [MINUS_INFINITY for _ in xrange(m + 1)]
    if local:
        # Best: empty substring alignment (score=0)
        e[:, 0] = [0 for _ in xrange(m + 1)] 
        I[:, 0] = [NONE for _ in xrange(m + 1)]
        J[:, 0] = [NONE for _ in xrange(m + 1)]
    else:
        # Best: aligning x against gaps
        e[:, 0] = [0 if j == 0 else (gap_init + (i - 1) * gap_ext) for i in xrange(m + 1)]
        I[:, 0] = [NONE] + np.arange(m)
        J[:, 0] = [0 for _ in xrange(m + 1)]
    c[:, 0] = e[:, 0]
    
    #-----------------------------------
    # Dynamic programming
    #-----------------------------------
    for i, xi in enumerate(x, 1):
        if debug:
            if i % 100 == 0: print i, time.time() - start
        for j, yj in enumerate(y, 1):
            # Possible types of paths to extend to (i,j)
            d_max = c[i - 1, j - 1] + score(xi, yj)
            e1, e2, e3, e4 = d[i - 1, j] + gap_init, e[i - 1, j] + gap_ext, d[i, j - 1] + gap_init, e[i, j - 1] + gap_ext
            e_max = max(e1, e2, e3, e4)
            c_max = max(d_max, e_max, RESTART)  # Pick best path (greedy approach)
            # Reconstruct the previous element along the best path             
            if c_max == d_max: ip = i - 1, j - 1
            elif c_max == e_max: ip = (i - 1, j) if e_max == e1 or e_max == e2 else (i, j - 1) 
            else: ip = NONE, NONE
            # Save (i,j) state in matrix
            d[i, j], e[i, j], c[i, j], (I[i, j], J[i, j]) = d_max, e_max, c_max, ip
        
    # Maximize score, back-track path
    i, j = divmod(np.argmax(c), n + 1) if local else (m, n)
    if debug >= 1: print 'Starting back-tracking at', (i, j)
    if debug >= 2:
        print c
        print I
        print J
    return c[i][j], alignment_matrix_form((x, y), c, I, J, (i, j), gap_symbol=gap_symbol)

def alignment_matrix_form((x, y), c, I, J, (i, j), gap_symbol='-'):
    '''Return the augmented-aligned strings of the original strings x and y
    from the DP matrix (result of global_alignment_matrix()) c.'''
    s, t = '', ''
    while True:
        ip, jp = I[i, j], J[i, j]
        if ip == NONE or jp == NONE: break
        s, t = (gap_symbol if ip == i else x[i - 1]) + s, (gap_symbol if jp == j else y[j - 1]) + t
        i, j = ip, jp
    return s, t

#---------------------------------------
# Scoring
#---------------------------------------
class ScoringMatrix(object):
    '''An alignment scoring matrix object. Holds a list of symbols and their scoring matrix,
    such as the BLOSUM62 matrix.'''
    
    def __init__(self, file_name):
        '''Read from file file_name.'''
        self._symbol = dict((v, k) for k, v in enumerate(ro.iterlines(file_name).next().split()))
        self._score = np.loadtxt(file_name, skiprows=1, usecols=range(1, len(self._symbol) + 1), dtype=int)
    
    def __call__(self, i, j):
        '''Return the score of changing i to j.'''
        return self._score[self._symbol[i]][self._symbol[j]]
    
'''The BLOSUM62 alignment scoring matrix.'''
BLOSUM62 = ScoringMatrix(ro.ROSALIND_HOME + '/dat/blosum62.dat')
PAM250 = ScoringMatrix(ro.ROSALIND_HOME + '/dat/pam250.dat')

class FixedCost(object):
    '''Scoring function of a fixed-cost (edit distance) model.'''
    def __init__(self, p, d):
        '''Read from file file_name. p>0: cost of matching symbols. d: non-matching penalty (<0) '''
        self._p, self._d = p, d
    
    def __call__(self, i, j):
        '''Return the score of changing i to j.'''
        return self._p if i == j else self._d
