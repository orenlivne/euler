'''
============================================================
http://rosalind.info/problems/mmch

The graph theoretical analogue of the quandary stated in the introduction above is that if we have an RNA string s that does not have the same number of 'C's as 'G's and the same number of 'A's as 'U's, then the bonding graph of s cannot possibly possess a perfect matching among its basepair edges. For example, see Figure 1; in fact, most bonding graphs will not contain a perfect matching.

In light of this fact, we define a maximum matching in a graph as a matching containing as many edges as possible. See Figure 2 for three maximum matchings in graphs.

A maximum matching of basepair edges will correspond to a way of forming as many base pairs as possible in an RNA string, as shown in Figure 3.

Given: An RNA string s of length at most 100.

Return: The total possible number of maximum matchings of basepair edges in the bonding graph of s.
============================================================
'''
import rosalind.rosutil as ro
from rosalind.rosalind_mmch import num_max_matching
from collections import Counter

class MaxMatching(object):
    '''Computes # of max matching modulo r using DP, memoization.'''
    def __init__(self):
        self._m = {}  # _m = memo array

    def m(self, s):
        '''Returns the number of max matching for the binary tuple s.'''
        if not s in self._m:
            # print s
            if s == '': self._m[s] = 1
            else:
                # print s
                s0c = ro.RNA_COMPLEMENT[s[0]]
                c = Counter(s)
                C = [i for i in xrange(1, len(s)) if s[i] == s0c]
                self._m[s] = sum(self.m(s[1:i] + s[i + 1:]) for i in C)
                if c[s[0]] > c[s0c]: self._m[s] += self.m(s[1:])
        return self._m[s]

def num_max_matching_dp(s):
    '''Returns the number of max matching in the RNA string s.'''
    return MaxMatching().m(s)

def mmch_dp(f):
    '''Main driver to solve this problem.'''
    return num_max_matching_dp(ro.read_fafsa(f))

if __name__ == "__main__":
    # TODO: convert to a test suite
#    print num_max_matching_dp('AUGCUUC')  # 6
    s = 'AUA'
    print num_max_matching_dp(s), num_max_matching(s)  # 6
    s = 'AUAGGAAAUUCGCCGC'
    print num_max_matching_dp(s), num_max_matching(s)  # 6
    
    # print mmch('rosalind_mmch_sample.dat')
    # print mmch('rosalind_mmch.dat')
