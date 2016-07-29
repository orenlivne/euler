'''
====================================================================
A routine for optimizing the coarse-level operator using TV-energy-
minimizing interpolation.
====================================================================
'''
import numpy as np, util, level

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

  def fine_energy(self, x):
    W = self._level.W
    n, K = x.shape
    energy_fine = np.zeros(n, K)
    for i in xrange(n):
      nbhrs = W[:,i].nonzero()[0]
      energy_fine[i,:] = A[:,i] * (x[nbhrs,:] - np.repeat(np.matrix(x[0,:]), len(nbhrs), axis=0)) ** 2
    return energy_fine

  def __optimal_weights(self):
    pass
