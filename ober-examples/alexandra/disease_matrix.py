#!/usr/bin/env python
'''
============================================================
Disease adjacency matrix from disease-(LD-block) edge list.
Reads from stdin in CSV format, writes to stdin in CSV
format.

Created on July 30, 2013
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
import util, networkx as nx, sys, numpy as np

sorted_pair = lambda a, b: (a, b) if a <= b else (b, a)

'''Main program'''
if __name__ == '__main__':
    in_file = sys.stdin
    delimiter = ','
    output_format = 'cytoscape'  # 'matrix'
    
    # Read disease-block list from a delimited text file (by default, a CSV)
    # Create a hash table of block-to-diseases
    h = util.mdict.from_items((j, i) for (i, j) in np.loadtxt(in_file, delimiter=delimiter, dtype=[('i', 'S50'), ('j', 'S50')]))
    
    # For each h-entry and each pair of diseases in the entry, increment the a-b weight in the
    # disease graph
    weighted_edgelist = util.occur_dict(sorted_pair(a, b) for diseases in h.itervalues() for a in diseases for b in diseases)
    g = nx.Graph()
    g.add_weighted_edges_from((i, j, w) for (i, j), w in weighted_edgelist.iteritems())

    # Convert to adjacency matrix and output in CSV format 
    diseases = g.nodes()
    
    if output_format == 'matrix':
        print delimiter.join(diseases)
        A = nx.to_numpy_matrix(g)
        for i in xrange(len(diseases)): print diseases[i] + delimiter + delimiter.join(str(x) for x in A[i, :].tolist()[0])
    elif output_format == 'cytoscape':
        print '\n'.join(delimiter.join([u, v, 'pp', 'TRUE', 'edge%05d' % (k,), str(d['weight'])]) for k, (u, v, d) in enumerate(g.edges_iter(data=True)))
