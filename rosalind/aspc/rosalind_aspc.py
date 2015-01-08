'''
============================================================
http://rosalind.info/problems/aspc

In "Counting Subsets", we saw that the total number of subsets
of a set S containing n elements is equal to 2n.

However, if we intend to count the total number of subsets of S having a fixed size k, then we use the combination statistic C(n,k), also written (nk).

Given: Positive integers n and m with 0<=m<=n<=2000.

Return: The sum of combinations C(n,k) for all k satisfying m<=k<=n, modulo 1,000,000. In shorthand, SUM nk=m(nk).
============================================================
'''
import rosalind.rosutil as ro, itertools as it

def aspc(f, r=1000000L):
    '''Main driver to solve this problem.'''
    n, m = ro.read_ints_str(f)
    return ro.sum_mod(it.islice(ro.binom_mod(r), n, n + 1).next()[m:], r)

if __name__ == "__main__":
    print aspc('rosalind_aspc_sample.dat')
    print aspc('rosalind_aspc.dat')
