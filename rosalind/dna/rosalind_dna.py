#!/usr/bin/env python
'''
============================================================
http://rosalind.info/problems/dna/

Given: A DNA string s of length at most 1000 nt.

Return: Four integers (separated by spaces) counting the respective number of times that the symbols 'A', 'C', 'G', and 'T' occur in s.
============================================================
'''
from rosalind.rosutil import read_str

def histogram(s):
    d = {}
    for x in s: d[x] = d.setdefault(x, 0) + 1
    return ' '.join(map(str, (d[x] for x in ['A', 'C', 'G', 'T'])))
         
if __name__ == "__main__":
    print histogram(read_str('rosalind_dna.dat'))
    print histogram(read_str('rosalind_dna_sample.dat'))
