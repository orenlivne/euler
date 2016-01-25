# Demonstrates the Lucas-Lehmer primality test for Mersenne
# primes (primes of the form 2^p - 1).
# https://en.wikipedia.org/wiki/Lucas%E2%80%93Lehmer_primality_test

import numpy as np, itertools as it, math

def primes_in_range(n_min, n_max, p):
  # Returns a list of the primes in the range [n_min,n_max) given the list p
  # of all primes < n_min.'''
  candidate = np.empty((n_max - n_min,), dtype=np.bool)
  candidate.fill(True)  # Initially, all are potentially prime
  for b in it.chain(p, xrange(n_min, int(math.floor(math.sqrt(n_max))) + 1)):
    # Remove multiples of b from candidate list
    i = b - n_min
    if b < n_min or candidate[i]:
      r = n_min % b
      start = (b - r) if r > 0 else 0
      if start == i: start += b
      candidate[np.where(candidate[start::b])[0] * b + start] = False
  return n_min + np.where(candidate)[0]

def primes_up_to(n_max):
  return primes_in_range(2, n_max, np.array([], np.long))

def mersenne_primes(exponents):
  # This loop could be parallelized.
  for p in exponents:
    m, s = 2 ** long(p) - 1, 4
    for _ in xrange(p - 2):
      s = (pow(s, 2, m) - 2) % m
      if s == 0: yield p, m

if __name__ == "__main__":
  # Only need to check prime powers. Generating them is fast.
  for p, m in mersenne_primes(primes_up_to(10**8)):
    print 'exponent', p, '#digits', int(math.ceil(math.log10(m)))
