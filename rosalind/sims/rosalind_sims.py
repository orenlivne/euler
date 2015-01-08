'''
============================================================
http://rosalind.info/problems/sims

Given a string s and a motif t, an alignment of a substring
of s against all of t is called a fitting alignment. Our aim
is to find a substring s' of s that maximizes an alignment
score with respect to t.

Note that more than one such substring of s may exist,
depending on the particular strings and alignment score used.
One candidate for scoring function is the one derived from
edit distance; In this problem, we will consider a slightly
different alignment score, in which all matched symbols count
as +1 and all mismatched symbols (including insertions and
deletions) receive a cost of -1. Let's call this scoring
function the mismatch score. See Figure 1 for a comparison
of global, local, and fitting alignments with respect to
mismatch score.

Given: Two DNA strings s and t, where s has length at most
10 kbp and t represents a motif of length at most 1 kbp.

Return: An optimal fitting alignment score with respect to
the mismatch score defined above, followed by an optimal
fitting alignment of a substring of s against t. If multiple
such alignments exist, then you may output any one.
============================================================
'''
import rosalind.rosutil as ro, rosalign as ra

def sims(f, debug=False, align='fit'):
    '''Main driver to solve the SIMS problem.'''
    (s, t), score, gap_score = ro.fafsa_values(f), ra.FixedCost(1, -1), -1
    d, (ss, tt) = ra.optimal_alignment(s, t, score, gap_score, gap_score, align=align, debug=debug) 
    print d
    print ss
    print tt
    #print ra.score_of(ss, tt, score, gap_score, gap_score)

if __name__ == "__main__":
    sims('rosalind_sims_sample.dat', debug=1)
    #sims('rosalind_sims_sample2.dat', align='local')
    #sims('rosalind_sims_sample2.dat', align='fit')
    sims('rosalind_sims.dat', debug=1)
