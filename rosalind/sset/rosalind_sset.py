'''
============================================================
http://rosalind.info/problems/sset

Given: A positive integer n (n<=1000).
Return: The total number of subsets of {1,2,...,n} modulo 1,000,000.
============================================================
'''
import rosalind.rosutil as ro
sset = lambda n, r = 1000000: pow(2, n, r)

if __name__ == "__main__":
    print sset(ro.read_int('rosalind_sset_sample.dat'))
    print sset(ro.read_int('rosalind_sset.dat'))
