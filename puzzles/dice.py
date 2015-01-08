'''
============================================================
If a 6 sided die is rolled twice, what is the probability
that the second roll is larger than the first?

Created on Jan 8, 2015
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
import random, numpy as np, matplotlib.pyplot as P

def sample_second_roll_greater(n, sample_size=100):
    '''Roll two dice and record results. Repeat sample_size times'''
    second_is_greater = 0
    for _ in xrange(sample_size):
        if random.randint(1, n) < random.randint(1, n): second_is_greater += 1
    return (1.0 * second_is_greater) / sample_size

def second_roll_greater_probability(n):
    '''Expected value, theoretically derived.'''
    return (n - 1.) / (2 * n)

def plot_probability():
    n = np.arange(1, 11)
    P.plot(n, second_roll_greater_probability(n), \
           n, [sample_second_roll_greater(x, sample_size=100) for x in n], \
           n, [sample_second_roll_greater(x, sample_size=1000) for x in n], \
           n, [sample_second_roll_greater(x, sample_size=10000) for x in n])
    P.grid(True)
    P.legend(['Theoertical', '100 Simulations', '1000 Simulations', '10000 Simulations'], loc='bottom right')
    P.xlabel('Number of dice sides')
    P.ylabel('Probability of Second Roll > First Roll')
    P.title('Probability of Second Roll > First Roll vs. Number of Dice Sides')
    P.show()

if __name__ == '__main__':
    plot_probability()
    
