'''
============================================================
http://rosalind.info/problems/osym

Say that we have two strings s and t of respective lengths m
and n and an alignment score. Let's define a matrix M
corresponding to s and t by setting Mj,k equal to the
maximum score of any alignment that aligns s[j] with t[k].
So each entry in M can be equal to at most the maximum score
of any alignment of s and t.

Given: Two DNA strings s and t in FASTA format, each having
length at most 1000 bp.

Return: The maximum alignment score of a global alignment of
s and t, followed by the sum of all elements of the matrix M
corresponding to s and t that was defined above. Apply the
mismatch score introduced in "Finding a Motif with
Modifications".
============================================================
'''
import rosalind.rosutil as ro, rosalign as ra, numpy as np

def osym(f, debug=1):
    '''Main driver to solve the GLOB problem.'''
    (x, y), score, gap_score = ro.fafsa_values(f), ra.FixedCost(1, -1), -1
    a = ra.global_alignment_score_matrix((x, y), score, gap_score, debug=debug)
    m = a[:-1, :-1] + np.flipud(np.fliplr(ra.global_alignment_score_matrix((''.join(reversed(x)), ''.join(reversed(y))), ra.FixedCost(1, -1), -1, debug=debug)[:-1, :-1])) + \
    np.array([[score(x[i], y[j]) for j in xrange(len(y))] for i in xrange(len(x))])
    print m[-1, -1]
    print np.sum(m)

if __name__ == "__main__":
    #osym('rosalind_osym_sample.dat')
    osym('rosalind_osym.dat', debug=1)
