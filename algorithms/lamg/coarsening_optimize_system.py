'''
====================================================================
A routine for optimizing the coarse-level operator using TV-energy-
minimizing interpolation. Solves a LS system for the coefficients
of the equation at each aggregate that matches all TVs (potentially
both smooth and non-smooth).
====================================================================
'''
import numpy as np, util, level, networkx as nx, itertools as it
from scipy.sparse import coo_matrix
from scipy.linalg import lstsq

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
    return np.matrix(self._level.R * CoarseningOptimizer.__nodal_energy(self._level.fine_level.W, x))

  def coarse_nodal_energy(self, x, Wc):
    return CoarseningOptimizer.__nodal_energy(Wc, self._level.T * x)

  def optimized_coarse_adjacency_matrix(self, x, num_sweeps=2, factor_sweeps=1):
    # Returns the optimized coarse-level adjacency for the level.
    coarse_level = self._level
    if x.ndim == 1:
      x = np.matrix(x).transpose()
    Wc = coarse_level.W
    xc = coarse_level.T * x
    nc = coarse_level.num_nodes
    for sweep in xrange(num_sweeps):
      energy_fine = self.coarsened_nodal_fine_energy(x)
      print energy_fine.__class__
      weight = [dict() for _ in xrange(nc)]
      for I in xrange(coarse_level.num_nodes):
        nbhrs = Wc[I,:].nonzero()[1]
        print 'I', I, 'nbhrs', nbhrs
        Ec = np.square(xc[nbhrs,:] - np.repeat(np.matrix(xc[I,:]), len(nbhrs), axis=0)).transpose()
        print Ec
        ef = energy_fine[I,:].transpose()
        print ef
        w = lstsq(Ec, ef)[0]
        print 'w', w
        weight[I] = dict((J, wJ[0]) for J, wJ in it.izip(nbhrs, w))
        print weight[I]
      avg_weights = [0.5*(weight[I][J]+weight[J][I]) for I, J in coarse_level.g.edges_iter()]
      Wc = coo_matrix((avg_weights, zip(*coarse_level.g.edges())), shape=Wc.shape).tocsr()
      Wc = Wc + Wc.transpose()
    return Wc
