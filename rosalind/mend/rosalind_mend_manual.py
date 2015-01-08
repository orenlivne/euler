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
        
GENOTYPE_TO_PROB = {'AA': (1, 0, 0), 'Aa': (0, 1, 0), 'aa': (0, 0, 1)}

def geno_prob(t):
    if t.data: return GENOTYPE_TO_PROB[t.data]  # Leaf
    else:  # Node
        p, q, r = geno_prob(t.left)
        p2, q2, r2 = geno_prob(t.right)
        AA = (p + 0.5 * q) * (p2 + 0.5 * q2)
        aa = (r + 0.5 * q) * (r2 + 0.5 * q2)
        Aa = 1 - AA - aa
        return (AA, Aa, aa)
        
def mend(f):
    '''Main driver to solve this problem.'''
    return ro.join_list(geno_prob(rt.parse_newick(ro.read_str(f))))

if __name__ == "__main__":
    #print mend('rosalind_mend_sample.dat')
    print mend('rosalind_mend.dat')
