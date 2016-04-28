'''The misanthropes are coming. Suppose there is a row of some number, N, of houses in a new, initially empty development. Misanthropes are moving into the development one at a time and selecting a house at random from those that have nobody in them and nobody living next door. They keep on coming until no acceptable houses remain. At most, one out of two houses will be occupied; at least one out of three houses will be. But what's the expected fraction of occupied houses as the development gets larger, that is, as N goes to infinity?

 Complicate the neighborhood, make the misanthropes friendlier, build better fences to make better neighbors, or something even more creative.
'''

import random, numpy as np, matplotlib.pyplot as P, sys

def occupancy_fraction(n):
  '''Performs a random simulation and returns the fraction of occupied houses out of n.'''
  # h encodes
  available = set(range(n))
  occupied = [False] * n
  while available:
    found = False
    while not found:
      c = random.sample(available, 1)[0]    # Candidate house
      found = ((c == 0 or not occupied[c-1]) and (c == n-1 or not occupied[c+1]))
    occupied[c] = True
    available.remove(c)
    if c > 0:
      try: available.remove(c-1)
      except KeyError: pass
    if c < n-1:
      try: available.remove(c+1)
      except KeyError: pass
  fraction = float(sum(1 for status in occupied if status)) / n
#  print ' '.join(map(lambda x: '1' if x else '0', occupied)), '\t', fraction
  return fraction

def expected_occupancy_fraction(n, sample_size=100):
  return sum(occupancy_fraction(n) for _ in xrange(sample_size)) / sample_size

def print_expected_occupancy_fractions(exp_max=8, sample_size=100):
  for n in 2 ** np.arange(1, exp_max + 1):
    print n, expected_occupancy_fraction(n, sample_size=sample_size)

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
  print expected_occupancy_fraction(6, sample_size=10000)
  print_expected_occupancy_fractions(exp_max=10, sample_size=1000)
