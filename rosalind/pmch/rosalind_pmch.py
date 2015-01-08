'''
============================================================
http://rosalind.info/problems/pmch

Given: An RNA string s of length at most 80 bp having the same number of occurrences of 'A' as 'U' and the same number of occurrences of 'C' as 'G'.

Return: The total possible number of perfect matchings of basepair edges in the bonding graph of s.
============================================================
'''
import rosalind.rosutil as ro
from math import factorial
from collections import Counter

def pmch(f):
    c = Counter(ro.fafsa_values(f)[0])
    return factorial(c['A']) * factorial(c['G'])

if __name__ == "__main__":
    print pmch('rosalind_pmch_sample.dat')
    print pmch('rosalind_pmch.dat')
    