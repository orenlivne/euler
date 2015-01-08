'''
============================================================
http://rosalind.info/problems/lexv

Given: A collection of at most 12 symbols defining an ordered alphabet A, and a positive integer n (n<=4).
Return:  All strings of length at most n formed from A, ordered lexicographically.

(Note: As in "Enumerating k-mers Lexicographically", alphabet order is based on the order in which the
symbols are given.)
============================================================
'''
import rosalind.rosutil as ro, itertools as it

def lexv(f):
    lines = list(ro.read_lines(f))
    a, n = lines[0].split(), int(lines[1])
    for x in sorted(it.chain.from_iterable(it.product(xrange(len(a)), repeat=r) for r in xrange(1, n + 1))):
        print ''.join(a[i] for i in x)

if __name__ == "__main__":
    # lexv('rosalind_lexu_sample.dat')
    lexv('rosalind_lexu.dat')
    
