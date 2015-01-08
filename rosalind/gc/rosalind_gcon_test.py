'''
============================================================
http://rosalind.info/problems/gcon (gap = a)
http://rosalind.info/problems/gaff (gap = a + b*(L-1))

In a constant gap_ext penalty, every gap_ext receives some predetermaxed constant penalty, regardless of its length. Thus, the insertion or deletion of 1000 contiguous symbols is penalized equally to that of a single symbol.

Given: Two protein strings s and t in FASTA format (each of length at most 1000 aa).

Return: The maximum alignment score between s and t. Use:

The BLOSUM62 scoring matrix. Constant gap_ext penalty equal to 5.
============================================================
'''
import rosalind.rosutil as ro, sys, rosalign as ra

'''Alignment codes'''
EQ, T_GAP, S_GAP = range(3)

def alignment(x, y, a, gap_symbol='-'):
    '''Return the alignment strings from the original strings x and y and the alignment coding vector a.'''
    s, t, ix, iy = '', '', iter(x), iter(y)
    for ai in a:
        if ai == EQ:
            s += ix.next()
            t += iy.next()
        elif ai == T_GAP:
            s += ix.next()
            t += gap_symbol
        else:
            s += gap_symbol
            t += iy.next()
    return s, t

def optimal_alignment_separate_arrays(x, y, score, gap_init, gap_ext, debug=False):
    '''Optimal alignment that maximizes the alignment score based on the (symmetric) ScoringMatrix score
    and a gap_ext extension penalty \'gap_ext\'.
    
    Integrated DP+backtracking, O(mn) time, O(max(m,n)) storage.'''
    BIG_NEGATIVE = -sys.maxint - 1
    m, n = len(x), len(y)
    if m < n:
        d, (yy, xx) = optimal_alignment_separate_arrays(y, x, score, gap_init, gap_ext, debug=debug)
        return d, (xx, yy)
    # Initial condition (first row)
    d, d_old = [BIG_NEGATIVE] * (n + 1), [0] * (n + 1)
    e, e_old = [BIG_NEGATIVE] * (n + 1), [0] * (n + 1)
    f, f_old = [0] * (n + 1), [0] * (n + 1)
    for j in xrange(1, n + 1): f[j] = gap_init + (j - 1) * gap_ext
    c, c_old = [0] * (n + 1), [0] * (n + 1)
    c[:] = f[:]
    
    ad, ad_old = [() for _ in xrange(n + 1)], [()] * (n + 1)
    ae, ae_old = [() for _ in xrange(n + 1)], [()] * (n + 1)
    af, af_old = [tuple([S_GAP] * j) for j in xrange(n + 1)], [()] * (n + 1)
    a, a_old = [() for i in xrange(n + 1)], [()] * (n + 1)
    a[:] = af[:]
    
    # print zip(c, a)
    for i, xi in enumerate(x, 1):
        d_old[:] = d[:]; e_old[:] = e[:]; f_old[:] = f[:]
        ad_old[:] = ad[:]; ae_old[:] = ae[:]; af_old[:] = af[:]
        c_old[:] = c[:]; a_old[:] = a[:]
        # Initial condition (first column)
        d[0] = BIG_NEGATIVE; e[0] = gap_init + (i - 1) * gap_ext; f[0] = BIG_NEGATIVE
        ad[0] = None; ae[0] = a_old[0] + (T_GAP,); af[0] = None
        c[0] = e[0]; a[0] = ae[0]
        for j, yj in enumerate(y, 1):
            # Possible types of paths that extend to (i,j)
            d[j] = c_old[j - 1] + score(xi, yj)
            e[j] = max(c_old[j] + gap_init, e_old[j] + gap_ext) 
            f[j] = max(c[j - 1] + gap_init, f[j - 1] + gap_ext)

            ad[j] = a_old[j - 1] + (EQ,)
            ae[j] = (a_old[j] if e[j] == c_old[j] + gap_init else ae_old[j]) + (T_GAP,)
            af[j] = (a[j - 1] if f[j] == c[j - 1] + gap_init else af[j - 1]) + (S_GAP,)

            # Pick best path (greedy approach)
            # Keep track of moves in the a array to reconstuct the alignment
            c_max = max(d[j], e[j], f[j])
            if c_max == d[j]: a_max = ad[j]
            elif c_max == e[j]: a_max = ae[j]
            else: a_max = af[j]
            c[j], a[j] = c_max, a_max
            # print i, j, c[j], d[j], e[j], f[j], '--', (c_old[j] + gap_init, e_old[j] + gap_ext), (c_old[j], gap_init, e_old[j], gap_ext)
        # print zip(c, a)
    # print 'path', a[-1]
    return c[-1], alignment(x, y, a[-1])

