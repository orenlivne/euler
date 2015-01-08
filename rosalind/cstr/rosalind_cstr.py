'''
============================================================
http://rosalind.info/problems/cstr

A collection of strings is characterizable if there are at most two possible choices for the symbol at each position of the strings.

Given: A collection of at most 100 characterizable DNA strings, each of length at most 300 bp.

Return: A character table for which each nontrivial character encodes the symbol choice at a single position of the strings. (Note: the choice of assigning '1' and '0' to the two states of each SNP in the strings is arbitrary.)
============================================================
'''
import rosalind.rosutil as ro, numpy as np
from collections import Counter

def char_array(s):
    return np.array([[x for x in row] for row in s])

def char_table(s):
    return [s[:, j] == s[0, j][0] for j in np.where(map(lambda x: len(x) >= 2 and min(x.values()) >= 2, (Counter(s[:, j]) for j in xrange(s.shape[1]))))[0]]

def cstr(f):
    '''Main driver to solve this problem.'''
    for y in char_table(char_array(np.loadtxt(open(f, 'rb'), dtype=str))):
        print ro.join_list(map(int, y), delimiter='')

if __name__ == "__main__":
    #cstr('rosalind_cstr_sample.dat')
    cstr('rosalind_cstr.dat')
