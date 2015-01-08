#!/usr/bin/env python
'''
============================================================
Calculate p-value significance values of the intersection
sizes of pairs of LD block sets associated with diseases
in Alexandra's matrix.

Read matrix of LD block intersection sizes from standard
input in CSV format.

Write corresponding p-value matrix to standard output in 
CSV format.

Example of running:
ld_block_significance.py 5725 < disease_matrix.no_header.csv > p_value_matrix.csv
 
Created on September 11, 2013
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
import numpy as np, sys, matplotlib.pylab as P

def log_factorial(N):
    '''Return an array of log(n) for n=0,...,N-1.'''
    L = np.zeros((N,))
    for i in xrange(1, N): L[i] = L[i - 1] + np.log(i)
    return L

class LogNChooseKCalculator(object):
    '''Calculates log n-choose-k for a fixed range of n''s.''' 
    def __init__(self, N):
        '''Initialize a calculator of logs of binomial coefficients (n-choose-k) up to n=N-1.'''
        # Cache log(n!) values for n=0,..,N-1.
        self._L = log_factorial(N)

    def __call__(self, n, k):
        '''Return n-choose-k.'''
        return self._L[n] - self._L[k] - self._L[n - k]

class PairIntersectionSizePdf(object):
    '''Probability density function of the intersection size of a pair of LD blocks.'''
    def __init__(self, N):
        '''PDF for the case of n1,n2.'''
        self._c = LogNChooseKCalculator(N + 1)
        self._N = N

    def pdf(self, n1, n2, k):
        '''Return the probability density function P(X=k) for ld block sizes n1,n2.'''
        c, N = self._c, self._N
        return np.exp(c(n1, k) + c(N - n1, n2 - k) - c(N, n2))

    def p_value(self, n1, n2, k):
        '''Return the p-value P(X >= k) = integral_{k}^{\infty} P(X=x) dx
        for ld block sizes n1,n2.'''
        return sum(self.pdf(n1, n2, x) for x in xrange(k, min(n1, n2) + 1))

def plot_distribution(N, n1, n2):
    '''Illustration: plot the distribution.'''
    p = PairIntersectionSizePdf(N, n1, n2)
    a, b = 0, min(n1, n2) + 1
    pdf = [p.pdf(k) for k in xrange(a, b)]
    P.figure(1)
    P.clf()
    P.bar(range(a, b), pdf)
    P.xlabel('Intersection Size (k)')
    P.ylabel('Probability')
    P.title('PDF of Intersection Size of Two Sets of Sizes %d,%d Out Of %d' % (n1, n2, N))
    P.show()

'''Main program'''
if __name__ == '__main__':
    # Example: plot the distribution
    # plot_distribution(6000, 3000, 3000)
    
    # Load matrix of LD block intersection sizes from standard input 
    N = int(sys.argv[1])
    a = np.loadtxt(sys.stdin, dtype=int, delimiter=',')
    d = a.shape[0]
    # Diagonal of matrix = number of LD blocks associated with each disease
    n = [a[i, i] for i in xrange(d)]
    # Calculate p-values for each entry
    p = PairIntersectionSizePdf(N)
    b = np.array([[p.p_value(n[i], n[j], a[i, j]) for j in xrange(d)] for i in xrange(d)])
    # Output to standard output
    np.savetxt(sys.stdout, b, fmt='%.3e', delimiter=',')
    