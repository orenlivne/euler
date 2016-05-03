'''
The misanthropes are coming. Suppose there is a row of some number, N, of
houses in a new, initially empty development. Misanthropes are moving into the
development one at a time and selecting a house at random from those that have
nobody in them and nobody living next door. They keep on coming until no
acceptable houses remain. At most, one out of two houses will be occupied; at
least one out of three houses will be. But what's the expected fraction of
occupied houses as the development gets larger, that is, as N goes to infinity?

Complicate the neighborhood, make the misanthropes friendlier, build better
fences to make better neighbors, or something even more creative.
'''

import random, numpy as np, matplotlib.pyplot as P, itertools as it

def occupancy_fraction(n, debug=False):
  '''Performs a random simulation and returns the fraction of occupied houses
  out of n houses.'''
  available, num_occupied = set(range(n)), 0
  if debug: occupied = [False] * n
  while available:
    c = random.sample(available, 1)[0]    # Candidate house
    num_occupied += 1
    available.remove(c)
    if debug: occupied[c] = True
    if c > 0:
      try: available.remove(c-1)
      except KeyError: pass
    if c < n-1:
      try: available.remove(c+1)
      except KeyError: pass
  if debug: print ' '.join(map(lambda x: '1' if x else '0', occupied)), float(num_occupied) / n
  return float(num_occupied) / n


def expected_occupancy_fraction(n, sample_size=100, debug=False):
  return sum(occupancy_fraction(n, debug=debug) for _ in xrange(sample_size)) / sample_size

def theoretical_expected_occupancy_fraction(N):
  '''
  h[N] = 1 + (2/N) sum_{n=1}^{N-2} h[n]
  h[1] = 1, h[2] = 1

  h[N] = 1 + ((N-1)/N) * (h[N-1] - 1) + (2/N) * h[N-2]
       = ((N-1)/N) * h[N-1] + (2/N) * h[N-2] + (1 - (N-1)/N)
       = ((N-1) * h[N-1] + 2 * h[N-2] + 1)/N

  f(N) = ((N-1)/N)^2 * f[N-1] + (2*(N-2)/N) * f[N-2] + 1/N^2
  f(1) = 1, f(2) = 0.5
  '''
  f2, f1 = 1, 0.5
  yield 0.0
  yield f2
  yield f1
  for n in xrange(3, N + 1):
    f1, f2 = float((n-1)**2 * f1 + 2*(n-2)*f2 + 1) / n**2, f1
    yield f1

def print_expected_occupancy_fractions(exp_max=8, sample_size=100):
  f_theoretical = list(theoretical_expected_occupancy_fraction(2 ** exp_max))
  for n in 2 ** np.arange(1, exp_max + 1):
    print '%4d   %.5f   %.5f' % (n, expected_occupancy_fraction(n, sample_size=10000), f_theoretical[n])

def plot_probability(exp_max=8, sample_size=100):
  N = 2 ** np.arange(1, exp_max + 1)
  P.figure(1)
  P.clf()
  P.plot(N, theoretical_expected_occupancy_fraction(n), '%s-' % (c,), \
         N, expected_expected_occupancy_fraction(n, sample_size=sample_size), '%s--' % (c,))
  P.grid(True)
  P.legend(['n = %d in a row' % (n,) for k in N])
  P.xlabel('No. Houses')
  P.ylabel('Expected Occupancy Fraction')
  P.title('Expected Occupancy Fraction vs. Development Size')
  P.show()

if __name__ == '__main__':
  print_expected_occupancy_fractions(exp_max=10, sample_size=100)
