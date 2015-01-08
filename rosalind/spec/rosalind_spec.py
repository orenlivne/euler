'''
============================================================
http://rosalind.info/problems/spec

The prefix spectrum of a weighted string is the collection of all its prefix weights.

Given: A list L of n (n<=100) positive real numbers.

Return: A protein string of length n-1 whose prefix spectrum is equal to L (if multiple solutions exist, you may output any one of them). Consult the monoisotopic mass table.
============================================================
'''
import rosalind.rosutil as ro, numpy as np

spec = lambda f: ''.join(map(ro.aa_of_mass, np.diff(map(float, ro.read_lines(f)))))

if __name__ == "__main__":
    print spec('rosalind_spec_sample.dat')
    print spec('rosalind_spec.dat')
