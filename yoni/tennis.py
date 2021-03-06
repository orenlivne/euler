'''Nick has a terrible sleep schedule. He randomly picks a time between 4 AM and
6 AM to fall asleep, and wakes up at a random time between 11 AM and 1 PM of the
same day. What is the probability that Nick gets between 6 and 7 hours of
sleep?'''

import random, numpy as np, matplotlib.pyplot as P

def toss(p):
    '''Returns True with probability p and False with probability 1-p.'''
    return random.random() < p

def length_to_k_in_a_row(p, k):
    '''Returns the length of a random coin toss sequence ending with k in a row.'''
    seq_length, latest_tosses = k, [toss(p) for _ in xrange(k)]
    num_heads = sum(1 for x in latest_tosses if x)
    while num_heads > 0 and num_heads < k:
        if latest_tosses[seq_length % k]: num_heads -= 1
        new_toss = toss(p)
        latest_tosses[seq_length % k] = new_toss
        if new_toss: num_heads += 1
        seq_length += 1
    return seq_length

def expected_length_to_k_in_a_row(p, k, sample_size=100):
    s = 0
    pmf = dict()
    for _ in xrange(sample_size):
        x = length_to_k_in_a_row(p, k)
        s += x
        pmf[x] = pmf.setdefault(x, 0) + 1
    print 'PMF'
    r = 2 * p * (1 - p)
    for k, v in sorted(pmf.iteritems()):
        print 'k', k, 'sample', (1.0 * v) / sample_size, 'theoretical', r ** (k - 2) * (1 - r)
    return (1.0 * s) / sample_size
    # return (1.0 * sum(length_to_k_in_a_row(p, k) for _ in xrange(sample_size))) / sample_size

def sum_expected_length_to_k_in_a_row(p, k, terms=100):
    q = 1 - p
    c = [p * q * (p ** (l - 1) + q ** (l - 1)) for l in xrange(1, k)]
    print 'c', c
    x = [0] * (k - 1) + [p ** k + q ** k]
    s = k * x[-1]
    print 'n', k, 'x', x
    for n in xrange(k + 1, terms + k + 1):
        x = x[1:] + [sum(x[-l] * c[l - 1] for l in xrange(1, k))]
        s += n * x[-1]
        print 'n', n, 'x', x
    return s

def theoretical_expected_length_to_k_in_a_row(p, k):
    return (((k - 1) * p ** k - k * p ** (k - 1) + 1) * p ** 2 + ((k - 1) * (1 - p) ** k - k * (1 - p) ** (k - 1) + 1) * (1 - p) ** 2) / (p * (1 - p) * (p ** k + (1 - p) ** k)) + k

def compare_theoretical_and_sampling_results(p, k):
    avg_theoretical = theoretical_expected_length_to_k_in_a_row(p, k)
    # avg_old = 0
    print avg_theoretical
    for n in xrange(1, 8):
        sample_size = 10 ** n
        avg = expected_length_to_k_in_a_row(p, k, sample_size=sample_size)
        avg_sum = sum_expected_length_to_k_in_a_row(p, k)
        print sample_size, avg, avg_sum, abs(avg - avg_theoretical)
        # avg_old = avg

def plot_probability():
    p = np.linspace(0.01, 0.5)
    K = range(6)
    colors = ['k', 'b', 'g', 'r', 'm']
    P.figure(1)
    P.clf()
    P.hold(True)
    for k, c in zip(K, colors):
        P.plot(p, theoretical_expected_length_to_k_in_a_row(p, k), '%s-' % (c,), \
               p, [expected_length_to_k_in_a_row(x, k, sample_size=10000) for x in p], '%s--' % (c,))
    P.grid(True)
    P.legend(['%d in a row' % (k,) for k in K])
    P.xlabel('Probability of Heads')
    P.ylabel('Expected Value')
    P.title('EXpected Number of Coin Tosses to $k$-in-a-row')
    P.show()

if __name__ == '__main__':
    compare_theoretical_and_sampling_results(0.25, 2)
    #compare_theoretical_and_sampling_results(0.5, 3)
    # plot_probability()
