'''
============================================================
http://rosalind.info/problems/wfmd

Consider flipping a weighted coin that gives "heads" with some fixed probability p (i.e., p is not necessarily equal to 1/2).

We generalize the notion of binomial random variable from "Independent Segregation of Chromosomes" to quantify the sum of the weighted coin flips. Such a random variable X takes a value of k if a sequence of n independent "weighted coin flips" yields k "heads" and n-k "tails." We write that X~Bin(n,p).

To quantify the Wright-Fisher Model of genetic drift,
consider a population of N diploid individuals, whose 2N
chromosomes possess m copies of the dominant allele. As in
"Counting Disease Carriers", set p=m2N. Next, recall that
the next generation must contain exactly N individuals.
These individuals' 2N alleles are selected independently: a
dominant allele is chosen with probability p, and a
recessive allele is chosen with probability 1-p.

Given: Positive integers N (N<=7), m (m<=2N), g (g<=6) and k (k<=2N).

Return: The probability that in a population of N diploid individuals initially possessing m copies of a dominant allele, we will observe after g generations at least k copies of a recessive allele. Assume the Wright-Fisher model.
============================================================
'''
import rosalind.rosutil as ro, itertools as it

def wfmd(f):
    '''Main driver to solve this problem.'''
    N, m, g, k = ro.read_ints_str(f)
    n = 2 * N
    return sum(it.islice(ro.wf_pmf(n, m), g - 1, g).next()[:n - k + 1])

if __name__ == "__main__":
    print wfmd('rosalind_wfmd_sample.dat')
    print wfmd('rosalind_wfmd.dat')
