'''
============================================================
Graph theory utilities.

Created on January 21, 2014
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
import rosalind.rosutil as ro, networkx as nx

def read_edgelist(edgelist, create_using=None):
    '''Convert edge list format into a networkx graph object.'''
    g = nx.convert._prep_create_using(create_using)
    i = iter(edgelist)
    n, m = ro.to_int_list(i.next())
    g.add_nodes_from(xrange(1, n + 1))
    g.add_edges_from((int(x[0]), int(x[1])) for x in (x.split() for x in i))
    if g.number_of_edges() != m: raise ValueError('Problem reading edge list: wrong number of edges')
    return g
