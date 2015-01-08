'''
============================================================
http://rosalind.info/problems/lrep

A repeated substring of a string s of length n is simply a substring that appears in more than one location of s; more specifically, a k-fold substring appears in at least k distinct locations.

The suffix tree of s, denoted T(s), is defined as follows:

T(s) is a rooted tree having exactly n leaves.
Every edge of T(s) is labeled with a substring of s*, where s* is the string formed by adding a placeholder symbol $ to the end of s.
Every internal node of T(s) other than the root has at least two children; i.e., it has degree at least 3.
The substring labels for the edges leading from a node to its children must begin with different symbols.
By concatenating the substrings along edges, each path from the root to a leaf corresponds to a unique suffix of s*.
See Figure 1 for an example of a suffix tree.

Given: A DNA string s (of length at most 20 kbp) with $ appended, a positive integer k, and a list of edges defining the suffix tree of s. Each edge is represented by four components:

the label of its parent node in T(s);
the label of its child node in T(s);
the location of the substring t of s* assigned to the edge; and
the length of t.
Return: The longest substring of s that occurs at least k times in s. (If multiple solutions exist, you may return any single solution.)
============================================================
'''
import rosalind.rosutil as ro, rosmatch as rm, itertools as it

def read_data(f):
    '''Return s,k, edge list iterator. Nodes are converted to 0-based numbers,
    string start to 0-based.'''
    lines = ro.iterlines(f)
    return lines.next(), int(lines.next()), it.imap(lambda x: (int(x[0][4:]) - 1, int(x[1][4:]) - 1, (int(x[2]) - 1, int(x[3]))), (x.split() for x in lines))

def lrep(f):
    '''Main driver to solve this problem.'''
    s, k, edge_list = read_data(f)
    t = rm.SuffixTree(s, edge_list)
    node = t.max_repeated(k)
    return t.prefix_of_node(node)

if __name__ == "__main__":
    # print lrep('rosalind_lrep_sample.dat')
    print lrep('rosalind_lrep.dat')
