'''
============================================================
http://rosalind.info/problems/tree

Given: A positive integer n (n<=1000) and an adjacency list corresponding to a graph on n nodes that contains no cycles.

Return: The minimum number of edges that can be added to the graph to produce a tree.
============================================================
'''
import networkx as nx, itertools as it

def read_adjlist(file_name):
    g = nx.Graph()
    g.add_nodes_from(xrange(1, int(open(file_name, 'rb').next()) + 1))
    g.add_edges_from(map(int, x.strip().split()) for x in it.islice(open(file_name, 'rb'), 1, None))
    return g

def tree(file_name):
    return len(nx.connected_components(read_adjlist(file_name))) - 1
    
if __name__ == "__main__":
    #print tree('rosalind_tree_sample.dat')
    print tree('rosalind_tree.dat')
    