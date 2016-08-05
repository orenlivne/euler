'''
====================================================================
A routine for optimizing the coarse-level operator using TV-energy-
minimizing interpolation.
====================================================================
'''
import numpy as np, util, level, networkx as nx, itertools as it
from scipy.sparse import csr_matrix

class CoarseningOptimizer(object):

  def __init__(self, coarse_level):
    # Creates an operator optimizer for coarse_level. This must be
    # a coarse level, not the finest level.
    self._level = coarse_level

  @staticmethod
  def __nodal_energy(W, x):
    if x.ndim == 1:
      x = np.matrix(x).transpose()
    n, K = x.shape
    nodal_energy = np.zeros((n, K))
    for i in xrange(n):
      nbhrs = W[i,:].nonzero()[1]
      y = np.square(x[nbhrs,:] - np.repeat(np.matrix(x[i,:]), len(nbhrs), axis=0))
      w = np.repeat(W[nbhrs,i].todense(), K, axis=1)
      nodal_energy[i,:] = np.sum(np.multiply(w, y), axis=0)
    return nodal_energy

  def coarsened_nodal_fine_energy(self, x):
    return self._level.R * CoarseningOptimizer.__nodal_energy(self._level.fine_level.W, x)

  def coarse_nodal_energy(self, x):
    return CoarseningOptimizer.__nodal_energy(self._level.W, self._level.T * x)

  def optimized_coarse_adjacency_matrix(self, x, num_sweeps=3):
    # Returns the optimized coarse-level adjacency for the level.
    if x.ndim == 1:
      x = np.matrix(x).transpose()
    Wc = self._level.W
    for sweep in xrange(num_sweeps):
      for I in xrange(self._level.num_nodes):
        # TODO: only update the coarse and fine vectors instead of recalculating all of them every step
        energy_fine = self.coarsened_nodal_fine_energy(x)
        energy_coarse = self.coarse_nodal_energy(x)
        ef = energy_fine[I,:]
        ec = energy_coarse[I,:]
        w = np.dot(ef, ec) / np.dot(ec, ec)
        Wc[:,I] = w * Wc[:,I]
        Wc[I,:] = w * Wc[I,:]
        print '-'*80
        print 'I', I
        print 'w', w
    return Wc
