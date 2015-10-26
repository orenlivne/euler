'''
============================================================
What's the probability that m people will have the same
birthday among a group of n people? (For m = 2, 3).

Created on Oct 25, 2015
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
import numpy as np, matplotlib.pyplot as P, itertools as it
from collections import Counter
from scipy.special import binom

NUM_SOLAR_DAYS = 365  # Ignoring February 29

def no_pair_probability(n, k):
    '''Returns the probability that no two people have the same birthday among
    a group of n people. k is the number of days in a year (i.e., number of
    birthday possibilities).'''
    # Calculating the log of the probability first to retain numerical accuracy.
    return np.exp(sum(np.log(k - i) for i in xrange(n)) - n * np.log(k))

def pair_probability(n, k):
    '''Returns the probability that there exist 2 people with the same birthday
    among a group of n people. k is the number of days in a year (i.e., number of
    birthday possibilities).'''
    return 1 - no_pair_probability(n, k)

def num_configs_with_i_pairs(n, k, i):
    '''Returns the number of configurations of n birthdays with k equal pairs and
    n - 2*k singletons.'''
    # Calculating the log of the probability first to retain numerical accuracy.
    return np.exp(sum(np.log(n - j) for j in xrange(2 * i))
                  - sum(np.log(j) for j in xrange(2, i + 1))
                  - i * np.log(2 * k))

def triplet_probability(n, k):
    '''Returns the probability that there exist 3 people with the same birthday
    among a group of n people. k is the number of days in a year (i.e., number of
    birthday possibilities).'''
    return 1 - sum(num_configs_with_i_pairs(n, k, i) * no_pair_probability(n - i, k) for i in xrange(n / 2 + 1))

def multi_birthday_probability(n, m, k):
    '''Returns the probability that there exist m people with
    the same birthday among a group of n people. k is the number of days in a year
    (i.e., number of birthday possibilities).'''
    if m == 2: return pair_probability(n, k)
    if m == 3: return triplet_probability(n, k)
    raise ValueError('Unsupported m = %d' % (m,))

def multi_birthday_probability_of_sample(n, m, k):
    birthdays = np.random.random_integers(0, k - 1, size=(n,))
    return max(Counter(birthdays).itervalues()) >= m

def multi_birthday_probability_experimental(n, m, k, sample_size=100):
    '''Returns the approximate probability that there exist m people with
    the same birthday among a group of n people. k is the number of days in a year
    (i.e., number of birthday possibilities) using random sampling.'''
    return float(sum(multi_birthday_probability_of_sample(n, m, k) for _ in xrange(sample_size))) / sample_size

def plot_probability(k, sample_size=1000):
    N = np.arange(1, 200)
    p_pair = [multi_birthday_probability(n, 2, k) for n in N]
    p_pair_ian = [multi_birthday_probability_ian(n, 2, k) for n in N]
    p_pair_experimental = [multi_birthday_probability_experimental(n, 2, k, sample_size=sample_size) for n in N]
    p_triple = [multi_birthday_probability(n, 3, k) for n in N]
    p_triple_ian = [multi_birthday_probability_ian(n, 3, k) for n in N]
    p_triple_experimental = [multi_birthday_probability_experimental(n, 3, k, sample_size=sample_size) for n in N]
    # Find the smallest n such that p >= 0.5. Assuming p is monotonically increasing with N.
    N_half_pair = it.dropwhile(lambda (n, p): p < 0.5, zip(N, p_pair)).next()[0]
    N_triple_pair = it.dropwhile(lambda (n, p): p < 0.5, zip(N, p_triple)).next()[0]
    P.clf()
    P.hold(True)
    P.plot(N, p_pair               , 'b-',
           N, p_pair_ian           , 'g-',
           N, p_pair_experimental  , 'b.',
           N, p_triple             , 'r-',
           N, p_triple_ian         , 'g-',
           N, p_triple_experimental, 'r.')
    P.legend(['m = 2, theoretical', 'm = 2, Ian', 'm = 2, %d samples' % (sample_size,),
              'm = 3, theoretical', 'm = 3, Ian', 'm = 3, %d samples' % (sample_size,)],
             loc='lower right')
    P.grid(True)
    P.xlabel('# People')
    P.ylabel('Probability')
    P.title('Probability of m people with the same birthday')
    y_limits = (-0.01, 1.01)
    P.plot([N_half_pair, N_half_pair], y_limits, 'k--')
    P.plot([N_triple_pair, N_triple_pair], y_limits, 'k--')
    P.ylim(y_limits)
    P.show()

def multi_birthday_probability_ian(n, m, k):
    '''Returns the approximate probability that there exist m people with
    the same birthday among a group of n people. k is the number of days in a year
    (i.e., number of birthday possibilities). Assumes the events of subsets of m people not having
    equal birthdays are independent of each other (for different subsets). Idea by Ian Atkinson.'''
    if m > n: return 0.0
    return 1.0 - (1.0 - 1.0 / (k**(m-1))) ** binom(n, m)

def compare_probabilities(n, m, sample_size=2 ** 16):
  print 'Theoretical', n, m, 100. * multi_birthday_probability(n, m, NUM_SOLAR_DAYS), '%'
  print 'Ian', n, m, 100. * multi_birthday_probability_ian(n, m, NUM_SOLAR_DAYS), '%'
  print 'Experimental(sample size %d)' % (sample_size,), 100. * multi_birthday_probability_experimental(n, m, NUM_SOLAR_DAYS, sample_size=sample_size), '%'
  print ''

if __name__ == '__main__':
    compare_probabilities(3, 2)
    compare_probabilities(3, 3)  # Oberlab / Caliskan+Chong+Igartua
    compare_probabilities(4, 3)  # Oberlab / Caliskan+Chong+Igartua
    compare_probabilities(20, 3)  # Oberlab / Caliskan+Chong+Igartua
    plot_probability(NUM_SOLAR_DAYS)
    P.savefig('multi_birthday.png')
