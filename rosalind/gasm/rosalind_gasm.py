'''
============================================================
http://rosalind.info/problems/gasm

A directed cycle is simply a cycle in a directed graph in
which the head of one edge is equal to the tail of the next
(so that every edge in the cycle is traversed in the same
direction).

For a set of DNA strings S and a positive integer k, let Sk
denote the collection of all possible k-mers of the strings
in S.

Given: A collection S of (error-free) reads of equal length (not exceeding 50 bp). In this dataset, for some positive integer k, the de Bruijn graph Bk on Sk+1 U Srck+1 consists of exactly two directed cycles.

Return: A cyclic superstring of minimal length containing every read or its reverse complement.
============================================================
'''
import rosalind.rosutil as ro, networkx as nx, itertools as it

'''The reverse complement set of a set of strings.'''
revc_set = lambda S: [ro.revc(u) for u in S]

def db_graph(S, SC, k):
    '''A de-Bruijn graph B_k of a list S of reads and its reverse complement SC.'''
    return nx.from_edgelist(((r[:-1], r[1:]) 
                             for r in it.chain.from_iterable(ro.kmers(u, k + 1) for u in it.chain(S, SC))),
                            create_using=nx.DiGraph())

def cyclic_strings(g):
    '''Generate all cyclic strings in the de-Bruijn graph g if it consists of a collection of cycles.
    If not, returns nothing.'''
    if not all(g.out_degree(u) == 1 for u in g): return
    g, V = g.copy(), set(g.nodes_iter())
    print 'k', len(g.nodes_iter().next()), 'nodes', g.number_of_nodes(), 'edges', g.number_of_edges()
    while V:  # Loop over all cycles until graph is empty
        #print 'V', V
        s, u, cycle = '', g.nodes_iter().next(), set()  # Start cycle tracing at an arbitrary node u
        v = u  # Keeps track of current node in the cycle
        while True:  # While cycle is not complete, advance v to next vertex in the cycle & add v to s, cycle
            s += v[0]
            cycle.add(v)
            v = g.successors_iter(v).next()
            if v == u: break  # Cycle is complete
#         print cycle
#         print 's', s 
        yield s
        # Remove cycle from graph
        V -= cycle
        g = g.subgraph(V)
        
def min_superstring(S):
    '''Reconstruct a minimum-length super-string from a list S of reads.'''
    SC = revc_set(S)
    return min((len(s), s) for k in xrange(1, len(S[0])) for s in cyclic_strings(db_graph(S, SC, k)))[1]

def gasm(f):
    '''Main driver to solve this problem.'''
    return min_superstring(ro.read_lines(f))

if __name__ == "__main__":
    print gasm(ro.ROSALIND_HOME + '/rosalind_gasm_sample.dat')
    print gasm(ro.ROSALIND_HOME + '/rosalind_gasm.dat')
