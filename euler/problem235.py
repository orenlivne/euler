'''
============================================================
http://projecteuler.net/problem=235

Given is the arithmetic-geometric sequence u(k) = (900-3k)rk-1.
Let s(n) = sum k=1...nu(k).

Find the value of r for which s(5000) = -600,000,000,000.

Give your answer rounded to 12 places behind the decimal point.
============================================================
'''
from numpy import abs

def secant(f, x0, x1, tol):
    f0, f1 = f(x0), f(x1)
    while abs(x0 - x1) > tol:
        print '%.12f %.12f' % (x0, x1)
        x0, x1 = x1, x1 - f1 * (x1 - x0) / (f1 - f0)
        f0, f1 = f1, f(x1)
    print '%.12f %.12f' % (x0, x1)
    return 0.5 * (x0 + x1)

s = lambda x: sum((300 - k) * x ** (k - 1) for k in xrange(1, 5001)) + 2e11

if __name__ == "__main__":
    print '%.12f' % (secant(s, 1.00231, 1.00233, 1e-12),)
