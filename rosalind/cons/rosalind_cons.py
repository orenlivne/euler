'''
============================================================
http://rosalind.info/problems/cons

A matrix is a rectangular table of values divided into rows and columns. An mxn matrix has m rows and n columns. Given a matrix A, we write Ai,j to indicate the value found at the intersection of row i and column j.

Say that we have a collection of DNA strings, all having the same length n. Their profile matrix is a 4xn matrix P in which P1,j represents the number of times that 'A' occurs in the jth position of one of the strings, P2,j represents the number of times that C occurs in the jth position, and so on (see below).

A consensus string c is a string of length n formed from our collection by taking the most common symbol at each position; the jth symbol of c therefore corresponds to the symbol having the maximum value in the j-th column of the profile matrix. Of course, there may be more than one most common symbol, leading to multiple possible consensus strings.

A T C C A G C T
G G G C A A C T
A T G G A T C T
DNA Strings    A A G C A A C C
T T G G A A C T
A T G C C A T T
A T G G C A C T
A   5 1 0 0 5 5 0 0
Profile    C   0 0 1 4 2 0 6 1
G   1 1 6 3 0 1 0 0
T   1 5 0 0 0 1 1 6
Consensus    A T G C A A C T
Given: A collection of at most 10 DNA strings of equal length (at most 1 kbp) in FASTA format.

Return: A consensus string and profile matrix for the collection. (If several possible consensus strings exist, then you may return any one of them.)
============================================================
'''
from collections import Counter
from rosalind.rosutil import fafsa_itervalues

def consensus(G):
    g = G.next()
    count = [Counter({x:1}) for x in g]
    alphabet = set(g)
    try:
        while True:
            for i, x in enumerate(G.next()): 
                count[i][x] += 1
                alphabet.add(x)
    except StopIteration: pass
    return count, ''.join(c.most_common(1)[0][0] for c in count), alphabet

def print_cons(count, consensus, alphabet):
    print consensus
    for x in sorted(alphabet):
        print '%s:' % (x,),
        for i in xrange(len(count)): print ' %d' % (count[i][x],),
        print ''

def cons(file_name):
    print_cons(*consensus(fafsa_itervalues(file_name)))
    
if __name__ == "__main__":
    cons('rosalind_cons_sample.dat')
    cons('rosalind_cons.dat')    
