import unittest, level, util, relax, numpy as np, numpy.testing as nt, networkx as nx

#def test_tv_relax_grid_1d():
n = 6
g = nx.grid_graph(dim=[n])

# Construct fine level
level0 = level.create_finest_level(relax.create_gauss_seidel_relaxer, g)
geometric_aggregate_index = np.repeat(np.arange(n/2), 2)
level1 = level.create_coarse_level(relax.create_gauss_seidel_relaxer, level0, geometric_aggregate_index)


# Construct test vectors
K = 5
nu = 5
x = 2 * np.random.rand(n,K) - 1 # K TVs, each = rand[-1,1]
x = level0.tv_relax(x, nu)

level1.P * level1.T * x

print x
# TODO: add assertions on x's smoothness.
