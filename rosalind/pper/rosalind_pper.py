'''
============================================================
http://rosalind.info/problems/pper

Given: Positive integers n and k such that 100>=n>0 and 10>=k>0.
Return: The total number of partial permutations P(n,k), modulo 1,000,000.
============================================================
'''
import rosalind.rosutil as ro

def pper(n, k, r=1000000L):
    return ro.prod_mod(xrange(n, n - k, -1), r)

if __name__ == "__main__":
    print '%d' % (pper(*ro.read_ints_str('rosalind_pper_sample.dat')),)
    print '%d' % (pper(*ro.read_ints_str('rosalind_pper.dat')),)
