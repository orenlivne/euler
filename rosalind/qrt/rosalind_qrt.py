'''
============================================================
http://rosalind.info/problems/qrt

A partial split of a set S of n taxa models a partial
character and is denoted by A|B, where A and B are still the
two disjoint subsets of taxa divided by the character.
Unlike in the case of splits, we do not necessarily require
that AUB=S; (AUB)c corresponds to those taxa for which we
lack conclusive evidence regarding the character.

We can assemble a collection of partial characters into a
generalized partial character table C in which the symbol
x is placed in Ci,j if we do not have conclusive evidence
regarding the jth taxon with respect to the ith partial
character.

A quartet is a partial split A|B in which both A and B
contain precisely two elements. For the sake of simplicity,
we often will consider quartets instead of partial
characters. We say that a quartet A|B is inferred from a
partial split C|D if A SUBSETEQC and B SUBSETEQD (or
equivalently A SUBSETEQD and B SUBSETEQC). For example,
{1,3}|{2,4} and {3,5}|{2,4} can be inferred from
{1,3,5}|{2,4}.

Given: A partial character table C.

Return: The collection of all quartets that can be inferred
from the splits corresponding to the underlying characters
of C.
============================================================
'''
import rosalind.rosutil as ro, itertools as it, numpy as np

def quartets(s, lines):
    '''Returns the set of distinct quartets from taxa name array s and character array lines lines.'''
    Q = set()
    for line in lines:
        l = np.array([x for x in line])
        c, d = np.where(l == '0')[0], np.where(l == '1')[0]
        if len(c) >= 2 and len(d) >= 2:
            for q in it.product(it.combinations(c, 2), it.combinations(d, 2)):
                Q.add(q if q[0] < q[1] else (q[1], q[0]))
    return Q

def qrt(f):
    '''Main driver to solve this problem.'''
    lines = ro.iterlines(f)
    s = next(lines).split()
    for q in quartets(s, lines): print '{%s, %s} {%s, %s}' % tuple(map(s.__getitem__, sum(q, ())))

if __name__ == "__main__":
    # qrt('rosalind_qrt_sample.dat')
    qrt('rosalind_qrt.dat')
