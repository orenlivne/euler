#!/usr/bin/env python
'''
============================================================
Find the "knee" of an L-curve: the point of optimal
trade-off. This is the point of maximum curvature. The data
is the distribution of Probes I and II median beta values. 

Algorithm:
- Fit the data using an asymptotic series, since it has this
  approximate shape (a0 + a1/x + a2/x^2 + ...).
- Calculate the curvature of the approximant.
- Return the point of maximum curvature.

Created on October 26, 2012
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
import numpy as np 
import matplotlib.pylab as P 
from numpy.core.numeric import newaxis
from scipy.optimize.minpack import curve_fit

def curvature(x, y):
    '''Calculate the approximate curvature k(x) = y''(x)/(1 + y'(x)^2)^(3/2)
    of a curve y(x) using finite differences.'''
    dy = np.diff(y) / np.diff(x)
    xm = 0.5 * (x[:-1] + x[1:])
    dy2 = np.diff(dy) / np.diff(xm)
    dya = 0.5 * (dy[:-1] + dy[1:])
    return dy2 / (1 + dya ** 2) ** 1.5

def fit_curve(x, y):
    '''Fit the data y(x) using an asymptotic series approximation f. The fit is weighted using a variance
    model of Poisson distribution.'''
    f = lambda x, a, b, c, d: a + b / x + c / x ** 2 + d / x ** 3
    (p, _) = curve_fit(f, x, y, sigma=np.max(np.concatenate(([np.ones((len(x), 1)), np.sqrt(y)[:, newaxis]]), axis=1), axis=1))
    return f(x, *p)

def plot_data_and_model(x, y, f, knee, title):
    '''Generate a plot of the data y(x), fitted curve f, and knee point (knee is the index of that
    point into the x-array).'''
    P.figure(1)
    P.clf()
    P.hold(True)
    P.plot(x, y, 'x', label='Data')
    P.plot(x, f, 'r-', label='Fit')
    P.title(title)
    P.xlabel(r'$\beta$')
    P.ylabel('Frequency')
    P.legend(loc=0)
    P.plot(x[knee], y[knee], 'ko', markersize=8)

def fit_probe_data(x_filename, y_filename, title):
    '''Fit the prone data (x-coordinates and y -coordinates are assumed to be in the input files
    x_filename and y_filename, respectively); calculate the knee; and generate a plot showing the
    data and model.'''
    # Load data
    x = np.loadtxt(x_filename, skiprows=1)
    y = np.loadtxt(y_filename, skiprows=1)
    # Fit model
    f = fit_curve(x, y)
    # Calculate curvature and knee point
    k = curvature(x, f)
    knee = np.argmax(k)

    # Generate plot
    plot_data_and_model(x, y, f, knee, title)
    print 'Input file names %s, %s, knee point (%.2f, %.2f)' % (x_filename, y_filename, x[knee], y[knee])
    P.savefig('%s.png' % (title,))
    P.show()

if __name__ == '__main__':
    '''
    --------------------------------------------------
    Main program
    --------------------------------------------------
    '''
    for probe in ('I', 'II'):
        fit_probe_data('mads.%s.txt' % (probe,), 'freq.%s.txt' % (probe,), 'Probe %s' % (probe,))
