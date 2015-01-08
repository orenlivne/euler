'''
============================================================
My Rosalind pattern matching library.

Created on Dec 26, 2013
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
import networkx as nx, itertools as it, numpy as np

'''Useful for boundary cases.'''
EMPTY_STRING = '$'

def suffixes(s):
    '''Return the list of all suffixes s[k:] of a string s, k=0,...,len(s).'''
    return [s[k:] for k in xrange(len(s) + 1)]
 
def longest_common_substring(s, i, j):
    '''Return the longest common substring length in s[i:], s[j:].'''
    k, max_k = 0, len(s) - max(i, j)
    while k < max_k and s[i + k] == s[j + k]: k += 1
    return k

def longest_repeated_substring(s):
    '''Return the longest repeated substring of s - fast implementation using a suffix array.'''
    n = len(s)
    if n == 1: return ''  # Treat boundary case of one-character string, no non-trivial repeated substring

    suffix = suffix_array(s)
    # Find max longest_common_substring of adjacent elements in suffix array
    k, i = max((longest_common_substring(s, suffix[i], suffix[i + 1]), suffix[i]) for i in xrange(n - 1))
    return s[i:i + k]

def suffix_array(s):
    '''Return the sorted suffix array indices of a string s.'''
    n = len(s)
    # Comparator; nested function because it uses s
    def compare_suffixes(i, j):
        if i == j: return 0
        k = longest_common_substring(s, i, j)
        max_k = n - max(i, j)
        if k == max_k: return -1 if i > j else 1  # Both substrings equal to end of string but the one with the largest index is shorter
        else: return -1 if s[i + k] < s[j + k] else 1  # Unequal at a character before end of string
    return np.array(sorted(xrange(n), cmp=compare_suffixes))
        
def suffix_tree(s, debug=False):
    '''Return the suffix tree of the string s.'''
    return SuffixTreeBuilder(s, debug=debug).build()

def suffix_tree_weights(s):
    '''A generator of the suffix tree edge weights of the string s.'''
    return suffix_tree(s).weights()

####################################################################################
class SuffixTree(object):
    '''Suffix tree data structure.'''
    
    def __init__(self, s, edge_list):
        '''Initialize a suffix tree for a string s. edge_list is the tree's edge list.'''
        self._s = s
        self._g = nx.DiGraph()
        self._g.add_weighted_edges_from(edge_list)
        
    def max_repeated(self, k):
        '''Return the node of maximum prefix length with #leaves >= k under it.'''
        g = self._g
        num_leaves = [0] * g.number_of_nodes()
        for node in nx.dfs_postorder_nodes(g): num_leaves[node] = 1 if g.out_degree(node) == 0 else sum(num_leaves[child] for child in g.successors_iter(node))
        
        prefix_len = np.zeros((g.number_of_nodes(),), dtype=int)
        for node in nx.dfs_preorder_nodes(g):
            node_prefix_len = prefix_len[node]
            for child, e_attr in g[node].iteritems(): prefix_len[child] = node_prefix_len + e_attr['weight'][1]

        try: return max(it.ifilter(lambda x: x[0][1] >= k, ((v, k) for k, v in enumerate(zip(prefix_len, num_leaves)))))[1]
        except ValueError: return None
    
    def prefix_of_node(self, node):
        '''Return the s-prefix corresponding to the path from the root to node node.'''
        g, s, prefix = self._g, self._s, ''
        while True:
            parents = g.predecessors(node)
            if not parents: return prefix
            else:
                parent = parents[0]
                start, l = g[parent][node]['weight']
                prefix = s[start:start + l] + prefix
                node = parent
        
    def weights(self):
        '''Generate the list of strings serving as edge weights in the suffix tree to the output stream out.'''
        s = self._s
        for _, nbrsdict in self._g.adjacency_iter():
            for _, e_attr in nbrsdict.items():
                start, l = e_attr['weight']
                yield s[start:start + l]
                
    def print_tree(self):
        '''Print node and edge information.'''
        p = dict((u, self.prefix_of_node(u)) for u in self._g)    
        for u, nbrsdict in self._g.adjacency_iter():
            print 'u', u, '\'%s\'' % (p[u],)
            for v, e_attr in nbrsdict.items():
                start, l = e_attr['weight']
                print '\t', 'v', v, (start, l), self._s[start:start + l], '\'%s\'' % (p[v],)

