'''
============================================================
http://rosalind.info/problems/conv


A multiset is a generalization of the notion of set to include a collection of objects in which each object may occur more than once (the order in which objects are given is still unimportant). For a multiset S, the multiplicity of an element x is the number of times that x occurs in the set; this multiplicity is denoted S(x). Note that every set is included in the definition of multiset.

The Minkowski sum of multisets S1 and S2 containing real numbers is the new multiset S1+S2 formed by taking all possible sums s1+s2 of an element s1 from S1 and an element s2 from S2. The Minkowski sum could be defined more concisely as S1+S2=s1+s2:s1inS1,s2inS2, The Minkowski difference S1-S2 is defined analogously by taking all possible differences s1-s2.

If S1 and S2 represent simplified spectra taken from two peptides, then S1-S2 is called the spectral convolution of S1 and S2. In this notation, the shared peaks count is represented by (S2-S1)(0), and the value of x for which (S2-S1)(x) has the maximal value is the shift value maximizing the number of shared masses of S1 and S2.

Given: Two multisets of positive real numbers S1 and S2. The size of each multiset is at most 200.

Return: The largest multiplicity of S1-S2, as well as the absolute value of the number x maximizing (S1-S2)(x) (you may return any such value if multiple solutions exist).

============================================================
'''
import rosalind.rosutil as ro, StringIO , numpy as np

def max_multiplicity(s1, s2, tol=1e-10):
    '''The maximum multiplicity of s1-s2 and its maximizer element, where s1, s2 are mass multisets.''' 
    d = np.array(sorted(x - y for x in s1 for y in s2))
    i = np.where(np.diff(d) > tol)[0]
    return max(zip(np.diff(np.concatenate((i, [len(d) - 1]), axis=0)), d[i + 1]))

def conv(f, tol=1e-10):
    '''Main driver to solve this problem.'''
    lines = ro.read_lines(f)
    s1, s2 = np.loadtxt(StringIO.StringIO(lines[0])), np.loadtxt(StringIO.StringIO(lines[1]))
    return ro.join_list(max_multiplicity(s1, s2), delimiter='\n')
    
if __name__ == "__main__":
    # print conv('rosalind_conv_sample.dat')
    print conv('rosalind_conv.dat')
