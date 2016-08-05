import unittest, level, util, relax, numpy as np, numpy.testing as nt, networkx as nx, coarsening_optimize, matplotlib.pyplot as P
from scipy.sparse import diags

#def test_tv_relax_grid_1d():
n = 100
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

#x[:,0] = np.arange(n)
print x

optimizer = coarsening_optimize.CoarseningOptimizer(level1)
Wc = optimizer.optimized_coarse_adjacency_matrix(x, num_sweeps=2)
print Wc.todense()

A = level0.A
s = np.sum(Wc, 1)
s = [s[i,0] for i in xrange(level1.num_nodes)]
Ac = diags(s) - Wc
P.figure(1)
P.clf()
P.plot([Wc[i,i+1] for i in xrange(level1.num_nodes-1)], 'bo-')
P.show()

y = A*x
xc = level1.T * x
yc = Ac*xc
print [np.dot(x[:,k], y[:,k]) for k in xrange(K)]
print [np.dot(xc[:,k], yc[:,k]) for k in xrange(K)]
