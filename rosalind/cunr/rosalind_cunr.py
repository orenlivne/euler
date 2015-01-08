'''
============================================================
http://rosalind.info/problems/cunr

Given: A positive integer n (n<=1000).
Return: The total number of subsets of {1,2,...,n} modulo 1,000,000.
============================================================
'''
import rosalind.rosutil as ro

num_unrooted_trees = lambda n, r = 1000000: ro.prod_mod(((2 * i - 1) for i in xrange(1, n - 1)), r)

if __name__ == "__main__":
    print num_unrooted_trees(ro.read_int('rosalind_cunr_sample.dat'))
    print num_unrooted_trees(ro.read_int('rosalind_cunr.dat'))
