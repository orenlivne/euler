'''
============================================================
http://rosalind.info/problems/need

An online interface to EMBOSS's Needle tool for aligning DNA and RNA strings can be found here.

Use:

The DNAfull scoring matrix; note that DNAfull uses IUPAC notation for ambiguous nucleotides.
Gap opening penalty of 10.
Gap extension penalty of 1.
For our purposes, the "pair" output format will work fine; this format shows the two strings aligned at the bottom of the output file beneath some statistics about the alignment.

Given: Two GenBank IDs.

Return: The maximum global alignment score between the DNA strings associated with these IDs.
============================================================
'''
import rosalind.rosutil as ro, rosdb as rd

def need(f):
    a, b = ro.read_str(f).split()
    s, t = rd.dna_seq_of_id(a), rd.dna_seq_of_id(b)
    print s
    print t
    
if __name__ == "__main__":
    need('rosalind_need_sample.dat')
    #need('rosalind_need.dat')
