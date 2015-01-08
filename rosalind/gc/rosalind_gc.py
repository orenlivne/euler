'''
============================================================
http://rosalind.info/problems/gc

Identifying Unknown DNA Quickly

Problem

The GC-content of a DNA string is given by the percentage of symbols in the string that are 'C' or 'G'. For example, the GC-content of "AGCTATAG" is 37.5%. Note that the reverse complement of any DNA string has the same GC-content.

DNA strings must be labeled when they are consolidated into a database. A commonly used method of string labeling is called FASTA format. In this format, the string is introduced by a line that begins with '>', followed by some labeling information. Subsequent lines contain the string itself; the first line to begin with '>' indicates the label of the next string.

In Rosalind's implementation, a string in FASTA format will be labeled by the ID "Rosalind_xxxx", where "xxxx" denotes a four-digit code between 0000 and 9999.

Given: At most 10 DNA strings in FASTA format (of length at most 1 kbp each).

Return: The ID of the string having the highest GC-content, followed by the GC-content of that string. Rosalind allows for a default error of 0.001 in all decimal answers unless otherwise stated; please see the note on absolute error below.

Sample Dataset


Rosalind_0808
60.919540

Note on Absolute Error

We say that a number x is within an absolute error of y to a correct solution if x is within y of the correct solution. For example, if an exact solution is 6.157892, then for x to be within an absolute error of 0.001, we must have that |x-6.157892|<0.001, or 6.156892<x<6.158892.

Error bounding is a vital practical tool because of the inherent round-off error in representing decimals in a computer, where only a finite number of decimal places are allotted to any number. After being compounded over a number of operations, this round-off error can become evident. As a result, rather than testing whether two numbers are equal with x=z, you may wish to simply verify that |x-z| is very small.

The mathematical field of numerical analysis is devoted to rigorously studying the nature of computational approximation.
============================================================
'''
from __future__ import division
import rosalind.rosutil as ro

def max_gc_content(file_name):
    gc, label = max((ro.gc_content(v), k) for k, v in ro.fafsa_iteritems(file_name))
    print label
    print '%.6f' % (100.*gc,)
    
if __name__ == "__main__":
    max_gc_content('rosalind_gc_sample.dat')
    max_gc_content('rosalind_gc.dat')
