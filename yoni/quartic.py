'''Solve:  (x - 5)(x - 7)(x + 6)(x + 4) = 504.'''

def abs(x):
  return x if x > 0 else -x

def secant(f, x0, x1, eps, max_iter=20):
  '''Solve f(x) = 0 using the secant method, starting from the initial guesses
  x0, x1. Stopping criterion: |f(x)| < eps.'''
  f0, f1, i = f(x0), f(x1), 0
  print i, x0, f0
  print i, x1, f1
  while i < max_iter and abs(f1) > eps and abs(x0-x1) > eps:
    x2 = (x0*f1 - x1*f0)/(f1-f0)
    f2 = f(x2)
    print i, x2, f2
    x0, f0, x1, f1, i = x1, f1, x2, f2, i+1
  return x1

def deriv(f, x):
    '''Derivative of the polynomial f at x.'''
    return 0

if __name__ == '__main__':
  f = lambda x: (x - 5)*(x - 7)*(x + 6)*(x + 4) - 504
  print secant(f, -1, -3, 1e-8)
  print secant(f, 5, 6, 1e-8)
