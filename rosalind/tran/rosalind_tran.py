'''
============================================================
http://rosalind.info/problems/tran

For DNA strings s1 and s2 having the same length, their transition/transversion
ratio R(s1,s2) is the ratio of the total number of transitions to the total
number of transversions, where symbol substitutions are inferred from
mismatched corresponding symbols as when calculating Hamming distance (see "Counting Point Mutations").

Given: Two DNA strings s1 and s2 of equal length (at most 1 kbp).

Return: The transition/transversion ratio R(s1,s2).
============================================================
'''
from __future__ import division
import rosalind.rosutil as ro, itertools as it

_TRANSITION_CODE = {'A': 1, 'G': 1, 'C': 2, 'T': 2}

def count_tran(s, t):
    transitions, transversions = 0, 0
    for x, y in ((x, y) for x, y in it.izip(s, t) if x != y):
        if _TRANSITION_CODE[x] == _TRANSITION_CODE[y]: transitions += 1
        else: transversions += 1
    return transitions, transversions

def tran(f):
    transitions, transversions = count_tran(*ro.fafsa_values(f))
    return transitions / transversions 

if __name__ == "__main__":
    print tran('rosalind_tran_sample.dat')
    print tran('rosalind_tran.dat')
    
