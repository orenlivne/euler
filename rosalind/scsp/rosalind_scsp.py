'''
============================================================
http://rosalind.info/problems/scsp

A string s is a supersequence of another string t if s contains t as a subsequence.

A common supersequence of strings s and t is a string that serves as a supersequence of both s and t. For example, "GACCTAGGAACTC" serves as a common supersequence of "ACGTC" and "ATAT". A shortest common supersequence of s and t is a supersequence for which there does not exist a shorter common supersequence. Continuing our example, "ACGTACT" is a shortest common supersequence of "ACGTC" and "ATAT".

Given: Two DNA strings s and t.

Return: A shortest common supersequence of s and t. If multiple solutions exist, you may output any one.
============================================================
'''
import rosalind.rosutil as ro, rosalind.rosalign as ra

def shortest_supersequence(s, t):
    '''Return the shortest supersequence of s,t.'''
    gap_symbol = '-'
    _, (ss, tt) = ra.optimal_alignment(s, t, ra.FixedCost(-1, ra.MINUS_INFINITY), -1, -1, gap_symbol=gap_symbol)
    return ''.join((a if a != gap_symbol else b) for a, b in zip(ss, tt)) 

def scsp(f):
    '''Main driver to solve this problem.'''
    return shortest_supersequence(*ro.read_lines(f))

if __name__ == "__main__":
    print scsp('rosalind_scsp_sample.dat')
    print scsp('rosalind_scsp.dat')
