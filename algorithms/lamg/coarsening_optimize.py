'''
====================================================================
A routine for optimizing the coarse-level operator using TV-energy-
minimizing interpolation.
====================================================================
'''
import numpy as np, util, level, networkx as nx

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
      nbhrs = W[:,i].nonzero()[0]
      y = np.square(x[nbhrs,:] - np.repeat(np.matrix(x[i,:]), len(nbhrs), axis=0))
      w = np.repeat(W[nbhrs,i].todense(), K, axis=1)
      energy_fine[i,:] = np.sum(np.multiply(w, y), axis=0)
    return self._level.R * energy_fine

  def optimal_weights(self, x, num_sweeps=2):
    if x.ndim == 1:
      x = np.matrix(x).transpose()
    K = x.shape[1]
    ei = self.coarsened_fine_energy(x)
    for sweep in xrange(num_sweeps):
      for I in xrange(self._level.num_nodes):
        for k in xrange(K):
          
