'''
============================================================
http://rosalind.info/problems/foun

Given: Two positive integers N and m, followed by an array A containing k integers between 0 and 2N. A[j] represents the number of recessive alleles for the j-th factor in a population of N diploid individuals.

Return: An mxk matrix B for which Bi,j represents the common logarithm of the probability that after i generations, no copies of the recessive allele for the j-th factor will remain in the population. Apply the Wright-Fisher model.
============================================================
'''
import rosalind.rosutil as ro, numpy as np, sys, itertools as it

def foun(f):
    '''Main driver to solve this problem.'''
    lines = ro.read_lines(f)
    (N, m), a = map(int, lines[0].split()), map(int, lines[1].split())
    b = np.zeros((m, len(a)))
    for j, aj in enumerate(a): b[:, j] = [np.log10(x[0]) for x in it.islice(ro.wf_pmf(2*N, aj), m)]
    np.savetxt(sys.stdout, b, '%f')

if __name__ == "__main__":
    #foun('rosalind_foun_sample.dat')
    foun('rosalind_foun.dat')
