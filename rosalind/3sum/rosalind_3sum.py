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

def two_sum_indices(a, s):
  # Given an array a, outputs (p, q), indices such that 1 <= p < q <= n
  # such that A[p] + A[q] = s if exist, and None otherwise.
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
  # Complexity: O(n^2 log n).
  for p, x in enumerate(a):
    remaining_indices = two_sum_indices(a[p+1:], s - x)
    if remaining_indices is not None:
      # Map remaining_indices from the sub-array a[p+1:] back to indices in a.
      return (p, ) + tuple(map(lambda x: x + p + 1, remaining_indices))
  return None

# Alias for the best algorithm.
three_sum_indices_fast = three_sum_indices_2sum

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
  test_vs_brute_force_random()
  print three_sum('rosalind_3sum_sample.dat')
#  print three_sum('rosalind_3sum.dat')
