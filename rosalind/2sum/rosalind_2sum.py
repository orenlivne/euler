'''
============================================================
http://rosalind.info/problems/2sum

Given: A positive integer n, a positive integer k, and k arrays of size n
containing integers from 10**(-5) to 10**5.

Return: For each array A[1..n], output two different indices 1 <= p < q <= n
such that A[p]=-A[q] if exist, and "-1" otherwise.
============================================================
'''
import rosutil as ru, itertools as it, random, numpy as np

def two_sum_indices(a, s):
  # Given an array a, outputs (p, q), indices such that 1 <= p < q <= n
  # such that A[p] + A[q] = s if exist, and (-1) otherwise.
  # Complexity: O(n log n).

  # Treat the corner case of two equal elements of size s/2 each.
  if s % 2 == 0:
    half_s = s/2
    zero_elements = [i for i, x in enumerate(a) if x == half_s]
    if len(zero_elements) >= 2:
      return tuple(zero_elements[:2])

  d = dict((x, i) for i, x in enumerate(a))
  for p, x in enumerate(a):
    if d.has_key(s - x):
      q = d[s - x]
      if p != q:
        return (p, q)
  return (-1, )

def two_sum_of_file(file_name, s):
  with open(file_name, 'r') as f:
    f.next() # Skip n, k line
    for line in f:
      # Map 0-based to 1-based indices. Negative index (not found) are unchanged.
      yield map(lambda x: x if x < 0 else x + 1, two_sum_indices(ru.to_int_list(line), s))

def two_sum(file_name):
  return '\n'.join(it.imap(ru.join_list, two_sum_of_file(file_name, 0)))

def two_sum_indices_brute_force(a, s):
  # Given an array a, outputs [p, q], indices such that 1 <= p < q <= n
  # such that A[p] + A[q] = s if exist, and [-1] otherwise.
  # Complexity: O(n^2).
  d = dict((x, i) for i, x in enumerate(a))
  indices = [(p, q) for p, x in enumerate(a) for q, y in enumerate(a[p+1:], p + 1) if x + y == s]
  return indices[0] if indices else [-1]

def _assert_results_equal(a, s):
  r1 = two_sum_indices(a, s)
  r2 = two_sum_indices_brute_force(a, s)
  if ((r1[0] == -1) ^ (r2[0] == -1)) or ((r1[0] != -1) and (a[r1[0]] + a[r1[1]] != s)):
    raise AssertionError('Wrong result, line %d: fast %s bf %s' % (i + 2, repr(r1), repr(r2)))

def test_vs_brute_force_random():
  print 'Random testing'
  n = 1000
  s = 0
  for i in xrange(10):
    print 'Random experiment %d' % (i,)
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

if __name__ == "__main__":
#  test_vs_brute_force_from_file('rosalind_2sum.dat')
#  test_vs_brute_force_random()
#  print two_sum('rosalind_2sum_sample.dat')
  print two_sum('rosalind_2sum.dat')
