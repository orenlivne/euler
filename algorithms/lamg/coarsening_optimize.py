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

  def operator(self):
    # Returns the optimized operator for the level.
    Q = self.interpolation()
    return np.transpose(Q) * self_level.fine_level.A * Q

  def interpolation(self):
    # Returns the optimized interpolation from which the optimized coarse
    # level operator is built via the Galerkin scheme.
    return util.caliber_one_interpolation_weighted(
        self._level.aggregate_index, self.optimal_weights())

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

  def optimal_weights_min_norm(self, x, num_sweeps=20):
    # Minimize weight norm while satisfying TV energy matching.
    if x.ndim == 1:
      x = np.matrix(x).transpose()
    W = self._level.fine_level.W
    n, K = x.shape
    ei = self.coarsened_fine_energy(x)
    ptx = self._level.P * self._level.T * x
    d = [self.__flux_matrix(W, ptx[:,k]) for k in xrange(K)]
    R = self._level.R.tocsr()
#    print 'ei', ei.shape

#    print 'd0', d[0]#.todense()
    # q = vector of interpolation weights to each fine node.
    q = np.ones((n,))
    for sweep in xrange(num_sweeps):
      for I in xrange(self._level.num_nodes):
#        print '-'*80
#        print 'I', I
        for k in xrange(K):
#          print 'k', k
          # Update the weights at all fine nodes of aggregate I to
          # satisfy coarse energy (TV k)[I] = coarsened fine energy (TV k)[I]
          # while moving minimally away from the old weights (Kaczmarz step).
          D = d[k]
          i = R[I,:].nonzero()[1]
          w = D[i,:] * q
#          print 'q', q, q.shape
#          print 'q[i]', q[i], q[i].shape
#          print 'D', D[i,:].todense(), D[i,:].shape
#          print 'w', w, w.shape
#          print 'ei', ei[I,k]
          delta = ei[I,k]/np.dot(w, w);
#          print 'delta', delta
          q[i] = delta * w
#          print 'Updated q', q
#          print 'residual', np.dot(q[i], D[i,:] * q) - ei[I,k]
#    print q
    return q

  def optimal_weights_kaczmarz(self, x, num_sweeps=20):
    if x.ndim == 1:
      x = np.matrix(x).transpose()
    W = self._level.fine_level.W
    n, K = x.shape
    ei = self.coarsened_fine_energy(x)
    ptx = self._level.P * self._level.T * x
    d = [self.__flux_matrix(W, ptx[:,k]) for k in xrange(K)]
    R = self._level.R.tocsr()
#    print 'ei', ei.shape

#    print 'd0', d[0]#.todense()
    # q = vector of interpolation weights to each fine node.
    q = np.ones((n,))
    for sweep in xrange(num_sweeps):
      for I in xrange(self._level.num_nodes):
#        print '-'*80
#        print 'I', I
        for k in xrange(K):
#          print 'k', k
          # Update the weights at all fine nodes of aggregate I to
          # satisfy coarse energy (TV k)[I] = coarsened fine energy (TV k)[I]
          # while moving minimally away from the old weights (Kaczmarz step).
          D = d[k]
          i = R[I,:].nonzero()[1]
          w = D[i,:] * q
#          print 'q', q, q.shape
#          print 'q[i]', q[i], q[i].shape
#          print 'D', D[i,:].todense(), D[i,:].shape
#          print 'w', w, w.shape
#          print 'ei', ei[I,k]
          delta = (ei[I,k] - np.dot(q[i], w))/np.dot(w, w);
#          print 'delta', delta
          q[i] += delta * w
#          print 'Updated q', q
#          print 'residual', np.dot(q[i], D[i,:] * q) - ei[I,k]
#   print q
    return q

  def __flux_matrix(self, W, x):
    # Returns the matrix d[i,j] = a[i,j] * (x[i]-x[j])^2 where x is the result of
    # interpolation from the coarse level.    
    # TODO: rename this function. These are not really fluxes but are edge energy contributions.
    
    # Need only include cross-aggregate edges.
    I = self._level.aggregate_index
    rows, cols = map(np.array, zip(*filter(lambda (row, col): I[row] != I[col], it.izip(*W.nonzero()))))
    
    d_values = [W[row,col]*(x[row] - x[col])**2 for row, col in zip(rows, cols)]
    return csr_matrix((d_values, (rows, cols)), shape=W.shape)
