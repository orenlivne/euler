'''
============================================================
http://rosalind.info/problems/prot

The Genetic Codeclick to expand

Problem

The 20 commonly occurring amino acids are abbreviated by using 20 letters from the English alphabet (all letters except for B, J, O, U, X, and Z). Protein strings are constructed from these 20 symbols. Henceforth, the term genetic string will incorporate protein strings along with DNA strings and RNA strings.

The RNA codon table dictates the details regarding the encoding of specific codons into the amino acid alphabet.

Given: An RNA string s corresponding to a strand of mRNA (of length at most 10 kbp).

Return: The protein string encoded by s.
============================================================
'''
from rosalind.rosutil import read_str, RNA_TRANSLATION, STOP_VALUE
from itertools import takewhile

def mrna_to_protein(s):
    '''Convert mRNA string to a protein string.'''
    return reduce(lambda x, y: ''.join((x, y)), takewhile(lambda v: v != STOP_VALUE, (RNA_TRANSLATION[s[i:i + 3]] for i in xrange(0, len(s), 3))), '')

if __name__ == "__main__":
    print mrna_to_protein(read_str('rosalind_prot_sample.dat'))
    print mrna_to_protein(read_str('rosalind_prot.dat'))
