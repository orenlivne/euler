'''
============================================================
http://rosalind.info/problems/indc

Consider a collection of coin flips. One of the most natural
questions we can ask is if we flip acoin 92 times, what is the
probability of obtaining 51 "heads", vs. 27 "heads", vs. 92 "heads"?

Each coin flip can be modeled by a uniform random variable in which each of the two outcomes
("heads" and "tails") has probability equal to 1/2. We may assume that these random variables
are independent (see "Independent Alleles"); in layman's terms, the outcomes of the two coin flips
do not influence each other.

A binomial random variable X takes a value of k if n consecutive "coin flips" result in k total "heads" and n-k total "tails." We write that X ~ Bin(n,1/2).

Given: A positive integer n<=50.

Return: An array A of length 2n in which A[k] represents the common logarithm of the probability that two diploid siblings share at least k of their 2n chromosomes (we do not consider recombination for now).
============================================================
'''
import rosalind.rosutil as ro, numpy as np, itertools as it

def indc(f):
    '''Main driver to solve this problem. We use exact arithmetic for binomials
    instead of the betainc function to avoid round-off.'''
    n = 2 * ro.read_int(f)
    # return ro.join_list('%.5f' % (np.log10(1 - ro.cumbin(n, 0.5, k - 1)),) for k in xrange(1, n + 1))
    return ro.join_list('%.3f' % (x,) for x in np.log10(map(float, np.cumsum(it.islice(ro.binom(), n, n + 1).next())))[-2::-1] - n * np.log10(2))

if __name__ == "__main__":
    print indc('rosalind_indc_sample.dat')
    print indc('rosalind_indc.dat')
