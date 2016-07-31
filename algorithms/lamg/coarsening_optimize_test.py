import unittest, util, numpy as np, numpy.testing as nt, networkx as nx, level, relax, coarsening_optimize

class TestCoarseningOptimizer(object): #(unittest.TestCase):
  def setUp(self):
    # Construct a weighted 1-D grid graph.
    self.n = 10
    self.g = nx.grid_graph(dim=[self.n])
    for i in xrange(self.n-1):
      self.g[i][i+1]['weight'] = i+1

    # Construct fine level 0 and geometric aggregation coarse level 1.
    self.level0 = level.create_finest_level(relax.create_gauss_seidel_relaxer, self.g)
    geometric_aggregate_index = np.repeat(np.arange(self.n/2), 2)
    self.level1 = level.create_coarse_level(relax.create_gauss_seidel_relaxer, self.level0, geometric_aggregate_index)

  def test_coarsened_fine_energy(self):
    # Construct a quadratic test vector.
    n = self.n
    x = np.arange(n) ** 2

    optimizer = coarsening_optimize.CoarseningOptimizer(self.level1)
    coarsened_fine_energy = optimizer.coarsened_fine_energy(x)

    def ei(i):
      return (i * (2*i-1)**2 if i > 0 else 0) + \
        ((i+1) * (2*i+1)**2 if i < n-1 else 0)

    expected_coarsened_fine_energy = np.matrix(np.array(map(
      lambda I: ei(2*I) + ei(2*I+1), np.arange(n/2))).transpose()).transpose()
    nt.assert_array_equal(coarsened_fine_energy, expected_coarsened_fine_energy)
