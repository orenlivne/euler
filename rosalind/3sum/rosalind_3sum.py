'''
============================================================
http://rosalind.info/problems/3sum

Given: A positive integer k <= 20, a postive integer
n <= 10^4, and k arrays of size n containing integers from
10^{-5} to 10^5.

Return: For each array A[1..n], output three different
indices 1 <= p < q < r <= n such that A[p] + A[q] + A[r] = 0
if exist, and "-1" otherwise.
============================================================
'''
import rosutil as ru, itertools as it, random, numpy as np
from scipy import signal

def three_sum_indices_fft(a, s):
  # Given an array a of integers between L1 and L2, outputs (p, q), indices
  # such that 1 <= p < q < r <= n such that A[p] + A[q] + A[r] = s if exist,
  # and None otherwise. Builds a hash table of A[q] + A[r] values using FFT
  # convolution of a bit vector representing A with itself, then proceeds like
  # the 2SUM solver (loop over p, find (q,r) using the hash).
  # Complexity: O(n + L log L) where L = L2 - L1.

  # Build the bit vector of size L. b[0] corresponds to a_min, b[1] to whether
  # or not a_min + 1 is in a, etc.
  a_min, a_max, n = a[0], a[0], len(a)
  for i in xrange(1, n):
    x = a[i]
    if x < a_min: a_min = x
    if x > a_max: a_max = x
  L = a_max - a_min + 1
  b = [0] * L
  for x in a: b[x - a_min] = 1

  # Multiply b with itself using FFT convolution. The locations of 1-bits in
  # the product correspond to all sums y + z of element pairs y, z in a. Store
  # all sums in a set so we can look a sum up in O(1).
  offset = 2 * a_min
  a_2sum = set(i + offset for i, x in enumerate(signal.fftconvolve(b, b)) if abs(x) > 1e-12)

  # Build a hash table of element values to indices. An element may be repeated,
  # so a value is mapped to a set of indices.
  d = {}
  for i, x in enumerate(a):
    d.setdefault(x, set()).add(i)

  # For each p, find whether there exists a sum t = s - A[p] = A[q] + A[r] in
  # a_2sum.
  for p, x in ((p, x) for p, x in enumerate(a) if (s - x) in a_2sum):
    t = s - x
    # Sum exists, loop over q's and find one for which there exists an r
    # such that A[q] + A[r] = t.
    for q, y in enumerate(a[p + 1:], p + 1):
      z = t - y
      if d.has_key(z):
        indices = d[z]
        if y == z and len(indices) > 1:
          # There exist two elements A[q] = A[r] = t/2.
          for r in indices:
            if r != q:
              break
          return (p, q, r)
        else:
          # There exist two differnt elements A[q], A[r] whose sum is t.
          for r in indices:
            if q < r:
              return (p, q, r)
  return None

def two_sum_indices(a, s, d=None):
  # Given an integer array a, outputs (p, q), indices such that 1 <= p < q <= n
  # such that A[p] + A[q] = s if exist, and None otherwise.
  # Complexity: O(n log n).

  # Treat the corner case of two equal elements of size s/2 each.
  if s % 2 == 0:
    half_s = s/2
    zero_elements = [i for i, x in enumerate(a) if x == half_s]
    if len(zero_elements) >= 2:
      return tuple(zero_elements[:2])

  if d is not None:
    d = dict((x, i) for i, x in enumerate(a))
  for p, x in enumerate(a):
    if d.has_key(s - x):
      q = d[s - x]
      if p < q:
        # Since p is increased from 0 to n-1, we could have equivalently
        # checked for p != q, since we will always reach and output a solution
        # (p, q) with p < q before (q, p).
        return (p, q)
  return None

def three_sum_indices_2sum(a, s):
  # Given an array a, outputs (p, q), indices such that 1 <= p < q < r <= n
  # such that A[p] + A[q] + A[r] = s if exist, and None otherwise. Uses n
  # calls of the 2SUM solver (loop over p, find (q,r) using 2SUM).
  # Complexity: O(n^2).
  # This dictionary can be cached instead of re-created n times inside
  # two_sum_indices (this however doesn't change the overall complexity).
  d = dict((x, i) for i, x in enumerate(a))
  for p, x in enumerate(a):
    remaining_indices = two_sum_indices(a[p+1:], s - x, d)
    if remaining_indices is not None:
      # Map remaining_indices from the sub-array a[p+1:] back to indices in a.
      return (p, ) + tuple(map(lambda x: x + p + 1, remaining_indices))
  return None

# Alias for the best algorithm.
three_sum_indices_fast = three_sum_indices_fft
#three_sum_indices_fast = three_sum_indices_2sum

# A value indicating that a solution was not found.
NOT_FOUND = -1

def three_sum_of_file(file_name, s):
  # Generates the 3SUM solutions for each array in the input file 'file_name'.
  with open(file_name, 'r') as f:
    f.next() # Skip n, k header line.
    for line in f:
      # Map 0-based to 1-based indices. Negative index (not found) are unchanged.
      result = three_sum_indices_fast(ru.to_int_list(line), s)
      yield (NOT_FOUND, ) if result is None else map(lambda x: x if x < 0 else x + 1, result)

def three_sum(file_name):
  # Returns a string representation of the 3SUM solution for each array in the
  # input file 'file_name' (one line per input, one line per corresponding output).
  return '\n'.join(it.imap(ru.join_list, three_sum_of_file(file_name, 0)))

#----------------------------------------------------------------
# TESTING FUNCTIONS
def three_sum_indices_brute_force(a, s):
  # Given an array a, outputs [p, q], indices such that 1 <= p < q < r <= n
  # such that A[p] + A[q] + A[r] = s if exist, and None otherwise.
  # Complexity: O(n^3).
  d = dict((x, i) for i, x in enumerate(a))
  indices = [(p0, p1, p2)
             for p0, x in enumerate(a)
             for p1, y in enumerate(a[p0 + 1:], p0 + 1)
             for p2, z in enumerate(a[p1 + 1:], p1 + 1)
             if x + y + z == s]
  return indices[0] if indices else None

def _assert_results_equal(a, s):
  k = 3
  result_fast = three_sum_indices_fast(a, s)
  result_bf = three_sum_indices_brute_force(a, s)
  if ((result_fast is None) ^ (result_bf is None)) or \
  ((result_fast is not None) and (sum(a[result_fast[i]] for i in xrange(k)) != s)):
    raise AssertionError('Wrong result: fast %s bf %s' % \
                         (repr(result_fast), repr(result_bf)))

def test_vs_brute_force_random():
  print 'Random testing'
  n = 150
  s = 0
  for i in xrange(20):
    print 'Random experiment %d' % (i,),
    _assert_results_equal(np.random.randint(low=-10**5, high=10**5 + 1, size=n), s)
    print 'OK'

def test_vs_brute_force_from_file(file_name):
  print 'Testing from file', file_name
  s = 0
  with open(file_name, 'r') as f:
    f.next() # Skip n, k line
    for i, line in enumerate(f):
      _assert_results_equal(ru.to_int_list(line), s)
  print 'OK'
#----------------------------------------------------------------

if __name__ == "__main__":
#  test_vs_brute_force_from_file('rosalind_3sum.dat')
#  print three_sum('rosalind_3sum_sample.dat')
#  test_vs_brute_force_random()
  print three_sum('rosalind_3sum.dat')
