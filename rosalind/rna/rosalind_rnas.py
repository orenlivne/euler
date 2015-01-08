'''
============================================================
http://rosalind.info/problems/rnas

Given an RNA string s, we will augment the bonding graph of s by adding basepair edges connecting all occurrences of 'U' to all occurrences of 'G' in order to represent possible wobble base pairs.

We say that a matching in the bonding graph for s is valid if it is noncrossing (to prevent pseudoknots) and has the property that a basepair edge in the matching cannot connect symbols sj and sk unless k>=j+4 (to prevent nearby nucleotides from base pairing).

See Figure 1 for an example of a valid matching if we allow wobble base pairs. In this problem, we will wish to count all possible valid matchings in a given bonding graph; see Figure 2 for all possible valid matchings in a small bonding graph, assuming that we allow wobble base pairing.

Given: An RNA string s (of length at most 200 bp).

Return: The total number of distinct valid matchings of basepair edges in the bonding graph of s. Assume that wobble base pairing is allowed.
============================================================
'''
import rosalind.rosutil as ro

'''Which letters can a letter bind to, assuming wobble bonding.'''
_BONDING = {'A':'U', 'U':'AG', 'C':'G', 'G':'CU'}
'''Returns the number of wobble non-crossing matching in the string s with
minimium wobble distance min_wobble_dist between bases.'''
_wobb = lambda s, w: wobb(s[1:], w) + sum(wobb(s[1:i], w) * wobb(s[i + 1:], w) for i in [i for i in xrange(w, len(s)) if s[i] in _BONDING[s[0]]]) if s else 1
wobb = ro.memoize(_wobb)
rnas = lambda f: wobb(ro.read_str(f), 4) # Main driver to solve this problem.

if __name__ == "__main__":
    print rnas('rosalind_rnas_sample1.dat')
    print rnas('rosalind_rnas_sample.dat')
    print rnas('rosalind_rnas.dat')
