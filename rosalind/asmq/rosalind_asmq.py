'''
============================================================
http://rosalind.info/problems/asmq

Given a collection of DNA strings representing contigs, we
use the N statistic NXX (where XX ranges from 01 to 99) to
represent the maximum positive integer L such that the total
number of nucleotides of all contigs having length >= L is
at least XX% of the sum of contig lengths. The most commonly
used such statistic is N50, although N75 is also worth
mentioning.

Given: A collection of at most 1000 DNA strings (whose
combined length does not exceed 50 kbp).

Return: N50 and N75 for this collection of strings.
============================================================
'''
from __future__ import division
import rosalind.rosutil as ro, numpy as np, itertools as it
from collections import Counter

def N(S, a):
    '''Return the N-statistic of the contig list S, evaluated at threshold a.'''
    entries = np.array(sorted(Counter(len(x) for x in S).iteritems(), reverse=True))
    L, C = entries[:, 0], entries[:, 1] * entries[:, 0]
    return next(l for l, c in it.izip(L, np.cumsum(C) / sum(C)) if c >= a)
     
def asmq(f):
    '''Main driver to solve this problem.'''
    S = ro.read_lines(f)
    print N(S, 0.5), N(S, 0.75)

if __name__ == "__main__":
    asmq('rosalind_asmq_sample.dat')
    asmq('rosalind_asmq.dat')
