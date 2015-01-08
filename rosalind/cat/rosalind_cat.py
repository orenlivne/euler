'''
============================================================
http://rosalind.info/problems/cat

A matching in a graph is noncrossing if none of its edges cross each other. If we assume that the n nodes of this graph are arranged around a circle, and if we label these nodes with positive integers between 1 and n, then a matching is noncrossing as long as there are not edges {i,j} and {k,l} such that i<k<j<l.

A noncrossing matching of basepair edges in the bonding graph corresponding to an RNA string will correspond to a possible secondary structure of the underlying RNA strand that lacks pseudoknots, as shown in Figure 3.

In this problem, we will consider counting noncrossing perfect matchings of basepair edges. As a motivating example of how to count noncrossing perfect matchings, let cn denote the number of noncrossing perfect matchings in the complete graph K2n. After setting c0=1, we can see that c1 should equal 1 as well. As for the case of a general n, say that the nodes of K2n are labeled with the positive integers from 1 to 2n. We can join node 1 to any of the remaining 2n-1 nodes; yet once we have chosen this node (say m), we cannot add another edge to the matching that crosses the edge {1,m}. As a result, we must match all the edges on one side of {1,m} to each other. This requirement forces m to be even, so that we can write m=2k for some positive integer k.

There are 2k-2 nodes on one side of {1,m} and 2n-2k nodes on the other side of {1,m}, so that in turn there will be ck-1 * cn-k different ways of forming a perfect matching on the remaining nodes of K2n. If we let m vary over all possible n-1 choices of even numbers between 1 and 2n, then we obtain the recurrence relation cn=SUM nk=1ck-1 * cn-k. The resulting numbers cn counting noncrossing perfect matchings in K2n are called the Catalan numbers, and they appear in a huge number of other settings. See Figure 4 for an illustration counting the first four Catalan numbers.

Given: An RNA string s having the same number of occurrences of 'A' as 'U' and the same number of occurrences of 'C' as 'G'. The length of the string is at most 300 bp.

Return: The total number of noncrossing perfect matchings of basepair edges in the bonding graph of s, modulo 1,000,000.
============================================================
'''
import rosalind.rosutil as ro

def _cum_count(s):
    '''Cumulative A,C,G,T counts (i-zipped) of the RNA string s.'''
    a, c, g, u = 0, 0, 0, 0
    for x in s:
        if x == 'A': a += 1
        elif x == 'C': c += 1
        elif x == 'G': g += 1
        elif x == 'U': u += 1
        yield a, c, g, u
        
def cum_count(s):
    '''Cumulative A,C,G,T count lists of the RNA string s.'''
    return zip(*list(_cum_count(s)))
    
class PerfectMatching(object):
    '''Computes # of perfect matching modulo r using DP, memoization.'''
    def __init__(self, r):
        self._c, self._r = {}, r  # _c = memo array

    def _k_range(self, s):
        s0c = ro.RNA_COMPLEMENT[s[0]]
        n = len(s) / 2
        fA, fC, fG, fU = cum_count(s)  # Cumulative letter counts
        for k in xrange(n):
            k1, k2 = 2 * k, 2 * k + 1
            if s[2 * k + 1] == s0c \
            and (k == 0 or (fA[k1] - fA[0] == fU[k1] - fU[0] and fG[k1] - fG[0] == fC[k1] - fC[0])) \
            and (k == n - 1 or (fA[-1] - fA[k2] == fU[-1] - fU[k2] and fG[-1] - fG[k2] == fC[-1] - fC[k2])):
                yield k
                     
    def c(self, s):
        '''Returns the number of perfect matching for the binary tuple s.'''
        if not s in self._c:
            # print 'c[%s]' % (ro.join_list(s))
            n, r = len(s) / 2, self._r
            if n == 0: self._c[s] = 1
            else:
                K = list(self._k_range(s)) 
                a = ro.sum_mod(((self.c(s[1:2 * k + 1]) * self.c(s[2 * k + 2:]) % r) for k in K), r)
                self._c[s] = a
        return self._c[s]

def num_perfect_matching(s, r=1000000L):
    '''Returns the number of perfect matching in the RNA string s, modulo r.'''
    return PerfectMatching(r).c(s)

def cat(f):
    '''Main driver to solve this problem.'''
    return num_perfect_matching(ro.read_fafsa(f))

if __name__ == "__main__":
    # TODO: convert to a test suite
    print num_perfect_matching('AUAUAU')  # 5
    print num_perfect_matching('AUGC')  # 1
    print num_perfect_matching('AGUC')  # 0
    
    print cat('rosalind_cat_sample.dat')
    print cat('rosalind_cat.dat')
