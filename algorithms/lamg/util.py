'''
====================================================================
Common LAMG utilities.
====================================================================
'''
import numpy as np
from scipy.sparse import coo_matrix

def caliber_one_interpolation(aggregate_index):
  # Returns an unweighted caliber-1 interpolation operator P in CSR format.
  # This is an n x nc matrix with entries P(i,aggregate_index(i)) = 1.0,
  # for i=0..n-1, otherwise 0, where n = len(aggregate_index) and
  # nc = max(aggregate_index) + 1. aggregate_index defines a mapping from fine
  # nodes (i) to their coarse aggregate index (I) where both i, I are 0-based
  # indices.
  return caliber_one_interpolation_weighted(
      aggregate_index, np.ones((len(aggregate_index), )))

def caliber_one_interpolation_weighted(aggregate_index, weight):
  # Returns a weighted caliber-1 interpolation operator P in CSR format. This is
  # an n x nc matrix with entries P(i,aggregate_index(i)) = weight(i), for
  # i=0..n-1, otherwise 0, where n = len(aggregate_index) = len(weight) and
  # nc = max(aggregate_index) + 1. aggregate_index defines a mapping from fine
  # nodes (i) to their coarse aggregate index (I) where both i, I are 0-based
  # indices.
  n, nc = len(aggregate_index), max(aggregate_index) + 1
  return coo_matrix(
      (weight, (np.arange(n), aggregate_index)), shape=(n, nc)).tocsr()

def to_column_matrix(x):
  # Converts an ndarray into a scipy column matrix.
  x = np.asmatrix(x)
  if x.shape[0] == 1 and x.shape[1] > 1:
    x = x.transpose()
  return x
