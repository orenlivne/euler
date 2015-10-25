'''
============================================================
http://rosalind.info/problems/2b

There are three different ways to divide a DNA string into codons for translation, one starting at each of the first three starting positions of the string. These different ways of dividing a DNA string into codons are called reading frames. Since DNA is double-stranded, a genome has six reading frames (three on each strand), as shown in Figure 1.

We say that a DNA string Pattern encodes an amino acid string Peptide if the RNA string transcribed from either Pattern or its reverse complement Pattern translates into Peptide.

Peptide Encoding Problem

Find substrings of a genome encoding a given amino acid sequence.

Given: A DNA string Text and an amino acid string Peptide.

Return: All substrings of Text encoding Peptide (if any such substrings exist).
============================================================
'''
from rosutil import read_str, RNA_TRANSLATION, STOP_VALUE
from itertools import takewhile

def encoding_patterns():
  '''Returns the list of DNA patterns that encodes the amino acid string a.''' 
RNA_TRANSLATION = dict(x.split(' ') for x in read_lines(_CODON_TABLE_FILE_NAME))

def mrna_to_protein(s):
    '''Converts mRNA string to a protein string.'''
    return ''.join(takewhile(lambda v: v != STOP_VALUE, (RNA_TRANSLATION[s[i:i + 3]] for i in xrange(0, len(s), 3))))

if __name__ == "__main__":
#    print mrna_to_protein(read_str('rosalind_2b_sample.dat'))
    print mrna_to_protein(read_str('rosalind_2b.dat'))
