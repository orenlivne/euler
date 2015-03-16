'''
================================================================================
A saw_the_stick problem.
The robots want to saw the stick in several pieces. The length of the stick is N
inches. We should help our robots saw the stick. All of the parts should have
integer lengths (1, 2, 3 .. inches, but not 1.2).
As we love the numerical series and especially the Triangular numbers (read more
about Triangular numbers on Wikipedia), you should saw the stick so that the
lengths form the consecutive fragment of the Triangular numbers series with the
maximum quantity (fragment's length). The parts should have different lengths
(no repeating). For example: 64 should divided at 15, 21, 28, because 28, 36 is
shorter and 1, 3, 15, 45 is not a consecutive fragment.

You are given a length of the stick (N). You should return the list of lengths
(integers) for the parts in ascending order. If it's not possible and the
problem does not have a solution, then you should return an empty list.

Created on Mar 15, 2015
@author: Oren Livne <oren.livne@gmail.com>
================================================================================
'''
import math, random

def consecutive_triangular_sum(n, m):
  # Returns the sum of the triangular numbers T_n,...,T_{m-1} where
  # T_n = n*(n+1)/2, T_0 = 0.
  return ((m - 1) * m * (m + 1) - (n - 1) * n * (n + 1)) / 6

def triangular_sequence(n, m):
  # Returns the sequence T_n,...,T_{m-1} of consecutive triangular numbers.
  return [i * (i + 1) / 2 for i in xrange(n, m)]

def saw_the_stick(stick_len):
  # Returns a longest list of consecutive triangular numbers whose sum is
  # stick_len, if exists, otherwise returns an empty list.
  # Complexity: O(N**0.5) using brute force over m and determining if there
  # exists an n for each m.
  m_max = int(math.ceil((2 * stick_len) ** (1. / 2.)))
  Sn_to_n_map = dict([((n - 1) * n * (n + 1) / 6, n) for n in xrange(1, m_max)])
  solutions = filter(lambda (n, m): consecutive_triangular_sum(n, m) == stick_len,
                     ((Sn_to_n_map[(m - 1) * m * (m + 1)/6 - stick_len], m)
                      for m in xrange(1, m_max)
                      if (m - 1) * m * (m + 1)/6 - stick_len in Sn_to_n_map))
  return triangular_sequence(*max((m - n, (n, m)) for n, m in solutions)[1]) if solutions else []

def is_integer(n):
  # Returns true if and only if n is an integer.
  return abs(n - int(n)) < 1e-12

def triangular_index(t):
  # Converts a triangular number t = T_n to its index n. n is integer if and
  # only if t is a triangular number.
  return 0.5 * (-1 + (1 + 8 * t) ** 0.5)

if __name__ == '__main__':
  # These "asserts" using only for self-checking and not necessary for
  # auto-testing.
  assert saw_the_stick(225) == [105, 120], "1st example"
  assert saw_the_stick(64) == [15, 21, 28], "1st example"
  assert saw_the_stick(371) == [36, 45, 55, 66, 78, 91], "1st example"
  assert saw_the_stick(882) == [], "1st example"

  # Random tests.
  for _ in xrange(1000):
    m = random.randint(100, 2000)
    n = random.randint(100, m)
    N = consecutive_triangular_sum(n, m)
    actual = saw_the_stick(N)
    expected = triangular_sequence(n, m)
    if actual != expected:
      assert sum(actual) == N
      assert len(actual) >= len(expected)
      n_actual = triangular_index(actual[0])
      assert is_integer(n_actual)
      m_actual = triangular_index(actual[-1])
      assert is_integer(m_actual)
      assert actual, triangular_sequence(int(n_actual), int(m_actual))
