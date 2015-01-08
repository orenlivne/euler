'''
============================================================
http://rosalind.info/problems/gbk

Given: A genus name, followed by two dates in YYYY/M/D format.

Return: The number of Nucleotide GenBank entries for the given genus that were published between the dates specified.
============================================================
'''
import rosalind.rosutil as ro, rosalind.rosdb as rd
from Bio import Entrez

Entrez.email = "god@heaven.gom"

def gbk(f):
    org, start, stop = ro.read_lines(f)
    return rd.num_records('nucleotide', '%s[Organism] AND %s:%s[dp]' % (org, start, stop))

if __name__ == "__main__":
    print gbk('rosalind_gbk_sample.dat')
    print gbk('rosalind_gbk.dat')
