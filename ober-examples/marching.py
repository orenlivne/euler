'''
============================================================
An illustration of a marching scheme's numerical instability
in the 2-D homogeneous Laplace equation.

Package requirements: numpy, matplotlib.

Created on September 20, 2012
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
import numpy as np, matplotlib.pyplot as plt
from matplotlib import rcParams

# Run method on a high frequency
np.set_printoptions(precision=3, linewidth=100)
n = 50
# Set the exact solution in the domain and on the boundary
u = np.zeros((n + 1, n + 1), dtype=np.float64)

# Initial conditions: perturb by machine-eps floating point high frequency error
e = np.finfo(np.float64).eps
i, j = np.meshgrid(np.arange(2), np.arange(1, n))
u[1:n, 0:2] = e * (-1) ** (i + j)

# Run the marching method
for i in xrange(2, n + 1):
    u[1:n, i] = 4 * u[1:n, i - 1] - u[0:n - 1, i - 1] - u[2:n + 1, i - 1] - u[1:n, i - 2]

# Monitor growth in norm along lines
U = np.max(u, axis=0)
print 'Growth factor', np.exp(np.diff(np.log(U)))

# Draw the method's symbol
rcParams['text.usetex'] = True
rcParams['text.latex.unicode'] = True
plt.figure(1, figsize=(7, 5))
t = np.linspace(-np.pi, np.pi, 100)
T = 2 - np.cos(t)
plt.plot(t, np.max((T + np.sqrt(T ** 2 -
                                 1), T - np.sqrt(T ** 2 - 1)), axis=0))
plt.xlabel(r'\textrm{Scaled frequency } $\theta$', fontsize=14)
plt.ylabel(r'$\hat{L}(\theta) = \max\{\lambda_1(\theta), \lambda_2(\theta)\}$', fontsize=14)
plt.title(ur'\textrm{Marching Scheme Amplification Factor $\hat{L}(\theta)$}', fontsize=14)
plt.grid(True)
plt.show()
plt.savefig('marching_symbol.png')
