'''
============================================================
http://rosalind.info/problems/edta

An alignment of two strings s and t is defined by two
strings s' and t' satisfying the following three conditions:
1. s' and t' must be formed from adding gap symbols "-" to
each of s and t, respectively; as a result, s and t will
form subsequences of s' and t'. 2. s' and t' must have the
same length. 3. Two gap symbols may not be aligned; that is,
if s'[j] is a gap symbol, then t'[j] cannot be a gap symbol
 and vice-versa.

We say that s' and t' augment s and t. Writing s' directly
over t' so that symbols are aligned provides us with a
scenario for transforming s into t. Mismatched symbols from
s and t correspond to symbol substitutions; a gap symbol
s'[j] aligned with a non-gap symbol t'[j] implies the
insertion of this symbol into t; a gap symbol t'[j] aligned
with a non-gap symbol s'[j] implies the deletion of this
symbol from s.

Thus, an alignment represents a transformation of s into t
via edit operations. We define the corresponding edit
alignment score of s' and t' as dH(s',t') (Hamming distance
is used because the gap symbol has been introduced for
insertions and deletions). It follows that
dE(s,t)=mins',t'dH(s',t'), where the minimum is taken over
all alignments of s and t. We call such a minimum score
alignment an optimal alignment (with respect to edit
distance).

Given: Two protein strings s and t in FASTA format (with
each string having length at most 1000 aa).

Return: The edit distance dE(s,t) followed by two augmented 
strings s' and t' representing an optimal alignment of s and
t.
============================================================
'''
import rosalind.rosutil as ro

'''Alignment codes'''
EQ, T_GAP, S_GAP = range(3)

def alignment(x, y, a, gap='-'):
    '''Return the alignment strings from the original strings x and y and the alignment coding vector a.'''
    s, t, ix, iy = '', '', iter(x), iter(y)
    for ai in a:
        if ai == EQ:
            s += ix.next()
            t += iy.next()
        elif ai == T_GAP:
            s += ix.next()
            t += gap
        else:
            s += gap
            t += iy.next()
    return s, t
    
def edit_distance_alignment(x, y, debug=False):
    '''Integrated DP+backtracking, O(mn) time, O(min(m,n)) storage.'''
    m, n = len(x), len(y)
    if m < n:
        d, (yy, xx) = edit_distance_alignment(y, x, debug=debug)
        return d, (xx, yy)
    c, c_old, a, a_old = range(n + 1), [0] * (n + 1), [tuple([S_GAP] * i) for i in xrange(n + 1)], [()] * (n + 1)
    if debug:
        print c
        #print a 
    for i, xi in enumerate(x, 1):
        c_old[:] = c[:]; a_old[:] = a[:]
        # Initial condition
        c[0] = i; a[0] = a_old [0 ] + (T_GAP,) 
        for j, yj in enumerate(y, 1):
            if xi == yj: c[j], a[j] = c_old[j - 1], a_old[j - 1] + (EQ,)
            else:
                c_min = min(c_old[j - 1], c_old[j], c[j - 1])
                if c_min == c_old[j - 1]: a_min = a_old[j - 1] + (EQ,)
                elif c_min == c_old[j]: a_min = a_old[j] + (T_GAP,)
                else: a_min = a[j - 1] + (S_GAP,)
                c[j], a[j] = c_min + 1, a_min
        if debug:
            print c
            #print a 
    return c[-1], alignment(x, y, a[-1])

def edta(f, debug=False):
    '''Main driver to solve this problem.'''
    x, y = ro.fafsa_values(f)
    d, (xx, yy) = edit_distance_alignment(x, y, debug=debug)
    print d
    print xx
    print yy

if __name__ == "__main__":
#     d, (xx, yy) = edit_distance_alignment('PRE', 'PI')
#     print d
#     print xx
#     print yy
    edta('rosalind_edta_sample.dat', debug=True)
    #edta('rosalind_edta.dat', debug=True)
