'''Nick has a terrible sleep schedule. He randomly picks a time between 4 AM and
6 AM to fall asleep, and wakes up at a random time between 11 AM and 1 PM of the
same day. What is the probability that Nick gets between 6 and 7 hours of
sleep?'''

import random

def uniform_random(a,b):
    '''Returns a uniformly random number in [a,b].'''
    return a + (b-a)*random.random()

def probability_interval_in_range(a, b, c, d, min_size, max_size, sample_size=100):
    '''Returns the (approximate, by sampling) probability of an interval whose
    start is random[a,b] and end is random[c,d] being of size between min_size
    and max_size.'''
    num_successes = 0
    for _ in xrange(sample_size):
        interval_size = uniform_random(d,c) - uniform_random(a,b)
        if interval_size >= min_size and interval_size <= max_size:
            num_successes = num_successes + 1
    return (1.0 * num_successes) / sample_size

if __name__ == '__main__':
    p_theoretical = 3./8. # Using phase-space approach, for instance.
    for n in xrange(1, 7):
        sample_size = 10**n
        p = probability_interval_in_range(4, 6, 11, 13, 6, 7, sample_size=sample_size)
        print sample_size, p, abs(p-p_theoretical)
