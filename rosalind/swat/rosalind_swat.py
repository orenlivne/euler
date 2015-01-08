'''
============================================================
http://rosalind.info/problems/swat

The EBI portal for Water, a program for local alignment in the EMBOSS suite, can be accessed here.

Use:

The BLOSUM62 scoring matrix.
Gap opening penalty of 10.
Gap extension penalty of 1.
Given: Two UniProt ID's corresponding to two protein strings s and t.

Return: The maximum score of any local alignment of s and t.
============================================================
'''
import rosalind.rosutil as ro, rosdb as rd

def swat(f):
    '''Print strings for local alignment score.'''
    a, b = ro.read_str(f).split()
    s, t = rd.protein_record(a).sequence, rd.protein_record(b).sequence
    print s
    print t

if __name__ == "__main__":
    # swat('rosalind_swat_sample.dat')
    swat('rosalind_swat.dat')