def copy_list(a, b):
    '''Deep-copy the list a into b in-place.'''
    for i in xrange(len(a)): b[i][:] = a[i][:]
    
def optimal_alignment_tuple(x, y, score, gap_init, gap_ext, debug=False):
    '''Optimal alignment that maximizes the alignment score based on the (symmetric) ScoringMatrix score
    and a gap_ext extension penalty \'gap_ext\'.
    
    Integrated DP+backtracking, O(mn) time, O(max(m,n)) storage.'''
    BIG_NEGATIVE = -sys.maxint - 1
    m, n = len(x), len(y)
    if m < n:
        d, (yy, xx) = optimal_alignment_separate_arrays(y, x, score, gap_init, gap_ext, debug=debug)
        return d, (xx, yy)
    # In state arrays, we keep tuples = (score, path) to keep track of moves and reconstruct
    # the alignment Initial condition (first row)

    # Initial condition (first row)
    empty = lambda n: [[0, ()] for _ in xrange(n + 1)]
    undefined = lambda n: [[BIG_NEGATIVE, ()] for _ in xrange(n + 1)]
    d, d_old = undefined(n), empty(n)
    e, e_old = undefined(n), empty(n)
    f, f_old = [[0 if j == 0 else (gap_init + (j - 1) * gap_ext), tuple([S_GAP] * j)] 
                for j in xrange(n + 1)], empty(n)
    c, c_old = empty(n), empty(n)
    copy_list(f, c)
    # print c
    for i, xi in enumerate(x, 1):
        # Advance to next row
        copy_list(d, d_old)
        copy_list(e, e_old)
        copy_list(f, f_old)
        copy_list(c, c_old)
        # Initial condition (first column)
        d[0] = [BIG_NEGATIVE, ()]
        e[0] = [gap_init + (i - 1) * gap_ext, c_old[0][1] + (T_GAP,)]
        f[0] = [BIG_NEGATIVE, None]
        c[0][:] = e[0][:]
        for j, yj in enumerate(y, 1):
            # Possible types of paths that extend to (i,j)
            d[j][0] = c_old[j - 1][0] + score(xi, yj)
            e[j][0] = max(c_old[j][0] + gap_init, e_old[j][0] + gap_ext) 
            f[j][0] = max(c[j - 1][0] + gap_init, f[j - 1][0] + gap_ext)

            d[j][1] = c_old[j - 1][1] + (EQ,)
            e[j][1] = (c_old[j][1] if e[j][0] == c_old[j][0] + gap_init else e_old[j][1]) + (T_GAP,)
            f[j][1] = (c[j - 1][1] if f[j][0] == c[j - 1][0] + gap_init else f[j - 1][1]) + (S_GAP,)
            
            # Pick best path (greedy approach)
            # Keep track of moves in the a array to reconstuct the alignment
            c[j] = max(d[j], e[j], f[j])
            # print i, j, c[j], d[j], e[j], f[j], '--', (c_old[j][0] + gap_init, e_old[j][0] + gap_ext), (c_old[j][0], gap_init, e_old[j][0], gap_ext)
        # print c
    # print 'path', a[-1]
    # print c[-1]
    return c[-1][0], alignment(x, y, c[-1][1])

