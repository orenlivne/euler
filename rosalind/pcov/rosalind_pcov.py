'''
============================================================
http://rosalind.info/problems/pcov

A circular string is a string that does not have an initial or terminal element; instead, the string is viewed as a necklace of symbols. We can represent a circular string as a string enclosed in parentheses. For example, consider the circular DNA string (ACGTAC), and note that because the string "wraps around" at the end, this circular string can equally be represented by (CGTACA), (GTACAC), (TACACG), (ACACGT), and (CACGTA). The definitions of substrings and superstrings are easy to generalize to the case of circular strings (keeping in mind that substrings are allowed to wrap around).

Given: A collection of (error-free) DNA k-mers (k<=50) taken from the same strand of a circular chromosome. In this dataset, all k-mers from this strand of the chromosome are present, and their de Bruijn graph consists of exactly one simple cycle.

Return: A cyclic superstring of minimal length containing the reads (thus corresponding to a candidate cyclic chromosome).
============================================================
'''
import rosalind.rosutil as ro

def perfect_coverage_recon(r):
    '''Reconstruct a DNA string from a perfect-coverage read generator.'''
    g = ro.de_bruijn_graph(r)
    s, node = '', g.nodes_iter().next()  # Start from an arbitrary node
    for _ in xrange(g.number_of_nodes()):  # Follow the cycle
        s += node[0]  # Take the first letter from every read
        node = g.successors_iter(node).next()
    return s

def pcov(f):
    '''Main driver to solve this problem.'''
    return perfect_coverage_recon(ro.iterlines(f))

if __name__ == "__main__":
    print pcov('rosalind_pcov_sample.dat')
    print pcov('rosalind_pcov.dat')
