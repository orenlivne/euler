'''
============================================================
http://rosalind.info/problems/prsm

The complete spectrum of a weighted string s is the multiset
S[s] containing the weights of every prefix and suffix of s.

Given: A positive integer n followed by a collection of n
protein strings s1, s2, ..., sn and a multiset R of positive
numbers (corresponding to the complete spectrum of some
unknown protein string).

Return: The maximum multiplicity of R-S[sk] taken over all
strings sk, followed by the string sk for which this maximum
multiplicity occurs (you may output any such value if
multiple solutions exist).
============================================================
'''
import rosalind.rosutil as ro, numpy as np, itertools as it
from rosalind.rosalind_prtm import prtm
from rosalind.rosalind_conv import max_multiplicity

def read_data(f):
    '''Read input file. Return a list of candidate proteins and target mass spectrum.'''
    n = int(open(f, 'rb').next())
    return np.array(list(it.islice(ro.iterlines(f), 1, n + 1))), np.loadtxt(f, skiprows=n + 1)

'''Return the protein mass spectrum corresponding to the protein string s.'''
prt_spec = lambda s: [prtm(s[k:]) for k in xrange(len(s))] + [prtm(s[:k]) for k in xrange(1, len(s))]

def closest_protein(proteins, spectrum):
    '''Given a list of candidate proteins '\proteins\'and target mass spectrum \'spectrum\',
    return the maximum maximum multiplicity between spectrum and p over all elements p of
    proteins, and its maximizer protein string p.'''
    return max((max_multiplicity(spectrum, prt_spec(p))[0], p) for p in proteins)

def prsm(f):
    '''Main driver to solve this problem.'''
    return ro.join_list(closest_protein(*read_data(f)), delimiter='\n')

if __name__ == "__main__":
    #print prsm('rosalind_prsm_sample.dat')
    print prsm('rosalind_prsm.dat')
