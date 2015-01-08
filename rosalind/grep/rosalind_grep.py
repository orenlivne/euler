'''
============================================================
http://rosalind.info/problems/grep

Recall that a directed cycle is a cycle in a directed graph in which the head of one edge is equal to the tail of the following edge.

In a de Bruijn graph of k-mers, a circular string s is
constructed from a directed cycle s1->s2->...->si->s1 is
given by s1+s2[k]+...+si-k[k]+si-k+1[k]. That is, because the
final k-1 symbols of s1 overlap with the first k-1 symbols of s2, we simply tack on the k-th symbol of s2 to s, then iterate the process.

For example, the circular string assembled from the cycle "AC" -> "CT" -> "TA" -> "AC" is simply (ACT). Note that this string only has length three because the 2-mers "wrap around" in the string.

If every k-mer in a collection of reads occurs as an edge in a de Bruijn graph cycle the same number of times as it appears in the reads, then we say that the cycle is "complete."

Given: A list Sk+1 of error-free DNA (k+1)-mers (k<=5) taken from the same strand of a circular chromosome (of length <=50).

Return: All circular strings assembled by complete cycles in the de Bruijn graph Bk of Sk+1. The strings may be given in any order, but each one should begin with the first (k+1)-mer provided in the input.
============================================================
'''
import rosalind.rosutil as ro, networkx as nx
from numpy.ma.testutils import assert_equal

'''de-Bruijn graph of a set of k-mers S coming from a single strand.'''
de_bruijn_graph_single_strand = lambda S: nx.from_edgelist(((r[:-1], r[1:]) for r in S), create_using=nx.MultiDiGraph())
'''Node to start Eulerian circuits at.'''
initial_node = lambda S: S[0][:-1]
'''Assemble string from a de-Bruijn graph cycle node list p.'''
assemble = lambda p: p[0] + ''.join(x[-1] for x in p[1:len(p) - len(p[0]) + 1])

# Gets hairy with self-loops and multi edges  
# def collapse(g, s):
#     '''Eliminate chains from g. s = initial node, don\'t collapse around it so that it stays the same.'''
#     while True:
#         # Find next node to eliminate. Could be more efficient if we selected a maximal independent set of such
#         try: u, v, w = next((u, v, w) for (u, v, w) in 
#                       ((next(g.predecessors_iter(u)), u, next(g.successors_iter(u))) 
#                        for u in (u for u in g if u != s and g.in_degree(u) == 1 and g.out_degree(u) == 1))
#                        if u != s)
#         except StopIteration: break
#         print 'Eliminating %s -> %s -> %s into %s -> %s' % (u, v, w, u[:-1] + v, w)
#         # Merge v into u
#         g.remove_node(v)
#         g.add_edge(u, w)
#         g = nx.relabel_nodes(g, {u: u[:-1] + v})
#         #print g.nodes()
#     return g

_EMPTY_LIST = []
def _eulerian_circuits(g, p, num_remaining_edges, debug=False):
    '''A helper method that performs a recursive DFS for Eulerian paths given a partial path p.'''
    u = p[-1]  # i = current node to start searching at
    if debug: print 'p', p, 'u', u, '#remaining edges', num_remaining_edges
    if u == p[0] and num_remaining_edges == 0:
        if debug: print 'Found path', p, 'assembled', assemble(p[:-1])
        yield assemble(p[:-1])
    else:
        n1 = num_remaining_edges - 1
        for v, edges in g[u].iteritems():
            unvisited_edges = [e for e, attr in edges.iteritems() if not attr['visited']] 
            if debug:
                print '\t', 'v', v, 'edges', edges
                print '\t\t', 'Edges to traverse', unvisited_edges
            # if len(unvisited_edges) >= 1: e = unvisited_edges[0]
            for e in ((unvisited_edges[0],) if unvisited_edges else _EMPTY_LIST):  # unvisited_edges:
                g[u][v][e]['visited'] = True
                p.append(v)
                for x in _eulerian_circuits(g, p, n1, debug=debug): yield x
                p.pop()
                g[u][v][e]['visited'] = False

def eulerian_circuits(g, s, debug=False):
    '''Return all Eulerian circuits in the multi-graph g, starting from the node s'''
    for _, _, edata in g.edges(data=True): edata['visited'] = False
    return  _eulerian_circuits(g, [s], g.number_of_edges(), debug=debug)

def possible_assemblies(S, debug=False):
    '''Return all possible DNA strings that can be assembled from the read-(k+1)-mer-list S.'''
    g = de_bruijn_graph_single_strand(S)
    # g = collapse(g, s)
    if debug:
        print 'nodes', g.nodes()
        print '#nodes', g.number_of_nodes(), '#edges', g.number_of_edges()
    return [x for x in eulerian_circuits(g, initial_node(S), debug=debug) if x.startswith(S[0])]

def grep(f):
    '''Main driver to solve this problem.'''
    return ro.join_list(possible_assemblies(ro.read_lines(f)), delimiter='\n')

def test_possible_assemblies(file_name):
    S = ro.read_lines('%s/%s.dat' % (ro.ROSALIND_HOME, file_name))
    a = possible_assemblies(S)
    assert_equal(sorted(a), sorted(ro.read_lines('%s/%s.out' % (ro.ROSALIND_HOME, file_name))), 'Wrong assembly set')
    
if __name__ == "__main__":
    #test_possible_assemblies('rosalind_grep_sample')
    #print grep(ro.ROSALIND_HOME + '/rosalind_grep_sample.dat')
    print grep(ro.ROSALIND_HOME + '/rosalind_grep.dat')
