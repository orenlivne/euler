'''
============================================================
http://rosalind.info/problems/ling

Given a length n string s formed over an alphabet A of size a, let the "substring count" sub(s) denote the total number of distinct substrings of s. Furthermore, let the "maximum substring count" m(a,n) denote the maximum number of distinct substrings that could appear in a string of length n formed over A.

The linguistic complexity of s (written lc(s)) is equal to sub(s)m(a,n); in other words, lc(s) represents the percentage of observed substrings of s to the total number that are theoretically possible. Note that 0<lc(s)<1, with smaller values of lc(s) indicating that s is more repetitive.

As an example, consider the DNA string (a=4) s=ATTTGGATT. In the following table, we demonstrate that lc(s)=3540=0.875 by considering the number of observed and possible length k substrings of s, which are denoted by subk(s) and m(a,k,n), respectively. (Observe that m(a,n)=SUM nk=1m(a,k,n)=40 and sub(s)=SUM nk=1subk(s)=35.)

k    subk(s)    m(a,k,n)
1     3     4
2     5     8
3     6     7
4     6     6
5     5     5
6     4     4
7     3     3
8     2     2
9     1     1
Total     35     40
Given: A DNA string s of length at most 100 kbp.

Return: The linguistic complexity lc(s).
============================================================
'''
from __future__ import division
from suffix_tree import SuffixTree
import rosalind.rosutil as ro

def ling_complexity(s):
    t = SuffixTree(s)
    subs = sum(len(x.edgeLabel.rstrip('$')) for x in t.postOrderNodes)
    m = (len(s) - 1) * len(s) / 2 + 4
    return subs / m

def ling(f):
    '''Main driver to solve this problem.'''
    return ling_complexity(ro.read_str(f))

if __name__ == "__main__":
    print ling('rosalind_ling_sample.dat')
    print ling('rosalind_ling.dat')
