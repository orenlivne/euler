'''
============================================================
Two people Adam and Bryan go to the same swimming pool
between 2 pm and 5 pm at a random time and each one of them
swims for one hour. What is the chance of them being
together in the swimming pool?

Created on Jan 7, 2015
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
import random, numpy as np, matplotlib.pyplot as P

def intervals_intersect(a, b, c, d):
    '''Do intervals [a,b], [c,d] intersect?'''
    return max(a, c) <= min(b, d)

def sample_interval_intersection(L, sample_size=100):
    '''Swimming pool open L hours; intervals of size 1.'''
    intersections = 0
    for _ in xrange(sample_size):
        a, b = random.uniform(0, L), random.uniform(0, L)
        if intervals_intersect(a, a + 1, b, b + 1):
            intersections += 1
    return (1.0 * intersections) / sample_size

def interval_intersection_probability(L):
    '''Expected value, theoretically derived by integrating over the probability
    mass function.'''
    return (2. * L - 1.) / (L * L)

def plot_probability():
    L = np.linspace(1.001, 10, 100)
    P.plot(L, interval_intersection_probability(L), \
           L, [sample_interval_intersection(x) for x in L], \
           L, [sample_interval_intersection(x, sample_size=1000) for x in L])
    P.grid(True)
    P.legend(['Theoertical', '100 Simulations', '1000 Simulations'])
    P.xlabel('Swimming Pool Opening Interval [Hour]')
    P.ylabel('Probability of Swimming Together')
    P.title('Probability of Adam and Bryan Swimming Together')
    P.show()

if __name__ == '__main__':
    for L in xrange(1, 10):
        print interval_intersection_probability(L), sample_interval_intersection(L)
    plot_probability()
    
