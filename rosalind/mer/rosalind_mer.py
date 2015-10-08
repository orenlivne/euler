'''
============================================================
http://rosalind.info/problems/mer

The Need for Averagesclick to expand

Problem

The merging procedure is an essential part of Merge Sort (which is considered in
one of the next problems).

Given: A positive integer n and a sorted array A[1..n] of integers from 10**(-5)
 to 10**5, a positive integer m and a sorted array B[1..m] of integers from
10**(-5) to 10**5.

Return: A sorted array C[1..n+m] containing all the elements of A and B.
============================================================
'''
import sys

def merge_sorted(a, b):
  # Given two sorted arrays a, b, returns a sorted array c that contains the
  # elements of a and b.
  na, nb, ia, ib, ai, bi, c = len(a), len(b), 0, 0, a[0], b[0], []
  while (ia < na) or (ib < nb):
    if ai < bi:
      c.append(ai)
      ia += 1
      ai = a[ia] if ia < na else sys.maxint
    else:
      c.append(bi)
      ib += 1
      bi = b[ib] if ib < nb else sys.maxint
  return c

def mer(file_name):
  with open(file_name, 'r') as f:
    na = int(f.next())
    a = map(int, f.next().split())
    if len(a) != na:
      raise ValueError(
          'Number of elements in first array (%d) doesn''t match its size (%d)' \
          % (len(a), na))

    nb = int(f.next())
    b = map(int, f.next().split())
    if len(b) != nb:
      raise ValueError(
          'Number of elements in second array (%d) doesn''t match its size (%d)' \
          % (len(b), nb))

    return ' '.join(map(str, merge_sorted(a, b)))

if __name__ == "__main__":
#  print mer('rosalind_mer_sample.dat')
  print mer('rosalind_mer.dat')
