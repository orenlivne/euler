'''
============================================================
http://rosalind.info/problems/cntq

A quartet AB|CD is consistent with a binary tree T if the
quartet can be inferred from one of the splits of T (see "Quartets" for a description of inferring quartets from splits).

Let q(T) denote the total number of quartets that are consistent with T.

Given: A positive integer n (4<=n<=5000), followed by an unrooted binary tree T in Newick format on n taxa.

Return: The value of q(T) modulo 1,000,000.

Sample Dataset
============================================================
'''
import rosalind.rosutil as ro, rostree as rt, StringIO

'''Number of new quartets formed by two sub-trees below a node.'''
S = lambda n, m: n * (n - 1) * m * (m - 1) / 4

def num_quartets(t, r=1000000L):
    '''Augment a Phylo tree with the number of leaves and number of inferred quartets in sub-tree.
    Return the number of quartets at the root node = q(T) mod r.'''
    for node in t.find_clades(order='postorder'):
        children = list(node)
        node.num_terminals = 1 if node.is_terminal() else sum(child.num_terminals for child in node)
        node.num_quartets = 0 if node.is_terminal() else \
        (ro.sum_mod((child.num_quartets for child in node), r) + \
         (S(children[0].num_terminals, children[1].num_terminals) if len(children) == 2 else \
          ro.sum_mod((S(child.num_terminals,
                        sum(other_child.num_terminals for other_child in node if other_child != child))
                        for child in node), r))) % r#         sum(child.num_quartets for child in node) + \
#         (S(children[0].num_terminals, children[1].num_terminals) if len(children) == 2 else \
#          sum(S(child.num_terminals,
#                sum(other_child.num_terminals for other_child in node if other_child != child))
#              for child in node))
#         n = node.num_terminals
#         ref = cntq_ncgll(n)
#         print node, 'leaves', node.num_terminals, 'quartets', node.num_quartets, 'ref', ref
#         for child in node:
#             print '\t', child, child.num_terminals, child.num_quartets
#         if ref != node.num_quartets:
#             print 'NOT EQUAL TO WHAT WE THINK IT SHOULD BE'
    return t.root.num_quartets

def cntq_ncgll(n, r=1000000L):
    '''From https://github.com/Mgccl/mgccl-haskell/blob/master/rosalind/cntq.hs ...'''
    return (n * (n - 1) * (n - 2) * (n - 3) / 24) % r

def cntq(f):
    '''Main driver to solve this problem.'''
    return cntq_ncgll(int(ro.read_lines(f)[0])), num_quartets(rt.read_newick(StringIO.StringIO(ro.read_lines(f)[1])))

if __name__ == "__main__":
    print cntq('rosalind_cntq_sample.dat')
    print cntq('rosalind_cntq.dat')
