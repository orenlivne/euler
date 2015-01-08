'''
============================================================
In an undirected graph, the degree d(u) of a vertex u is the
number of neighbors u has, or equivalently, the number of
edges incident upon it.

Given: A simple graph with n<=10**3 vertices in the edge
list format.

Return: An array D[1..n] where D[i] is the degree of vertex
i.

See Figure 3 for visual example from the sample dataset.
============================================================
'''
import rosalind.rosutil as ro, rosalind.rosgraph as rg

def deg(f):
    '''Main driver to solve this problem.'''
    g = rg.read_edgelist(ro.iterlines(f))
    return ' '.join(map(str, (g.degree(u) for u in xrange(1, g.number_of_nodes() + 1))))

if __name__ == "__main__":
    print deg('rosalind_deg_sample.dat')
    print deg('rosalind_deg.dat')
