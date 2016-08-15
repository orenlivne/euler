'''
====================================================================
Relaxation scheme implementation. Runs at a single Level.
====================================================================
'''
import numpy as np, util
from scipy.sparse import tril, triu
from scipy.sparse.linalg import spsolve

#---------------------------------------------------------------------
# Factory methods

def create_gauss_seidel_relaxer(A):
  return _GaussSeidelRelaxer(A)

#---------------------------------------------------------------------

class Relaxer(object):

  def relax_hom(self, x):
    # Performs a relaxation sweep on Ax=0 starting from x and returns the
    # new x. x may be a vector or a matrix.
    raise exception('Must be implemented by sub-classes')

  def relax_non_hom(self, x, b):
    # Performs a relaxation sweep on Ax=b starting from x and returns the
    # new x. x may be a vector or a matrix.
    raise Exception('Must be implemented by sub-classes')

#---------------------------------------------------------------------

class _GaussSeidelRelaxer(Relaxer):

  def __init__(self, A):
    self._M = tril(A).tocsr()
    self._N = triu(A, k=1).tocsr()

  def relax_hom(self, x):
    return util.to_column_matrix(spsolve(self._M, -self._N*x))

  def relax_non_hom(self, x, b):
    return util.to_column_matrix(spsolve(self._M, b - self._N*x))
