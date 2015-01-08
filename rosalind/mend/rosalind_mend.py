'''
============================================================
http://rosalind.info/problems/mend

A rooted binary tree can be used to model the pedigree of an individual. In this case, rather than time progressing from the root to the leaves, the tree is viewed upside down with time progressing from an individual's ancestors (at the leaves) to the individual (at the root).

An example of a pedigree for a single factor in which only the genotypes of ancestors are given is shown in Figure 1.

Given: A rooted binary tree T in Newick format encoding an individual's pedigree for a Mendelian factor whose alleles are A (dominant) and a (recessive).

Return: Three numbers between 0 and 1, corresponding to the respective probabilities that the individual at the root of T will exhibit the "AA", "Aa" and "aa" genotypes.
============================================================
'''
import rosalind.rosutil as ro, rostree as rt
#from Bio import Phylo
        
GENOTYPE_TO_PROB = {'AA': (1, 0, 0), 'Aa': (0, 1, 0), 'aa': (0, 0, 1)}

def geno_prob_stack(t):
    '''Calculate the genotype probabilities at t''s root.
    A non-recursive Phylo tree post-traversal implementation.'''
    stack = []
    for node in t.find_clades(order='postorder'):
        if node.is_terminal(): stack.append(GENOTYPE_TO_PROB[node.name])  # Leaf
        else:  # Node
            p2, q2, r2 = stack.pop()
            p, q, r = stack.pop()
            AA = (p + 0.5 * q) * (p2 + 0.5 * q2)
            aa = (r + 0.5 * q) * (r2 + 0.5 * q2)
            stack.append((AA, 1 - AA - aa, aa))
    return stack.pop()

def geno_prob_recursive(t):
    '''Calculate the genotype probabilities at t''s root. Recursive implementation'''
    if t.is_terminal(): return GENOTYPE_TO_PROB[t.name]  # Leaf
    else:  # Node
        left, right = list(t)
        p, q, r = geno_prob(left)
        p2, q2, r2 = geno_prob(right)
        AA = (p + 0.5 * q) * (p2 + 0.5 * q2)
        aa = (r + 0.5 * q) * (r2 + 0.5 * q2)
        return AA, 1 - AA - aa, aa

def geno_prob(t):
    '''Calculate the genotype probabilities at t''s root. Non-recursive implementation
    using our augmented info.'''
    for node in t.find_clades(order='postorder'):
        if node.is_terminal(): node.g = GENOTYPE_TO_PROB[node.name]  # Leaf
        else:  # Node
            left, right = list(node)
            p, q, r = left.g
            p2, q2, r2 = right.g
            AA = (p + 0.5 * q) * (p2 + 0.5 * q2)
            aa = (r + 0.5 * q) * (r2 + 0.5 * q2)
            node.g = (AA, 1 - AA - aa, aa)
    return t.root.g

def mend(f):
    '''Main driver to solve this problem.'''
    return ro.join_list(geno_prob(rt.read_newick(f).root))

if __name__ == "__main__":
    print mend('rosalind_mend_sample.dat')
    print mend('rosalind_mend.dat')
