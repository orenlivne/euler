'''
============================================================
http://rosalind.info/problems/tfsq

Sometimes it's necessary to convert data from FASTQ format to FASTA format. For example, you may want to perform a BLAST search using reads in FASTQ format obtained from your brand new Illumina Genome Analyzer.

Links:

A FASTQ to FASTA converter can be accessed from the Sequence conversion website

A free GUI converter developed by BlastStation is available here for download or as an add-on to Google Chrome.

There is a FASTQ to FASTA converter in the Galaxy web platform. Note that you should register in the Galaxy and upload your file prior to using this tool.

Given: FASTQ file

Return: Corresponding FASTA records
============================================================
'''
import sys
from Bio import SeqIO

def tfsq(f):
    '''Main driver to solve this problem.'''
    SeqIO.convert(open(f, 'rb'), 'fastq', sys.stdout, 'fasta')

if __name__ == "__main__":
    # tfsq('rosalind_tfsq_sample.dat')
    tfsq('rosalind_tfsq.dat')
