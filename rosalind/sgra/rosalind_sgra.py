'''
============================================================
http://rosalind.info/problems/sgra

For a weighted alphabet A and a collection L of positive real numbers, the spectrum graph of L is a digraph constructed in the following way. First, create a node for every real number in L. Then, connect a pair of nodes with a directed edge (u,v) if v>u and v-u is equal to the weight of a single symbol in A. We may then label the edge with this symbol.

In this problem, we say that a weighted string s=s1s2...sn matches L if there is some increasing sequence of positive real numbers (w1,w2,...,wn+1) in L such that w(s1)=w2-w1, w(s2)=w3-w2, ..., and w(sn)=wn+1-wn.

Given: A list L (of length at most 100) containing positive real numbers.

Return: The longest protein string that matches the spectrum graph of L (if multiple solutions exist, you may output any one of them). Consult the monoisotopic mass table.
============================================================
'''
import rosalind.rosutil as ro, numpy as np, networkx as nx

def longest_protein_from_spectrum_graph(a):
    '''Main driver to solve this problem.'''
    g = nx.DiGraph()
    g.add_weighted_edges_from((u, v, r) for u, v, r in ((i, j, ro.aa_of_mass_exact(v - u)) for i, u in enumerate(a) for j, v in enumerate(a) if v > u) if r)
    i, l = nx.topological_sort(g), np.zeros((len(a),), dtype=int)
    for u in i:  l[u] = 0 if g.in_degree(u) == 0 else (max(l[v] for v in g.predecessors_iter(u)) + 1)
    u = np.argmax(l)
    d, s = l[u], ''
    for _ in xrange(d):
        v = max((l[v], v) for v in g.predecessors_iter(u))[1]
        s, u, d = g[v][u]['weight'] + s, v, l[v]
    return s

def sgra(f):
    '''Main driver to solve this problem.'''
    return longest_protein_from_spectrum_graph(np.loadtxt(f))

if __name__ == "__main__":
    print sgra('rosalind_sgra_sample.dat')
    print sgra('rosalind_sgra.dat')
