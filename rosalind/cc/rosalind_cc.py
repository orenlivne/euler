'''
============================================================
http://rosalind.info/problems/cc

Given: A list of n species (n<=80) and an n-column character table C in which the jth column denotes the jth species.

Return: An unrooted binary tree in Newick format that models C.
============================================================
'''
import rosalind.rosutil as ro

def read_graph(lines):
    # Returns a graph from a edge info lines.
    
    # Read the header n, m.
    line = next(lines)
    items = line.split()
    if len(items) != 2: raise ValueError('Invalid header line: ' + line)
    n = int(items[0])
    items = line.split()
    g = dict((u, set()) for u in xrange(1, n+1))
    for line in lines:
        items = line.split()
        if len(items) != 2: raise ValueError('Invalid edge line: ' + line)
        u, v = map(int, items)
        g[u].add(v)
        g[v].add(u)
    return g

def dfs(g, u):
    # Returns the set of nodes connected to u in g.
    visited, stack = set(), [u]
    while stack:
        v = stack.pop()
        if not v in visited:
            visited.add(v)
            for w in g[v]: stack.append(w)
    return visited
    
def connected_components(g):
    # Returns the list of connected components of g. Each component is a set of
    # node labels.
    if not g: return [] # Optimization for empty graph and assures that next(iter()) doesn't raise an exception below.
    unvisited = set(g.keys())
    components = []
    while unvisited:
        c = dfs(g, next(iter(unvisited))) # Pick a random unvisited node and run DFS
        components.append(c)
        unvisited -= c
    return components

def cc(f):
    '''Main driver to solve this problem.'''
    return len(connected_components(read_graph(ro.iterlines(f))))

if __name__ == "__main__":
    #print cc('rosalind_cc_sample.dat')
    print cc('rosalind_cc.dat')
