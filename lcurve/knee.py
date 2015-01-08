#!/usr/bin/env python
'''
============================================================
Finds the knee point of a curve.
Adaptation of the Matlab code from
http://www.mathworks.com/matlabcentral/fileexchange/35094-knee-point/content/knee_pt.m 

Created on July 9, 2013
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
import numpy as np, matplotlib.pylab as P, sys

def _line_fit(x, y):
    '''Return the slope m and intercept b of the best line fit y=mx+b to the data x[:k] and y[:k]
    for k=0..len(y).''' 
    # Figure out the m and b (in the y=mx+b sense) for the "left-of-knee"
    n, sigma_x, sigma_y, sigma_xx, sigma_xy = np.arange(1, len(y) + 1), np.cumsum(x), np.cumsum(y), np.cumsum(x * x), np.cumsum(x * y)
    det = np.maximum(n * sigma_xx - sigma_x * sigma_x, 1e-15)
    m = (n * sigma_xy - sigma_x * sigma_y) / det
    b = -(sigma_x * sigma_xy - sigma_xx * sigma_y) / det
    return m, b

'''Reverse an array.'''
_reverse = lambda x: x[-1::-1]

def knee_pt(x, y, absolute_dev=True):
    '''Returns the index of the x-coordinate of the knee of the curve y=f(x).

    Parameters:
    x (required) vector of the same size as y
    y (required) vector (>=3 elements)
    absolute_dev (optional) use sum of square error sums (if False, use sum of root mean square error)
    
    The x and y  don't need to be sorted, they just have to
    correspond: knee_pt([1,2,3],[3,4,5]) = knee_pt([3,1,2],[5,3,4])
    
    Because of the way the function operates y must be at least 3
    elements long and the function will never return either the first or the
    last point as the answer.
    
    The function operates by walking along the curve one bisection point at a time and
    fitting two lines, one to all the points to left of the bisection point and one
    to all the points to the right of of the bisection point.
    The knee is judged to be at a bisection point which minimizes the
    sum of errors for the two fits.
    
    Example:
    >>> x = np.arange(.1, 3, .1)
    >>> y = 3-np.exp(-x) / np.sqrt(x) 
    >>> knee = knee_pt(x, y)
    >>> print knee, x[knee], y[knee]
    >>> plot_knee_point(x, y, knee)

    Food for thought: In the best of possible worlds, per-point errors should
    be corrected with the confidence interval (i.e. a best-line fit to 2
    points has a zero per-point fit error which is kind-a wrong).
    Practially, I found that it doesn't make much difference.'''    
    
    # Check input args
    if len(y) < 3: raise ValueError('knee_pt: y must be at least 3 elements long')
    # Sort x, y in increasing x-order
    if any(np.diff(x) < 0):
        idx = np.argsort(x)
        x, y = x[idx], y[idx]
    else: idx = np.arange(len(x))
    
    # Regression slope (m) and intercept (b) for the "left-of-knee"
    m_fwd, b_fwd = _line_fit(x, y)
    # Regression slope (m) and intercept (b) for the "right-of-knee"
    m_bck, b_bck = map(_reverse, _line_fit(_reverse(x), _reverse(y)))
                       
    # Calculate sum of errors for left- and right- of-knee fits per point
    error_curve = np.tile(np.inf, len(y))
    for breakpt in xrange(1, len(y) - 1):
        err_fwd = m_fwd[breakpt] * x[:breakpt] + b_fwd[breakpt] - y[:breakpt]
        err_bck = m_bck[breakpt] * x[breakpt:] + b_bck[breakpt] - y[breakpt:]
        error_curve[breakpt] = sum(abs(err_fwd)) + sum(abs(err_bck)) if absolute_dev else np.sqrt(sum(err_fwd * err_fwd)) + np.sqrt(sum(err_bck * err_bck))
    # Find location of the min of the error_curve
    return idx[np.argmin(error_curve)]

#---------------------------------
# Example
#---------------------------------
def plot_knee_point(x, y, knee, text_offset=(180, -20)):
    '''Generate a plot of the data y(x), and the knee point at knee (the index of that
    point in the x- and y-arrays).'''
    idx = np.argsort(x)
    fig = P.figure()
    P.clf()
    ax = fig.add_subplot(111)
    P.hold(True)
    ax.plot(x[idx], y[idx], 'bx-', label='Data')
    P.xlabel('x')
    P.ylabel('y')
    P.plot(x[knee], y[knee], 'ro', markersize=10)
    P.annotate('Knee Point (%.3f,%.3f)' % (x[knee], y[knee]), xy=(x[knee], y[knee]), xytext=text_offset,
               textcoords='offset points', ha='right', va='bottom',
               bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
               arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
    P.title('Curve and Knee')

if __name__ == '__main__':
    # Tests
    data = np.loadtxt(sys.argv[1])
    x, y = data[:, 0], data[:, 1]
    knee = knee_pt(x, y)
    print 'Knee at index', knee, 'x', x[knee], 'y', y[knee]
    plot_knee_point(x, y, knee)
    P.show()
    # P.savefig(os.environ['OBER'] + '/code/misc/lcurve/exp.png')
