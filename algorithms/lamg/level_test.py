import unittest, level, util, relax, numpy as np, numpy.testing as nt, networkx as nx

#def test_tv_relax_grid_1d():
n = 6
g = nx.grid_graph(dim=[n])

# Construct fine level
lev = level.create_finest_level(relax.create_gauss_seidel_relaxer, g)
np.repeat(np.arange(n/2), 2)

# Construct test vectors
K = 5
nu = 5
x = 2 * np.random.rand(n,K) - 1 # K TVs, each = rand[-1,1]
x = lev.tv_relax(x, nu)

print x
# TODO: add assertions on x's smoothness.
