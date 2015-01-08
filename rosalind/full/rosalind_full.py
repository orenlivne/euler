'''
============================================================
http://rosalind.info/problems/full

Say that we have a string s containing t as an internal substring, so that there exist nonempty substrings s1 and s2 of s such that s can be written as s1ts2. A t-prefix contains all of s1 and none of s2; likewise, a t-suffix contains all of s2 and none of s1.

Given: A list L containing 2n+3 positive real numbers (n<=100). The first number in L is the parent mass of a peptide P, and all other numbers represent the masses of some b-ions and y-ions of P (in no particular order). You may assume that if the mass of a b-ion is present, then so is that of its complementary y-ion, and vice-versa.

Return: A protein string t of length n for which there exist two positive real numbers w1 and w2 such that for every prefix p and suffix s of t, each of w(p)+w1 and w(s)+w2 is equal to an element of L. (In other words, there exists a protein string whose t-prefix and t-suffix weights correspond to the non-parent mass values of L.) If multiple solutions exist, you may output any one.
============================================================
'''
import rosalind.rosutil as ro, itertools as it, numpy as np

def chain(l):
    '''Return the chain of letters of t from a sorted list of b-/y-ion masses.'''
    i, n = 0, len(l)
    while True:
        li = l[i]
        try: i, ti = it.dropwhile(lambda x: not x[1], ((k, ro.aa_of_mass_exact(l[k] - li)) for k in xrange(i + 1, n))).next()
        except StopIteration: break
        yield ti
    
def full(f):
    '''Main driver to solve this problem.'''
    l = np.loadtxt(f)[1:]
    return ''.join(it.islice(chain(l), (len(l) - 2) / 2))

if __name__ == "__main__":
    #print full('rosalind_full_sample.dat')
    print full('rosalind_full.dat')
