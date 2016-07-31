'''
====================================================================
A routine for optimizing the coarse-level operator using TV-energy-
minimizing interpolation.
====================================================================
'''
import numpy as np, util, level, networkx as nx
from scipy.sparse import csr_matrix

class CoarseningOptimizer(object):

  def __init__(self, coarse_level):
    # Creates an operator optimizer for coarse_level. This must be
    # a coarse level, not the finest level.
    self._level = coarse_level

  def operator(self):
    # Returns the optimized operator for the level.
    Q = self.operator()
    return np.transpose(Q) * self_level.fine_level.A * Q

  def interpolation(self):
    # Returns the optimized interpolation from which the optimized coarse
    # level operator is built via the Galerkin scheme.
    return util.caliber_one_interpolation_weighted(
        self._level.aggregate_index, self.__optimal_weights())

  def coarsened_fine_energy(self, x):
    if x.ndim == 1:
      x = np.matrix(x).transpose()
    W = self._level.fine_level.W
    n, K = x.shape
    energy_fine = np.zeros((n, K))
    for i in xrange(n):
      nbhrs = W[i,:].nonzero()[1]
      y = np.square(x[nbhrs,:] - np.repeat(np.matrix(x[i,:]), len(nbhrs), axis=0))
      w = np.repeat(W[nbhrs,i].todense(), K, axis=1)
      energy_fine[i,:] = np.sum(np.multiply(w, y), axis=0)
    return self._level.R * energy_fine

  def optimal_weights(self, x, num_sweeps=2):
    if x.ndim == 1:
      x = np.matrix(x).transpose()
    W = self._level.fine_level.W
    K = x.shape[1]
    ei = self.coarsened_fine_energy(x)
    ptx = self._level.P * self._level.T * x
    d = [self.__flux_matrix(W, ptx[:,k]) for k in xrange(K)]
    R = self._level.R.tocsr()

    for sweep in xrange(num_sweeps):
      for I in xrange(self._level.num_nodes):
        print 'I', I
        for k in xrange(K):
          D = d[k]
          i = R[I,:].nonzero()[1]
          print D[:,i].todense()
          
    return None

  def __flux_matrix(self, W, x):
    rows, cols = W.nonzero()
    d_values = [W[row,col]*(x[row] - x[col])**2 for row, col in zip(rows, cols)]
    return csr_matrix((d_values, (rows, cols)), shape=W.shape)