####################################################################################
class SuffixTreeBuilder(object):  # 
    '''A SuffixTree builder. Has ~O(n log n) complexity (depends on the data - brings common
    suffixes together based on an longest common prefix function that may take O(1) time or longer).'''
    
    def __init__(self, s, debug=False):
        '''Initialize a builder for the string s.'''
        n = len(s)
        self._s = s
        self._n = n
        self._suffix = suffix_array(s)
        self._count = 0
        self._node = np.zeros((n,), dtype=int)        
        self._index = np.zeros((n,), dtype=int)
        self._debug = debug
        if debug:
            print 's', s
            print sorted(s[k:] for k in xrange(len(s)))

        
    def build(self):
        '''Main call to build the suffix tree.'''
        return SuffixTree(self._s, self._edge_list())
    
    def _edge_list(self):
        '''A Generator of suffix tree edges.'''
        while self._suffix.size:
            for e in self._advance_groups(): yield e
    
    def _advance_groups(self, debug=False):
        '''Perform a single round through the remaining, non-exhausted suffixes.'''
        s, n, f, nf, start = self._s, self._n, self._suffix, len(self._suffix), 0
        debug = self._debug
        if debug:
            print '-' * 80
            print 'suffix', self._suffix
            print 'index ', self._index
            print 'node  ', self._node
        while start < nf:
            stop = self._group_stop(start)
            if debug: print 'Group: start', start, 'stop', stop
            k_old = self._index[start]
            k_new = self._common_prefix_index(start, stop)
            self._count += 1
            l = k_new - k_old
            f_start = f[start]
            if debug:
                print 'k_old', k_old, 'k_new', k_new, 'f[start]', f[start]
                print 'edge', self._node[start], self._count, (f_start + k_old, l), s[f_start + k_old:f_start + k_new]
            yield self._node[start], self._count, (f_start + k_old, l)
            self._index[start:stop] = k_new
            self._node[start:stop] = self._count
            start = stop
            if debug: print
 
        if debug:
            print 'suffix', self._suffix
            print 'index ', self._index
            print 'node  ', self._node
        # Remove exhausted suffixes that have just become leaves from active lists
        remaining = np.where(self._index < n - self._suffix)
        if debug: print 'remaining', np.where(remaining)[0]
        self._index, self._suffix, self._node = self._index[remaining], self._suffix[remaining], self._node[remaining]  
    
    def _group_stop(self, start):
        '''Return the stop index of the suffix group starting with start. Groups have a common
        self._node values and the same prefix up to and including self._index[start].'''
        s, nf, f, node = self._s, len(self._suffix), self._suffix, self._node
        k = self._index[start]
        node_start, s_start = node[start], s[f[start] + k]
        try: return it.dropwhile(lambda i: node[i] == node_start and s[f[i] + k] == s_start, xrange(start + 1, nf)).next()
        except StopIteration: return nf
        
    def _common_prefix_index(self, start, stop):
        '''Return the largest index for which the group start:stop has a common prefix.'''
        s, n, f = self._s, self._n, self._suffix
        try: return it.dropwhile(lambda k: all(f[i] + k < n for i in xrange(start, stop))
                                 and all(s[f[i] + k] == s[f[i + 1] + k] for i in xrange(start, stop - 1)),
                                 xrange(self._index[start] + 1, n)).next()
        except StopIteration: return n
            
if __name__ == '__main__':
    # test_binary_search_tree()
    pass
