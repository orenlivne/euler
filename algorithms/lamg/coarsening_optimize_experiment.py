import unittest, level, util, relax, numpy as np, numpy.testing as nt, networkx as nx, coarsening_optimize, matplotlib.pyplot as P, setup, cycle
from scipy.sparse import diags

#def test_tv_relax_grid_1d():
n = 100 #10000
g = nx.grid_graph(dim=[n])
print 'n', n

# Construct fine level
level0 = level.create_finest_level(relax.create_gauss_seidel_relaxer, g)
geometric_aggregate_index = np.repeat(np.arange(n/2), 2)
level1 = level.create_coarse_level(relax.create_gauss_seidel_relaxer, level0, geometric_aggregate_index)
Ac_orig =level1.A

# Construct test vectors
K = 5
nu = 5
x = np.matrix(2 * np.random.rand(n,K) - 1) # K relaxed TVs, each = rand[-1,1]
x = level0.tv_relax(x, nu)
#y = 2 * np.random.rand(n,K) - 1 # K random TVs, each = rand[-1,1]
#x = np.concatenate([x,y], axis=1)
#K = x.shape[1]

#x[:,0] = np.arange(n)
#print x

'''
optimizer = coarsening_optimize.CoarseningOptimizer(level1)
Wc = optimizer.optimized_coarse_adjacency_matrix(x, num_sweeps=1, factor_sweeps=2)
print Wc.todense()

A = level0.A
s = np.sum(Wc, 1)
s = [s[i,0] for i in xrange(level1.num_nodes)]
Ac = diags(s) - Wc
P.figure(1)
P.clf()
edge_weights = [Wc[i,i+1] for i in xrange(level1.num_nodes-1)]
P.plot(edge_weights, 'bo-')
P.show()

y = A*x
xc = level1.T * x
yc = Ac*xc
yc_orig = Ac_orig*xc
x_energy = np.array([np.dot(x[:,k], y[:,k]) for k in xrange(K)])
xc_energy = np.array([np.dot(xc[:,k], yc[:,k]) for k in xrange(K)])
#xc_orig_energy = np.array([np.dot(xc[:,k], yc_orig[:,k]) for k in xrange(K)])
print x_energy
print xc_energy
#print xc_orig_energy
print 1 - x_energy / xc_energy
'''

setup = setup.Setup([level0, level1], 2, 1)
cycle.run_cycles(setup)
