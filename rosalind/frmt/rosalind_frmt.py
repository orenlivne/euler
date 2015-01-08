'''
============================================================
http://rosalind.info/problems/frmt

Given: A collection of n (n<=10) GenBank entry IDs.

Return: The shortest of the strings associated with the IDs in FASTA format.
============================================================
'''
import rosalind.rosutil as ro
from Bio import Entrez, SeqIO

Entrez.email = "god@heaven.gom"

def frmt(f):
    ids = ' '.join(ro.read_str(f).split())
    handle = Entrez.efetch(db='nucleotide', id=ids, rettype='fasta')
    records = list(SeqIO.parse(handle, 'fasta'))  # we get the list of SeqIO objects in FASTA format
    x = min((len(x), x) for x in records)[1]
    print '>' + x.description
    print x.seq

if __name__ == "__main__":
    # frmt('rosalind_frmt_sample.dat')
    frmt('rosalind_frmt.dat')
