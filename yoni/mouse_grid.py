'''
============================================================
Tony the mouse starts in the top left corner of a 3x3 grid.
After each second, he randomly moves to an adjacent square
with equal probability. What is the probability he reaches
the cheese in the bottom right corner before he reaches the
mousetrap in the center?

Created on Apr 11, 2015
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
import itertools as it, random, numpy as np, matplotlib.pyplot as P
from numpy import linalg

def cell_num(k, n):
    '''Returns a 0-based state number of cell number (k(0),...,k(d-1)) in an n^d grid.'''
    i = k[0]
    for m in xrange(1, len(k)): i = n * i + k[m]
    return i

def unit_vector(d, k):
    x = np.zeros((d, 1))
    x[k] = 1.0
    return x

def absorbing_probability(n, d):
    '''Returns the probability of the top-left state transitioning to the aborbing bottom right state.'''
    if n % 2 == 0: raise ValueError('n must be odd')
    # Build the mouse's transition matrix P.
    directions = [-1, 1]
    absorbing = set(map(lambda k: cell_num(k, n), [[n / 2] * d, [n - 1] * d]))
    num_states = n ** d
    P = np.matrix(np.zeros((num_states, num_states)))
    for k in it.product(range(n), repeat=d):
        i = cell_num(k, n)
        if i in absorbing: P[i, i] = 1
        else:
            for q in xrange(d):
                for s in directions:
                    k_nbhr = list(k)
                    k_nbhr[q] += s
                    k_nbhr = tuple(k_nbhr)
                    if k_nbhr[q] >= 0 and k_nbhr[q] < n:
                        j = cell_num(k_nbhr, n)
                        P[i, j] = 1
    P = np.diag(1. / np.array(np.sum(P, 1))[:, 0]) * P
    
    # Calculate the probability of transitive state 0 (top left corner) being absorbed in absorbing
    # state 1 (bottom left corner).  
    t = sorted(set(xrange(num_states)) - absorbing)
    r = sorted(absorbing)
    Q = P[np.ix_(t, t)]
    R = P[np.ix_(t, r)]
    return linalg.solve(np.eye(len(t)) - Q, R * unit_vector(len(r), 1))[0, 0]
    
def absorbing_state_experimental():
    state = (0, 0)
    while True:
        if state == (1, 1): return 0
        elif state == (2, 2): return 1
        i, j = state
        nbhrs = filter(lambda (k, l): k >= 0 and k < 3 and l >= 0 and l < 3, [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)])
        state = random.choice(nbhrs)

def absorbing_probability_experimental(sample_size=100):
    return float(sum(absorbing_state_experimental() for _ in xrange(sample_size))) / sample_size

# def expected_length_to_k_in_a_row(p, k, sample_size=100):
#     s = 0
#     pmf = dict() 
#     for _ in xrange(sample_size):
#         x = length_to_k_in_a_row(p, k)
#         s += x
#         pmf[x] = pmf.setdefault(x, 0) + 1
#     print 'PMF'
#     r = 2 * p * (1 - p)
#     for k, v in sorted(pmf.iteritems()):
#         print 'k', k, 'sample', (1.0 * v) / sample_size, 'theoretical', r ** (k - 2) * (1 - r)
#     return (1.0 * s) / sample_size    
#     # return (1.0 * sum(length_to_k_in_a_row(p, k) for _ in xrange(sample_size))) / sample_size
# 
# def sum_expected_length_to_k_in_a_row(p, k, terms=100):
#     q = 1 - p
#     c = [p * q * (p ** (l - 1) + q ** (l - 1)) for l in xrange(1, k)]
#     print 'c', c
#     x = [0] * (k - 1) + [p ** k + q ** k]
#     s = k * x[-1]
#     print 'n', k, 'x', x
#     for n in xrange(k + 1, terms + k + 1):
#         x = x[1:] + [sum(x[-l] * c[l - 1] for l in xrange(1, k))]
#         s += n * x[-1]
#         print 'n', n, 'x', x
#     return s
# 
# def theoretical_expected_length_to_k_in_a_row(p, k):
#     return (((k - 1) * p ** k - k * p ** (k - 1) + 1) * p ** 2 + ((k - 1) * (1 - p) ** k - k * (1 - p) ** (k - 1) + 1) * (1 - p) ** 2) / (p * (1 - p) * (p ** k + (1 - p) ** k)) + k
# 
# def compare_theoretical_and_sampling_results(p, k):
#     avg_theoretical = theoretical_expected_length_to_k_in_a_row(p, k)
#     # avg_old = 0
#     print avg_theoretical
#     for n in xrange(1, 8):
#         sample_size = 10 ** n
#         avg = expected_length_to_k_in_a_row(p, k, sample_size=sample_size)
#         avg_sum = sum_expected_length_to_k_in_a_row(p, k)
#         print sample_size, avg, avg_sum, abs(avg - avg_theoretical)
#         # avg_old = avg
# 

def plot_probability():
    N = np.arange(3, 17, 2)
    D = np.arange(1, 4)
    colors = ['k', 'b', 'g', 'r', 'm']
    P.figure(1)
    P.clf()
    P.hold(True)
    for d, c in zip(D, colors):
        P.plot(N, [absorbing_probability(n, d) for n in N], '%so-' % (c,))
# #, \
# p, [expected_length_to_k_in_a_row(x, k, sample_size=10000) for x in p], '%s--' % (c,))
    P.grid(True)
    P.legend(['%d-D grid' % (d,) for d in D])
    P.xlabel('Grid size')
    P.ylabel('Probability')
    P.title('Probability of Getting to Bottom-Right Corner before Middle')
    P.show()

if __name__ == '__main__':
    for N in 2 ** np.arange(10):
        print N, absorbing_probability_experimental(sample_size=N)
    for d in xrange(1, 4):
        for n in xrange(3, 17, 2):
            print n, d, absorbing_probability(n, d)
    plot_probability()
