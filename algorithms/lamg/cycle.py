'''
====================================================================
Multi-level cycle for testing the coarse level grid quality.

For now, only a 2-level cycle is implemented.
====================================================================
'''
import numpy as np, util, level, networkx as nx, itertools as it
from scipy.sparse import coo_matrix, hstack, vstack
from scipy.sparse.linalg import spsolve
from numpy.linalg import norm

class Cycle(object):

  def __init__(self, setup, b):
    # Creates a 2-level cycle from the mult-level setup hierachy 'setup'
    # for solving Ax = b at the finest level.
    self._setup = setup
    self._b = b

    # Augment a row and column to the coarse-level operator for the
    # constant-vector nullspace.
    coarse_level = self._setup.level[1]
    uc = np.ones((coarse_level.num_nodes, 1))
    self._Ac_augmented = vstack((hstack((coarse_level.A, uc)), vstack((uc, 0)).transpose()))

  def run(self, x):
    # Runs a 2-level cycle on the initial guess x. Outputs the new x.
    fine_level = self._setup.level[0]

    # Pre-relaxations.
    x = fine_level.relax(x, self._b, self._setup.nu1)

    # Coarse-level correction.
    coarse_level = self._setup.level[1]
    r = self._b - fine_level.A * x
    rc = coarse_level.R * r
    ec = util.to_column_matrix(spsolve(self._Ac_augmented, vstack((rc, 0)))[:-1])
    e = coarse_level.P * ec
    x += e

    # Post-relaxations.
    x = fine_level.relax(x, self._b, self._setup.nu2)
    return x

def run_cycles(setup, num_cycles=20):
  # Set up Ax = b with a compatible random RHS b so x has non-trivial components
  # to be reduced by cycles.
  A = setup.level[0].A
  b = np.matrix(2 * np.random.rand(setup.level[0].num_nodes, 1) - 1)
  b -= np.mean(b)

  cycle = Cycle(setup, b)
  # Random initial guess.
  x = np.matrix(2 * np.random.rand(setup.level[0].num_nodes, 1) - 1)
  # Run cycles.
  r_new = norm(b - A*x)
  print 'Initial      |r|=%.3e' % (r_new,)
  for i in xrange(1, num_cycles + 1):
    r_old = r_new
    x = cycle.run(x)
    r_new = norm(b - A*x)
    print 'Cycle %2d     |r|=%.3e  (%.2f)' % (i, r_new, r_new / r_old)
