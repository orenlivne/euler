'''
============================================================
What's the probability that m people will have the same
birthday among a group of n people? (For m = 2, 3). 

Created on Oct 25, 2015
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
import numpy as np, matplotlib.pyplot as P, scipy.special
from collections import Counter

NUM_DAYS = 365  # Ignoring February 29

def no_pair_probability(n, k):
    '''Returns the probability that no two people have the same birthday among
    a group of n people. k is the number of days in a year (i.e., number of
    birthday possibilities).'''
    return np.exp(sum(np.log(k - i) for i in xrange(n)) - n * np.log(k))

def pair_probability(n, k):
    '''Returns the probability that there exist 2 people with the same birthday
    among a group of n people. k is the number of days in a year (i.e., number of
    birthday possibilities).'''
    return 1 - no_pair_probability(n, k)

def triplet_probability(n, k):
    '''Returns the probability that there exist 3 people with the same birthday
    among a group of n people. k is the number of days in a year (i.e., number of
    birthday possibilities).'''
    for i in xrange(n / 2):
        print i, 'pairs', 'p', no_pair_probability(n - 2 * i, k), scipy.special.binom(n, i) / (k ** i), scipy.special.binom(n, i)
    return 1 - sum((scipy.special.binom(n, i) / (k ** i)) * no_pair_probability(n - 2 * i, k) for i in xrange(n / 2))  
      
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

def plot_probability(m):
    N = np.arange(1, 50)
    P.plot(N, [multi_birthday_probability(n, m, NUM_DAYS) for n in N], 'b-', \
           N, [multi_birthday_probability_experimental(n, m, NUM_DAYS, sample_size=100) for n in N], 'g-', \
           N, [multi_birthday_probability_experimental(n, m, NUM_DAYS, sample_size=10000) for n in N], 'r-')
    P.grid(True)
    P.legend(['Theoretical', '100 Samples', '10000 samples', '40000 samples'], loc='upper left')
    P.xlabel('# People')
    P.ylabel('Probability')
    P.title('Probability of %d people with the same birthday' % (m,))
    P.show()
    
def compare_probabilitie(n, m):
    print 'Theoretical', n, m, multi_birthday_probability(n, m, NUM_DAYS)
    print 'Experimental'
    for N in 2 ** np.arange(15):
        print N, multi_birthday_probability_experimental(n, m, NUM_DAYS, sample_size=N)

if __name__ == '__main__':
    # compare_probabilitie(20, 2)
    compare_probabilitie(20, 3)
    # TODO: show all probabilities on the same graph
#    plot_probability(2)
    # plot_probability(3)
