'''
============================================================
http://rosalind.info/problems/motz

To count all possible secondary structures of a given RNA string that do not contain pseudoknots, we need to modify the Motzkin recurrence so that it counts only matchings of basepair edges in the bonding graph corresponding to the RNA string; see Figure 2

Given: An RNA string s of length at most 300 bp.

Return: The total number of noncrossing matchings of basepair edges in the bonding graph of s, modulo 1,000,000.
============================================================
'''
import rosalind.rosutil as ro

class NonCrossingMatching(object):
    '''Computes # of max matching modulo r using DP, memoization.'''
    def __init__(self, r):
        self._m, self._r = {}, r  # _m = memo array

    def m(self, s):
        '''Returns the number of non-crossing matching in the string s.'''
        if not s: return 1
        if not s in self._m:
            s0c = ro.RNA_COMPLEMENT[s[0]]
            C = [i for i in xrange(1, len(s)) if s[i] == s0c]
            self._m[s] = (self.m(s[1:]) + ro.sum_mod((self.m(s[1:i]) * self.m(s[i + 1:]) for i in C), self._r)) % self._r
        return self._m[s]

def num_noncrossing_matching(s, r=1000000L):
    '''Returns the number of non-crossing matching in the RNA string s.'''
    return NonCrossingMatching(r).m(s)

def motz(f):
    '''Main driver to solve this problem.'''
    return num_noncrossing_matching(ro.read_fafsa(f))

if __name__ == "__main__":
    # TODO: convert to a test suite
    #print num_noncrossing_matching('AUAU')  # 7
    # Test the feasibility of solving the problem given its input string length requirement 
    #print num_noncrossing_matching(ro.random_string(300, alphabet='ACGU'))
    
    print motz('rosalind_motz_sample.dat')
    print motz('rosalind_motz.dat')
