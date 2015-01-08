'''
============================================================
http://rosalind.info/problems/kmer

For a fixed positive integer k, order all possible k-mers taken from an underlying alphabet lexicographically.

Then the k-mer composition of a string s can be represented by an array A for which A[m] denotes the number of times that the mth k-mer (with respect to the lexicographic order) appears in s.

Given: A DNA string s in FASTA format (having length at most 100 kbp).

Return: The 4-mer composition of s.
============================================================
'''
import rosalind.rosutil as ro, itertools as it
from numpy.ma.testutils import assert_equal

kmer = lambda file_name: ' '.join(it.imap(str, ro.kmer_composition(ro.fafsa_values(file_name)[0], 4)))

def test_kmer_composition(s, k, expected):
    assert_equal(ro.kmer_composition(s, k), expected, 'Wrong string k-mer composition')
    
if __name__ == "__main__":
    test_kmer_composition('TTGATTACCTTATTTGATCATTACACATTGTACGCTTGTGTCAAAATATCACATGTGCCT', 2, [3, 5, 0, 8, 6, 2, 1, 3, 2, 2, 0, 4, 5, 3, 7, 8])
    test_kmer_composition(ro.fafsa_values('rosalind_kmer_sample.dat')[0], 4, [4, 1, 4, 3, 0, 1, 1, 5, 1, 3, 1, 2, 2, 1, 2, 0, 1, 1, 3, 1, 2, 1, 3, 1, 1, 1, 1, 2, 2, 5, 1, 3, 0, 2, 2, 1, 1, 1, 1, 3, 1, 0, 0, 1, 5, 5, 1, 5, 0, 2, 0, 2, 1, 2, 1, 1, 1, 2, 0, 1, 0, 0, 1, 1, 3, 2, 1, 0, 3, 2, 3, 0, 0, 2, 0, 8, 0, 0, 1, 0, 2, 1, 3, 0, 0, 0, 1, 4, 3, 2, 1, 1, 3, 1, 2, 1, 3, 1, 2, 1, 2, 1, 1, 1, 2, 3, 2, 1, 1, 0, 1, 1, 3, 2, 1, 2, 6, 2, 1, 1, 1, 2, 3, 3, 3, 2, 3, 0, 3, 2, 1, 1, 0, 0, 1, 4, 3, 0, 1, 5, 0, 2, 0, 1, 2, 1, 3, 0, 1, 2, 2, 1, 1, 0, 3, 0, 0, 4, 5, 0, 3, 0, 2, 1, 1, 3, 0, 3, 2, 2, 1, 1, 0, 2, 1, 0, 2, 2, 1, 2, 0, 2, 2, 5, 2, 2, 1, 1, 2, 1, 2, 2, 2, 2, 1, 1, 3, 4, 0, 2, 1, 1, 0, 1, 2, 2, 1, 1, 1, 5, 2, 0, 3, 2, 1, 1, 2, 2, 3, 0, 3, 0, 1, 3, 1, 2, 3, 0, 2, 1, 2, 2, 1, 2, 3, 0, 1, 2, 3, 1, 1, 3, 1, 0, 1, 1, 3, 0, 2, 1, 2, 2, 0, 2, 1, 1])
    print kmer('rosalind_kmer_sample.dat')
    print kmer('rosalind_kmer.dat')
    
