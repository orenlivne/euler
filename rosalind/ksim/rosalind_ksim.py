'''
============================================================
http://rosalind.info/problems/ksim

Given: A positive integer k (k<=50), a DNA string s of
length at most 5 kbp representing a motif, and a DNA string
t of length at most 50 kbp representing a genome.

Return: All substrings t' of t such that the edit distance
dE(s,t') is less than or equal to k. Each substring should
be encoded by a pair containing its location in t followed
by its length.
============================================================
'''
import rosalind.rosutil as ro, time, numpy as np
from numpy.ma.testutils import assert_equal
from rosalind.rosalind_edit import edit_distance

def ed_ending_at(x, y, free_x_gaps=True):
    '''Lean storage row-by-row DP, O(mn) time, O(min(m,n)) storage.'''
    n = len(y)
    c, c_old = [0] * (n + 1) if free_x_gaps else range(n + 1), [0] * (n + 1)
    #print c
    for i, xi in enumerate(x, 1):
        c_old[:] = c[:]
        c[0] = i
        for j, yj in enumerate(y, 1): c[j] = c_old[j - 1] if xi == yj else min(c_old[j - 1], c_old[j], c[j - 1]) + 1
        #print c
    return c

def max_repeats(t, s, k, debug=0):
    '''Return all (start,length) tuples of approximate maximal repeats of s in t up to edit distance k.'''
    if debug >= 1:
        print 'max_repeats(k=%d)' % (k,)
        print 'Pattern s', s
        print 'Text t', t
    start = time.time()
    b = ed_ending_at(s, t)
    ends = [j for j, e in enumerate(b) if e <= k]
    if debug >= 1:
        t_sec = time.time() - start
        print 'Finding ends took', t_sec, 'secs', t_sec / (len(s) * len(t)), 'sec/entry'
        print '#ends', len(ends)
    rev_s, m = s[-1::-1], len(s)
    for j in ends:
        i = max(j - m - k, 0)
        if debug >= 1: start = time.time()
        tt = ''.join(reversed(t[i:j]))
        a = np.array(ed_ending_at(rev_s, tt, free_x_gaps=False))
        J = np.where(a <= k)[0]
        for offset in J:
            yield j - offset, j, a[offset]
        if debug >= 1:
            t_sec = time.time() - start
            print 'i', i, 'j', j, 'took', t_sec, 'secs', t_sec / (len(s) * (j - i)), 'sec/entry'

def ksim(f, debug=0):
    '''Main driver to solve the LOCA problem.'''
    lines = ro.read_lines(f)
    for i, j, _ in max_repeats(lines[2], lines[1], int(lines[0]), debug=debug): print i + 1, j - i
    
#--------------------------
# Testing
#--------------------------
def max_repeats_bf(t, s, k):
    '''Brute force implementation.'''
    n = len(t)
    return ((i, j, d) for i, j, d in ((i, j, edit_distance(t[i:j], s)) for j in xrange(n + 1)  for i in xrange(j)) if d <= k)

def test_ksim(f, debug=0, impl=max_repeats):
    '''Main driver to solve the LOCA problem.'''
    lines = ro.read_lines(f)
    k, s, t = int(lines[0]), lines[1], lines[2]
    a_bf = sorted(max_repeats_bf(t, s, k))
    a = sorted(impl(t, s, k, debug=debug))
    if debug >= 1:
        print f
        print 'actual', a
        print 'bf    ', a_bf
        print len(a_bf)
    assert_equal(a, a_bf, err_msg='Wrong maximum repeats set for file_name %s' % (f,))

if __name__ == "__main__":
#    np.set_printoptions(linewidth=1000)
    #start = time.time()
#     for f in ('rosalind_ksim_sample.dat', 
#               'rosalind_ksim_sample2.dat', 
#               'rosalind_ksim_sample3.dat', 
#               'rosalind_ksim_sample4.dat', 
#               'rosalind_ksim_sample5.dat', 
#               'rosalind_ksim_sample6.dat', 
#               'rosalind_ksim_sample7.dat',
#               'rosalind_ksim_sample8.dat'):
#         test_ksim(ro.ROSALIND_HOME + '/ksim/' + f)
    ksim(ro.ROSALIND_HOME + '/ksim/rosalind_ksim_sample8.dat', debug=0)
#    ksim(ro.ROSALIND_HOME + '/ksim/rosalind_ksim.dat', debug=1)
#    print 'time', time.time() - start