def optimal_alignment_tuple_v1(x, y, score, gap_init, gap_ext, debug=False):
    '''Using tuples instead of separate d,e,f,c, ad,ae,af,ac arrays. Currently broken.'''
    BIG_NEGATIVE = -sys.maxint - 1
    m, n = len(x), len(y)
    if m < n:
        d, (yy, xx) = optimal_alignment_tuple(y, x, score, gap_init, gap_ext, debug=debug)
        return d, (xx, yy)
    # Tuple = (score, path) to keep track of moves and reconstruct the alignment
    # Initial condition (first row)
    d, d_old = [[BIG_NEGATIVE, ()]] * (n + 1), [None] * (n + 1)
    e, e_old = [[BIG_NEGATIVE, ()]] * (n + 1), [None] * (n + 1)
    f, f_old = [[0, tuple([S_GAP] * j)] for j in xrange(n + 1)], [None] * (n + 1)
    c, c_old = [None] * (n + 1), [None] * (n + 1)
    for j in xrange(1, n + 1): f[j][0] = gap_init + (j - 1) * gap_ext
    c[:] = f[:]
    print c
    for i, xi in enumerate(x, 1):
        d_old[:] = d[:]; e_old[:] = e[:]; f_old[:] = f[:]; c_old[:] = c[:]
        # Initial condition (first column)
        d[0] = f[0] = [BIG_NEGATIVE, None]
        e[0] = c[0] = [gap_init + (i - 1) * gap_ext, c_old[0][1] + (T_GAP,)]
        for j, yj in enumerate(y, 1):
            # Possible types of paths that extend to (i,j)
            d[j][0] = c_old[j - 1][0] + score(xi, yj)
            e[j][0] = max(c_old[j][0] + gap_init, e_old[j][0] + gap_ext)
            f[j][0] = max(c[j - 1][0] + gap_init, f[j - 1][0] + gap_ext)

            d[j][1] = c_old[j - 1][1] + (EQ,)
            e[j][1] = (c_old[j][1] if e[j][0] == c_old[j][0] + gap_init else e[j][1]) + (T_GAP,)
            f[j][1] = (c[j - 1][1] if f[j][0] == c[j - 1][0] + gap_init else f[j - 1][1]) + (S_GAP,)

            # Pick best path (greedy approach)
            c[j] = max(map(tuple, (d[j], e[j], f[j])))
            # print i, j, c[j], d[j], e[j], f[j], '--', (c_old[j][0] , gap_init, e_old[j][0], gap_ext)
            pass
        
        print c
    print c[-1]
    return c[-1][0], alignment(x, y, c[-1][1])

def gcon(f, debug=False, optimal_alignment=optimal_alignment_separate_arrays):
    '''Main driver to solve the GCON problem.'''
    x, y = ro.fafsa_values(f)
    d, (xx, yy) = optimal_alignment(x, y, ra.BLOSUM62, -5, 0, debug=debug)
    print xx
    print yy
    return d

def gaff(f, score=ra.BLOSUM62, gap_init= -11, gap_ext= -1, debug=False, optimal_alignment=optimal_alignment_separate_arrays):
    '''Main driver to solve the GAFF problem.'''
    x, y = ro.fafsa_values(f)
    d, (xx, yy) = optimal_alignment(x, y, score, gap_init, gap_ext, debug=debug)
    # d, (xx, yy) = optimal_alignment(x, y, ra.BLOSUM62, -12, -1, debug=debug)
    print x
    print y
    print ra.score_of(xx, yy, score, gap_init, gap_ext)
    print
    print d
    print xx
    print yy
    return d

if __name__ == "__main__":
    # test_gaff('Q', 'DQA')
    f = 'rosalind_gaff_data6.dat'
    gaff(f)
    gaff(f, optimal_alignment=optimal_alignment_tuple)
    
