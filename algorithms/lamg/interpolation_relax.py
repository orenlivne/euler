'''
====================================================================
Relaxation for optimizing the LAMG interpolation weights.
Feasibility test for a periodic 1-D chain.

Fits the weights to a single (ideal) linear TV.
====================================================================
'''
import numpy as np, matplotlib.pyplot as P

def interpolation_relax_gs(w, omega=0.5):
  # Performs an interpolation weight GS relaxation sweep for a periodic 1-D chain of size
  # n, starting from the weights w. Returns the updated w.
  n = len(w)
  for j in xrange(n):
    w[j] = (1-omega)*w[j] + omega*(1.0 - w[(j+1)%n] * w[(j+2)%n])/w[(j-1)%n]
  return w

def interpolation_relax_kac(w, omega=1.0):
  '''Performs an interpolation weight Kaczmarz relaxation sweep for a periodic
  1-D chain of size n, starting from the weights w. Returns the updated w.'''
  n = len(w)
  for j in xrange(0, n, 2):
    residual    = 1.0 - w[(j-1)%n] * w[j] - w[(j+1)%n] * w[(j+2)%n]
    delta       = omega * residual / (w[(j-1)%n] ** 2 + w[(j+2)%n] ** 2)
    w[j]       += delta*w[(j-1)%n]
    w[(j+1)%n] += delta*w[(j+2)%n]
  return w


def ls_functional(w):
  n = len(w)
  return sum((1.0 - w[(j-1)%n] * w[j] - w[(j+1)%n] * w[(j+2)%n]) ** 2 for j in xrange(0, n, 2))
  #return n - 4 * sum((w[(j-1)%n] * w[j] + w[(j+1)%n] * w[(j+2)%n]) for j in xrange(0, n, 2))

'''
def interpolation_relax_kac_jacobi(w, omega=1.0):
  # Performs an interpolation weight Kaczmarz relaxation sweep for a periodic
  # 1-D chain of size n, starting from the weights w. Returns the updated w.
  n = len(w)
  w_new = w.copy()
  for j in xrange(0, n, 2):
    residual        = 1.0 - w[(j-1)%n] * w[j] - w[(j+1)%n] * w[(j+2)%n]
    delta           = omega * residual / (w[(j-1)%n] ** 2 + w[(j+2)%n] ** 2)
    w_new[j]       += delta*w[(j-1)%n]
    w_new[(j+1)%n] += delta*w[(j+2)%n]
  return w_new
'''

def run_relax(n, num_sweeps, relax=interpolation_relax_kac):
  # Runs num_sweeps interpolation weight relaxation sweeps for a periodic 1-D chain of
  # size n.
  P.figure(1)
  P.clf()
  P.hold(True)
  w = 1 * np.ones((n, ))
  print 'Initial', w, ls_functional(w)
  for sweep in xrange(num_sweeps):
    w = relax(w)
    print 'Sweep', sweep, w, ls_functional(w)
  P.plot(w, 'bo-')
  return w

if __name__ == '__main__':
  w = run_relax(1000, 10)
