'''
============================================================
http://projecteuler.net/problem=209

A k-input binary truth table is a map from k input bits (binary digits, 0 [false] or 1 [true]) to 1 output bit. For example, the 2-input binary truth tables for the logical AND and XOR functions are:

x    y    x AND y
0    0    0
0    1    0
1    0    0
1    1    1
x    y    x XOR y
0    0    0
0    1    1
1    0    1
1    1    0

How many 6-input binary truth tables, tau, satisfy the formula

tau(a, b, c, d, e, f) AND tau(b, c, d, e, f, a XOR (b AND c)) = 0

for all 6-bit inputs (a, b, c, d, e, f)?
============================================================
'''
import networkx as nx
from numpy import prod
from itertools import islice
#import matplotlib.pylab as P
from problem002 import fibonacci

'''Cache enough Fibonacci numbers.'''
MAX_RING_SIZE = 50
F = list(islice(fibonacci(1, 2), MAX_RING_SIZE + 1))

'''Check if a connected graph is a ring.'''
is_ring = lambda g: g.number_of_nodes() >= 3 and all(g.degree(x) == 2 for x in g.nodes_iter())

def is_chain(g):
    '''Check if a connected graph is a chain.'''
    if g.number_of_nodes() == 1: return True  # Lone node is a chain
    degree1_count = 0
    for d in g.degree().itervalues():
        if d > 2: return False
        if d == 1:
            degree1_count += 1
            if degree1_count > 2: return False
    return degree1_count == 2

def num_colorings2_component(g):
    '''Number of 2-color colorings (W or B) of a chain or ring graph, where no two adjacent nodes are
    colored with B.'''
    n = g.number_of_nodes()
    if n == 1: return 1
    elif is_chain(g): return F[n]
    elif is_ring(g): return F[n - 1] + F[n - 3]
    else: raise ValueError('Cannot determine #colorings for component')
    
'''Number of 2-color colorings (W or B) of graph whose components are chains or rings,
where no two adjacent nodes are colored with B.'''
num_colorings2 = lambda g: prod(map(num_colorings2_component, nx.connected_component_subgraphs(g)))

'''Last bit of the constraint transformation of a truth table row. n >= 3.'''
last_bit = lambda x, n: (x >> (n - 1)) ^ (((x >> (n - 2)) & 1) & ((x >> (n - 3)) & 1))

def constraint_graph(n):
    '''tau(A) AND tau(B) = 0 constraint graph for n-bit truth tables. n >= 3.'''
    last_digits = 2 ** (n - 1)
    g = nx.Graph()
    g.add_nodes_from(xrange(1 << n))
    g.add_edges_from((x, ((x % last_digits) << 1) + last_bit(x, n)) for x in xrange(1 << n))
    return g

if __name__ == "__main__":
    print num_colorings2(constraint_graph(6))
    
#----------------------
# def combinations(n, k):
#     """Return C(n, k), the number of combinations of k out of n."""
#     c = 1
#     k = min(k, n - k)
#     for i in range(1, k + 1):
#         c *= n - k + i
#         c //= i
#     return c
# 
# def cyclic_nonadjacent_combinations(n, k):
#     """Return the number of ways to choose k elements from a cycle of
#     length n, such that none of the chosen elements are adjacent.
# 
#     """
#     if n < 0 or k < 0 or n - k < k: return 0
#     if k == 0: return 1
#     return n * combinations(n - k - 1, k - 1) // k
# 
# def cyclic_nonadjacent_two_colourings(n):
#     """Return the number of ways to two-colour a cycle of length n such
#     that no black nodes are adjacent.
# 
#     """
#     return sum(cyclic_nonadjacent_combinations(n, k) for k in range(n // 2 + 1))
#print 'Theirs', [cyclic_nonadjacent_two_colourings(n) for n in (46, 6, 6, 3, 2, 1)]
