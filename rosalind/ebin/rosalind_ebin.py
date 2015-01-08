'''
============================================================
http://rosalind.info/problems/ebin

In "The Wright-Fisher Model of Genetic Drift", we generalized the concept of a binomial random variable Bin(n,p) as a "weighted coin flip." It is only natural to calculate the expected value of such a random variable.

For example, in the case of unweighted coin flips (i.e., p=1/2), our intuition would indicate that E(Bin(n,1/2) is n/2; what should be the expected value of a binomial random variable?

Given: A positive integer n (n<=1000000) followed by an array P of length m (m<=20) containing numbers between 0 and 1. Each element of P can be seen as representing a probability corresponding to an allele frequency.

Return: An array B of length m for which B[k] is the expected value of Bin(n,P[k]); in terms of Wright-Fisher, it represents the expected allele frequency of the next generation.
============================================================
'''
import rosalind.rosutil as ro

def ebin(f):
    '''Main driver to solve this problem.'''
    lines = ro.read_lines(f)
    n = int(lines[0])
    p = map(float, lines[1].split())
    return ro.join_list((n * x for x in p))

if __name__ == "__main__":
    #print ebin('rosalind_ebin_sample.dat')
    print ebin('rosalind_ebin.dat')
