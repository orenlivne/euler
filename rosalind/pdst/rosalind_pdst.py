'''
============================================================
http://rosalind.info/problems/pdst

For two strings s1 and s2 of equal length, the p-distance between them, denoted dp(s1,s2), is the proportion of corresponding symbols that differ between s1 and s2.

For a general distance function d on n taxa s1,s2,...,sn (taxa are often represented by genetic strings), we may encode the distances between pairs of taxa via a distance matrix D in which Di,j=d(si,sj).

Given: A collection of n (n<=10) DNA strings s1,...,sn of equal length (at most 1 kbp). Strings are given in FASTA format.

Return: The matrix D corresponding to the p-distance dp on the given strings. As always, note that your answer is allowed an absolute error of 0.001.

============================================================
'''
from __future__ import division
import rosalind.rosutil as ro

D = lambda s, t: sum(1 for i in xrange(len(s)) if s[i] != t[i]) / len(s)

def pdst(f):
    s = list(ro.fafsa_itervalues(f))
    print '\n'.join(' '.join(repr(D(x, y)) for y in s) for x in s)
     
if __name__ == "__main__":
    #pdst('rosalind_pdst_sample.dat')
    pdst('rosalind_pdst.dat')
    