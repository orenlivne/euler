'''
============================================================
http://rosalind.info/problems/mrep

A maximal repeat of a string s is a repeated substring t of s having two occurrences t1 and t2 such that t1 and t2 cannot be extended by one symbol in either direction in s and still agree.

For example, "AG" is a maximal repeat in "TAGTTAGCGAGA" because even though the first two occurrences of "AG" can be extended left into "TAG", the first and third occurrences differ on both sides of the repeat; thus, we conclude that "AG" is a maximal repeat. Note that "TAG" is also a maximal repeat of "TAGTTAGCGAGA", since its only two occurrences do not still match if we extend them in either direction.

Given: A DNA string s of length at most 1 kbp.

Return: A list containing all maximal repeats of s having length at least 20.
============================================================
'''
# Going for a simpler O(n^2) solution than more efficient algorithms such as
# http://ab.inf.uni-tuebingen.de/teaching/ss07/albi2/script/suffixtrees_14May2007.pdf 
import rosalind.rosutil as ro, rosmatch as rm

def mrep(f):
    '''Main driver to solve this problem.'''
    s = ro.read_str(f)
    for r in maximal_prefixes(s, 20): print r

def maximal_prefixes(s, min_length):
    '''Generate all maximal prefixes in s of legnth >= min_length.''' 
    ss = rm.EMPTY_STRING + s
    prefixes = ro.ALPHABET + rm.EMPTY_STRING
    num_prefixes = lambda r: sum(1 for a in prefixes if ss.find(a + r) != -1)  # @UnusedVariable
    t = rm.suffix_tree(s)
    g = t._g
    return (r for r in (t.prefix_of_node(u) for u in g if g.out_degree(u) > 0)
                        if len(r) >= min_length and num_prefixes(r) >= 2)

if __name__ == "__main__":
    #mrep('rosalind_mrep_sample.dat')
    mrep('rosalind_mrep.dat')
