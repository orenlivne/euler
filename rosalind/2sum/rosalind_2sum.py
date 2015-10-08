'''
============================================================
http://rosalind.info/problems/2sum

The Need for Averagesclick to expand

Problem


Given: A positive integer n, a positive integer k, and k arrays of size n
containing integers from 10**(-5) to 10**5.

Return: For each array A[1..n], output two different indices 1 <= p < q <= n
such that A[p]=-A[q] if exist, and "-1" otherwise.
============================================================
'''
import rosutil as ru, itertools as it, random, numpy as np

def two_sum_indices(a):
  # Given an array a, outputs [p, q], indices such that 1 <= p < q <= n
  # such that A[p] = -A[q] if exist, and [-1] otherwise. Complexity: O(n log n).

  # Treat the corner case of two elements equal to 0.
  x = 0
  zero_elements = [i for i, x in enumerate(a) if x == 0]
  if len(zero_elements) >= 2:
    return zero_elements[:2]

  d = dict((x, i) for i, x in enumerate(a))
  for p, x in enumerate(a[:len(a)/2]):
    return [p, d[-x]] if d.has_key(-x) else [-1]

def two_sum_of_file(file_name):
  with open(file_name, 'r') as f:
    f.next() # Skip n, k line
    for line in f:
      # Map 0-based to 1-based indices. Negative (error code) indices are
      # unchanged.
      yield map(lambda x: x if x < 0 else x + 1, two_sum_indices(ru.to_int_list(line)))

def two_sum(file_name):
  return '\n'.join(it.imap(ru.join_list, two_sum_of_file(file_name)))

def two_sum_indices_brute_force(a):
  # Given an array a, outputs [p, q], indices such that 1 <= p < q <= n
  # such that A[p] = -A[q] if exist, and [-1] otherwise. Complexity: O(n log n).
  d = dict((x, i) for i, x in enumerate(a))
  indices = [(p, q + p + 1) for p, x in enumerate(a) for q, y in enumerate(a[p+1:]) if y == -x]
  return indices[0] if indices else [-1]

def test_vs_brute_force_random():
  n = 100
  for i in xrange(10):
    print 'Random experiment %d' % (i,)
    a = np.random.randint(low=-10**5, high=10**5 + 1, size=n)
    assert two_sum_indices(a) == two_sum_indices_brute_force(a)

def test_vs_brute_force_from_file(file_name):
  with open(file_name, 'r') as f:
    f.next() # Skip n, k line
    for i, line in enumerate(f):
      # Map 0-based to 1-based indices. Negative (error code) indices are
      # unchanged.
      a = ru.to_int_list(line)
      r1 = two_sum_indices(a)
      r2 = two_sum_indices_brute_force(a)
      if r1 != r2:
        raise AssertionError('Wrong result, line %d: fast %s bf %s' % (i + 2, repr(r1), repr(r2)))

if __name__ == "__main__":
  test_vs_brute_force_from_file('rosalind_2sum.dat')
  test_vs_brute_force_random()
#  print two_sum('rosalind_2sum_sample.dat')
#  print two_sum('rosalind_2sum.dat')
