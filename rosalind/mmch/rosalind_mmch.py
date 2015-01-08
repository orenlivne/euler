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
from __future__ import division
import rosalind.rosutil as ro
# from scipy import misc
from collections import Counter
from scipy.misc import factorial

'''Number of ways to choose k objects out of n where order matters.'''
# perm = lambda n, k : long(misc.factorial(k)) * misc.comb(n, k, exact=True)
perm = lambda n, k : reduce(lambda x, y: x * y, xrange(n - k + 1, n + 1L), 1L)
#perm = lambda n, k : factorial(n) // factorial(n - k)

'''Number of A-U (or C-G) matching in an RNA string.'''
num_matching = lambda a, b: perm(max(a, b), min(a, b))

def num_max_matching(s):
    c = Counter(s)
    return long(num_matching(c['A'], c['U']) * num_matching(c['C'], c['G']))

def num_max_matching_luiz(seq):
    '''For validation, solution from https://github.com/luizirber/rosalind/blob/master/mmch.py'''
    min_gc, max_gc = sorted([seq.count('G'), seq.count('C')])
    min_au, max_au = sorted([seq.count('A'), seq.count('U')])
    print min_gc, max_gc
    print min_au, max_au
    print perm(max_gc, min_gc)
    print perm(max_au, min_au)
    print '%.16f' % (factorial(max_gc) // factorial(max_gc - min_gc),)
    print '%.16f' % (factorial(max_au) // factorial(max_au - min_au),)
    return (factorial(max_gc) // factorial(max_gc - min_gc) * 
            factorial(max_au) // factorial(max_au - min_au))
    
def mmch(f):
    s = ro.fafsa_values(f)[0]
    #return num_max_matching(s), long(num_max_matching_luiz(s))
    print s
    print len(s)
    return num_max_matching(s), long(num_max_matching_luiz(s))

if __name__ == "__main__":
    print mmch('rosalind_mmch_sample.dat')
    print mmch('rosalind_mmch.dat')
