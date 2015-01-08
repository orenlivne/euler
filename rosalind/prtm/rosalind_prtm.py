'''
============================================================
http://rosalind.info/problems/prtm

Chaining the Amino Acidsclick to expandclick to expand

Problem

In a weighted alphabet, every symbol is assigned a positive real number called a weight. A string formed from a weighted alphabet is called a weighted string, and its weight is equal to the sum of the weights of its symbols.

The standard weight assigned to each member of the 20-symbol amino acid alphabet is the monoisotopic mass of the corresponding amino acid.

Given: A protein string P of length at most 1000 aa.

Return: The total weight of P. Consult the monoisotopic mass table.
============================================================
'''
from rosalind.rosutil import read_str, aa_mass

'''Return the amino acid mass of the protein whose string s.'''
prtm = lambda s: sum(aa_mass[x] for x in s)

if __name__ == "__main__":
    print prtm(read_str('rosalind_prtm.dat')) # 821.392
    print prtm(read_str('rosalind_prtm_sample.dat'))
    