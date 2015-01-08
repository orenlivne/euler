'''
============================================================
As in the case of unrooted trees, say that we have a fixed collection of n taxa labeling the leaves of a rooted binary tree T. You may like to verify that (by extension of "Counting Phylogenetic Ancestors") such a tree will contain n-1 internal nodes and 2n-2 total edges. Any edge will still encode a split of taxa; however, the two splits corresponding to the edges incident to the root of T will be equal. We still consider two trees to be equivalent if they have the same splits (which requires that they must also share the same duplicated split to be equal).

Let B(n) represent the total number of distinct rooted binary trees on n labeled taxa.

Given: A positive integer n (n<=1000).

Return: The value of B(n) modulo 1,000,000.
============================================================
'''
import rosalind.rosutil as ro, rosalind.rosalind_cunr as rc

# Same counting argument as problem CUNR, plus the option to add a new root and the nth leaf
# under it. Hence 2*(n-1)-2 edges + 1 = 2*n-3, so the total number is (2*n-3)!!.
num_rooted_trees = lambda n, r = 1000000: rc.num_unrooted_trees(n + 1, r)

if __name__ == "__main__":
    print num_rooted_trees(ro.read_int('rosalind_root_sample.dat'))
    print num_rooted_trees(ro.read_int('rosalind_root.dat'))
