'''
====================================================================
A single level in the multi-level setup hierarchy. Holds the
action operator, TVs, aggregation info, and transfer operators.
====================================================================
'''
import numpy as np, util, networkx as nx
from scipy.sparse import tril, triu

#---------------------------------------------------------------------
# Factory methods

def create_finest_level(relaxer_factory, g):
  return _FinestLevel(relaxer_factory, g)

def create_coarse_level(relaxer_factory, fine_level, aggregate_index):
  return _CoarseLevel(relaxer_factory, fine_level, aggregate_index)

#---------------------------------------------------------------------

class Level(object):

  def __init__(self, relaxer_factory):
    self._relaxer = relaxer_factory(self.A)

  def tv_relax(self, x, nu):
    # Performs nu relaxation sweeps on Ax=0 starting from the initial value x.
    # x may be a matrix whose columns are TVs.
    for _ in xrange(nu):
      x = self._relaxer.relax_hom(x)
    return x

#---------------------------------------------------------------------

class _FinestLevel(Level):

  def __init__(self, relaxer_factory, g):
    self.g = g
    self.A = nx.laplacian_matrix(g)
    self.W = nx.adjacency_matrix(g)
    super(_FinestLevel, self).__init__(relaxer_factory)

#---------------------------------------------------------------------

class _CoarseLevel(Level):

  def __init__(self, relaxer_factory, fine_level, aggregate_index):
    # Galerkin coarsening
    self.P = util.caliber_one_interpolation(aggregate_index)
    self.R = np.transpose(self.P)
    self.A = self.R * fine_level.A * self.P
    super(_CoarseLevel, self).__init__(relaxer_factory)

    self.fine_level = fine_level
    self.aggregate_index = aggregate_index

    # Recover the graph and adjacency matrix from A.
    # TODO: replace building W by the proper sub-edgelist of A (more efficient?)
    self.W = -tril(self.A, k=-1) - triu(self.A, k=1)
    self.g = nx.from_scipy_sparse_matrix(self.W)
