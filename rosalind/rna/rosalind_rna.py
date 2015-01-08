#!/usr/bin/env python
'''
============================================================
http://rosalind.info/problems/rna/

Given: A DNA string t having length at most 1000 nt.

Return: The transcribed RNA string of t.
============================================================
'''
from rosalind.rosutil import read_str

transcribe = lambda s: ''.join(('U' if x == 'T' else x) for x in s)
if __name__ == "__main__":
    print transcribe(read_str('rosalind_rna_sample.dat'))
    print transcribe(read_str('rosalind_rna.dat'))
