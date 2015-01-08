'''
============================================================
http://rosalind.info/problems/trie

Given a collection of strings, their trie (often pronounced "try" to avoid ambiguity with the general term tree) is a rooted tree formed as follows. For every unique first symbol in the strings, an edge is formed connecting the root to a new vertex. This symbol is then used to label the edge.

We may then iterate the process by moving down one level as follows. Say that an edge connecting the root to a node v is labeled with 'A'; then we delete the first symbol from every string in the collection beginning with 'A' and then treat v as our root. We apply this process to all nodes that are adjacent to the root, and then we move down another level and continue. See Figure 1 for an example of a trie.

As a result of this method of construction, the symbols along the edges of any path in the trie from the root to a leaf will spell out a unique string from the collection, as long as no string is a prefix of another in the collection (this would cause the first string to be encoded as a path terminating at an internal node).

Given: A list of at most 100 DNA strings of length at most 100 bp, none of which is a prefix of another.

Return: The adjacency list corresponding to the trie T for these patterns, in the following format. If T has n nodes, first label the root with 1 and then label the remaining nodes with the integers 2 through n in any order you like. Each edge of the adjacency list of T will be encoded by a triple containing the integer representing the edge's parent node, followed by the integer representing the edge's child node, and finally the symbol labeling the edge.
============================================================
'''
import rosalind.rosutil as ro, networkx as nx

class Trie(object):
    '''A string collection\'s trie data structure.'''
    _ROOT = 1
    
    def __init__(self, s=None):
        '''Initialize an empty trie.'''
        self._count = Trie._ROOT
        self._g = nx.DiGraph()
        self._g.add_node(self._count)
        if s is not None:
            for x in s: self.add(x)
            
    def write_edgelist(self):
        '''Write the formatted edge list.'''
        for u, u_nbhrs in self._g.adjacency_iter():
            for v, e_attr in u_nbhrs.items(): print '%d %d %s' % (u, v, e_attr['weight'])
    
    def add(self, s):
        '''Add the string s to the trie.'''
        node, i = Trie._ROOT, 0
        #print 'Adding s', s
        for x in s:  # Continue along an existing branch until s becomes different
            node_new = self._find_edge(node, x)
            #print 'x', x, 'node_new', node_new
            if node_new: node = node_new
            else: break
            i += 1
        if i == len(s): raise ValueError('s is a suffix of another string in the trie')
        #print 'Branching at i', i
        for x in s[i:]:  # Form a new branch
            self._count += 1
            #print 'x', x, 'new edge: %d -> %d' % (node, self._count) 
            self._g.add_edge(node, self._count, weight=x)
            node = self._count
    
    def _find_edge(self, node, value):
        '''Return the child node of node whose edge value is value, if found; otherwise, return None.'''
        children = [k for k, v in self._g[node].iteritems() if v['weight'] == value]
        return children[0] if children else None 

def trie(f):
    '''Main driver to solve this problem.'''
    Trie(ro.iterlines(f)).write_edgelist()

if __name__ == "__main__":
    #trie('rosalind_trie_sample.dat')
    trie('rosalind_trie.dat')
