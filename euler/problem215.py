'''
============================================================
http://projecteuler.net/problem=215

Consider the problem of building a wall out of 2x1 and 3x1 bricks (horizontalvertical dimensions) such that, for extra strength, the gaps between horizontally-adjacent bricks never line up in consecutive layers, i.e. never form a "running crack".
For example, the following 9x3 wall is not acceptable due to the running crack shown in red:

There are eight ways of forming a crack-free 9x3 wall, written W(9,3) = 8.

Calculate W(32,10).
============================================================
'''
import networkx as nx
from numpy import cumsum, ones
from itertools import islice

def states(n):
    '''Return a list of all options to build a single layer of length n, n>=1. Options (states)
    are encoded as strings of ''2'' and ''3'' representing the block sequence.'''
    s1 = []
    if n == 1: return s1  # Initial conditions
    s2 = ['2']
    if n == 2: return s2  # Initial conditions
    s3 = ['3']
    if n == 3: return s3  # Initial conditions
    for _ in xrange(4, n + 1):
        s4 = [x + '3' for x in s1] + [x + '2' for x in s2]  # Dynamic programming: n in terms of n-3, n-2
        s1, s2, s3 = s2, s3, s4  # Advance iterates
    return s4

adjacency_matrix = lambda states: nx.to_scipy_sparse_matrix(nx.from_edgelist((s, t) for s in states for t in states if
                                                                            not set(cumsum(map(int, s))[:-1]) & set(cumsum(map(int, t))[:-1])), dtype=int)

def W(n):
    '''An iterator of W(n,k), k=1,2,... .'''
    S = states(n)
    print 'nodes', len(S)
    A, x = adjacency_matrix(S), ones((len(S),), dtype=int)
    print 'edges', A.nnz
    while True:
        print x
        yield sum(x)
        x = A * x

if __name__ == "__main__":
    print islice(W(9), 2, 3).next()
    print islice(W(32), 9, 10).next()
