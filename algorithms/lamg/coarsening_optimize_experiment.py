import unittest, level, util, relax, numpy as np, numpy.testing as nt, networkx as nx, coarsening_optimize, matplotlib.pyplot as P

#def test_tv_relax_grid_1d():
n = 10
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
w = optimizer.optimal_weights_kaczmarz(x, num_sweeps=2)
print w

A = level0.A
Q = util.caliber_one_interpolation_weighted(level1.aggregate_index, w)
Ac = np.transpose(Q)*A*Q
P.figure(1)
P.clf()
P.plot([-Ac[i,i+1] for i in xrange(level1.num_nodes-1)], 'bo-')
P.show()

y = A*x
xc = level1.T * x
yc = Ac*xc
print [np.dot(x[:,k], y[:,k]) for k in xrange(K)]
print [np.dot(xc[:,k], yc[:,k]) for k in xrange(K)]
