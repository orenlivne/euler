'''
============================================================
http://rosalind.info/problems/eubt

Recall the definition of Newick format from "Distances in Trees"
as a way of encoding trees. See Figure 1 for an example of Newick format applied to an unrooted binary tree whose five leaves are labeled (note that the same tree can have multiple Newick representations).

Given: A collection of species names representing n taxa.

Return: A list containing all unrooted binary trees whose leaves are these n taxa. Trees should be given in Newick format, with one tree on each line; the order of the trees is unimportant.
============================================================
'''
import rosalind.rosutil as ro, networkx as nx

def deep_copy(g):
    h = nx.DiGraph()
    h.add_nodes_from(g.nodes_iter())
    h.add_edges_from(g.edges_iter())
    return h

def add_leaf(g, (u, v), leaf):
    g = deep_copy(g)
    w = g.number_of_nodes() + 1
    g.remove_edge(u, v)
    g.add_edges_from([(u, w), (w, leaf), (w, v)])
    return g

def _enumerate_trees(g, labels, num_leaves):
    #print '  ' * (num_leaves - 3), 'g', g.edges()
    if num_leaves == len(labels): yield g
    else:
        for u, v in g.edges_iter():
            #print '  ' * (num_leaves - 2), 'edge', u, '->', v
            for h in _enumerate_trees(add_leaf(g, (u, v), labels[num_leaves]), labels, num_leaves + 1): yield h

def enumerate_trees(labels):  # len(labels) must be >= 3
    return  _enumerate_trees(nx.from_edgelist(((0, x) for x in labels[:3]), nx.DiGraph()), labels, 3)
    
def _to_newick_str(g, node):
    is_leaf = g.out_degree(node) == 0
    return '%s' % (node,) if is_leaf else ('(' + ','.join(_to_newick_str(g, child) for child in g.successors(node)) + ')')

def to_newick_str(g, root=0):  # 0 assumed to be the root
    return _to_newick_str(g, root) + ';'

def eubt(f):
    '''Main driver to solve this problem.'''
    labels = ro.read_str(f).split()
    for g in enumerate_trees(labels): print to_newick_str(g)

if __name__ == "__main__":
    #eubt('rosalind_eubt_sample.dat')
    eubt('rosalind_eubt.dat')
