'''
============================================================
http://rosalind.info/problems/cbtl

Given a collection of n taxa, any subset S of these taxa can
be seen as encoding a character that divides the taxa into
the sets S and Sc; we can represent the character by S|Sc,
which is called a split. Alternately, the character can be
represented by a character array A of length n for which
A[j]=1 if the jth taxon belongs to S and A[j]=0 if the jth
taxon belongs to Sc (recall the "ON"/"OFF" analogy from "Counting Subsets").

At the same time, observe that the removal of an edge from an unrooted binary tree produces two separate trees, each one containing a subset of the original taxa. So each edge may also be encoded by a split S|Sc.

A trivial character isolates a single taxon into a group of its own. The corresponding split S|Sc must be such that S or Sc contains only one element; the edge encoded by this split must be incident to a leaf of the unrooted binary tree, and the array for the character contains exactly one 0 or exactly one 1. Trivial characters are of no phylogenetic interest because they fail to provide us with information regarding the relationships of taxa to each other. All other characters are called nontrivial characters (and the associated splits are called nontrivial splits).

A character table is a matrix C in which each row represents the array notation for a nontrivial character. That is, entry Ci,j denotes the "ON"/"OFF" position of the ith character with respect to the jth taxon.

Given: An unrooted binary tree T in Newick format for at most 200 species taxa.

Return: A character table having the same splits as the edge splits of T. The columns of the character table should encode the taxa ordered lexicographically; the rows of the character table may be given in any order. Also, for any given character, the particular subset of taxa to which 1s are assigned is arbitrary.
============================================================
'''
import rosalind.rosutil as ro, rostree as rt, numpy as np

def aug_num_terminals(t):
    '''Augment a Phylo tree with the number of terminal nodes in sub-tree.'''
    for node in t.find_clades(order='postorder'): node.num_terminals = 1 if node.is_terminal() else sum(child.num_terminals for child in node)
    return t

def char_splits(t):
    '''Generate split tuples in lexicographic ordering.'''
    nodes = list(t.find_clades(order='postorder'))
    n = len(nodes)
    s = np.zeros((n,), dtype=bool)
    term = np.array([x.postorder for x in sorted(t.find_clades(terminal=True), key=lambda x: x.name)])
    #print term
    for node in t.find_clades(order='postorder', terminal=False):
        children = list(node)
        #print repr(node), '#children', len(children)
        for i, child in enumerate(children):
            #print 'i', i, 'child', repr(child), 'prev', child.prev_child
            if child.num_terminals > 1:
                stop = child.postorder + 1
                prev = child.prev_child
                start = (prev.postorder + 1) if prev else 0
                #print 'Cut off branch to', repr(child), 'postorder indices', start, 'to', (stop - 1)
                s[start:stop] = True
                #print s
                #print s[term]
                yield s[term]
                s[start:stop] = False

def cbtl(f):
    '''Main driver to solve this problem.'''
    for s in char_splits(aug_num_terminals(rt.read_newick(f))): print ro.join_list((int(x) for x in s), delimiter='')

if __name__ == "__main__":
    #cbtl('rosalind_cbtl_sample.dat')
    cbtl('rosalind_cbtl.dat')
