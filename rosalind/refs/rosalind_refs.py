'''
============================================================
http://rosalind.info/problems/refs

Given: A species, two integers a and b, and a date in the form YYYY/MM/DD.

Return: The total number of records for genes of length between a and b for the given species submitted before the given date.
============================================================
'''
import rosalind.rosutil as ro
from Bio import Entrez

Entrez.email = "god@heaven.gom"

def refs(f):
    org, start, stop, before = ro.read_lines(f)
    return int(Entrez.read(Entrez.esearch(db='nucleotide',  term='%s[Organism] AND srcdb_refseq[PROP] AND %s:%s[Sequence length] AND 1986/01/01:%s[dp]' % (org, start, stop, before)))['Count'])

if __name__ == "__main__":
    print refs('rosalind_refs_sample.dat')
    print refs('rosalind_refs.dat')
