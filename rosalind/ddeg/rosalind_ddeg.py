'''
============================================================
In an undirected graph, the degree d(u) of a vertex u is the
number of neighbors u has, or equivalently, the number of
edges incident upon it.

Given: A simple graph with n<=10**3 vertices in the edge
list format.

Return: An array D[1..n] where D[i] is the ddegree of vertex
i.

See Figure 3 for visual example from the sample dataset.
============================================================
'''
import rosalind.rosutil as ro, rosalind.rosgraph as rg

def double_deg(g):
    '''Return the double-degree array of an undirected graph g.'''
    return [sum(g.degree(v) for v in g.neighbors_iter(u)) for u in xrange(1, g.number_of_nodes()+1)] 

def ddeg(f):
    '''Main driver to solve this problem.'''
    return ro.join_list(double_deg(rg.read_edgelist(ro.iterlines(f))))

if __name__ == "__main__":
    print ddeg('rosalind_ddeg_sample.dat')
    print ddeg('rosalind_ddeg.dat')
